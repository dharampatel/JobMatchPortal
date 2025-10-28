from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import tempfile
import json
import re

from app.deep_agent import master_agent
from app.tools import (
    resume_file_validator,
    query_validator,
    search_jobs,
    generate_cover_letter
)

app = FastAPI()

# Enable CORS for the frontend to access the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def stream_pipeline(file_path: str, role_query: str):
    """
    Generator to stream updates using DeepAgents for each sub-task.
    """

    try:
        # --- Resume Validation ---
        yield json.dumps({"step": "resume_validation", "status": "running"}) + "\n"
        resume_result = resume_file_validator.run(file_path)
        yield json.dumps({
            "step": "resume_validation",
            "status": "completed",
            "resume_text_snippet": resume_result.get("resume_text", "")[:200]
        }) + "\n"

        # --- Query Validation ---
        yield json.dumps({"step": "query_validation", "status": "running"}) + "\n"
        query_result = query_validator.run(role_query)
        yield json.dumps({
            "step": "query_validation",
            "status": "completed",
            "query": query_result.get("query")
        }) + "\n"

        # --- Resume Parsing (Improved JSON handling) ---
        yield json.dumps({"step": "resume_parsing", "status": "running"}) + "\n"

        resume_text = resume_result.get("resume_text", "")

        resume_parse_prompt = f"""
        You are an expert resume parser. Extract structured information from the text below.

        Resume:
        \"\"\"{resume_text}\"\"\"

        Return only valid JSON in this format:
        {{
            "name": "Full name",
            "contact": "Email or phone number",
            "summary": "Short summary or headline",
            "skills": ["list", "of", "skills"],
            "experience": [
                {{
                    "position": "Job title",
                    "company": "Company name",
                    "years": "Duration or timeline",
                    "details": "Responsibilities or key work"
                }}
            ],
            "education": [
                {{
                    "degree": "Degree",
                    "institution": "University or college",
                    "year": "Graduation year"
                }}
            ]
        }}
        Do not include any markdown, text, or explanations — JSON only.
        """

        parse_response = master_agent.invoke({"messages": [{"role": "user", "content": resume_parse_prompt}]})
        raw_resume_data = parse_response["messages"][-1].content.strip()

        # --- Try to extract valid JSON from response ---
        try:
            resume_data = json.loads(raw_resume_data)
        except Exception:
            json_match = re.search(r"\{.*\}", raw_resume_data, re.DOTALL)
            if json_match:
                try:
                    resume_data = json.loads(json_match.group(0))
                except Exception:
                    resume_data = {"raw_text": raw_resume_data}
            else:
                resume_data = {"raw_text": raw_resume_data}

        yield json.dumps({
            "step": "resume_parsing",
            "status": "completed",
            "resume_data": resume_data
        }) + "\n"

        # --- Job Search ---
        yield json.dumps({"step": "job_search", "status": "running"}) + "\n"
        job_search_result = search_jobs(role_query)
        jobs = job_search_result.get("jobs", [])
        yield json.dumps({
            "step": "job_search",
            "status": "completed",
            "jobs": jobs
        }) + "\n"

        # --- Job Match Validation ---
        yield json.dumps({"step": "job_match_validation", "status": "running"}) + "\n"
        alignment_prompt = f"""
        Analyze how well the resume matches the following jobs.

        Resume:
        {resume_text}

        Jobs:
        {json.dumps(jobs, indent=2)}

        Return JSON only:
        {{
            "alignment_score": "0-100",
            "summary": "short summary of alignment reasoning"
        }}
        """
        alignment_response = master_agent.invoke({"messages": [{"role": "user", "content": alignment_prompt}]})
        raw_alignment_data = alignment_response["messages"][-1].content.strip()

        try:
            alignment_data = json.loads(raw_alignment_data)
        except Exception:
            json_match = re.search(r"\{.*\}", raw_alignment_data, re.DOTALL)
            if json_match:
                alignment_data = json.loads(json_match.group(0))
            else:
                alignment_data = {"alignment_score": "N/A", "summary": raw_alignment_data}

        yield json.dumps({
            "step": "job_match_validation",
            "status": "completed",
            "alignment_score": alignment_data.get("alignment_score"),
            "summary": alignment_data.get("summary", "")
        }) + "\n"

        # --- Cover Letter Generation ---
        yield json.dumps({"step": "cover_letter_generation", "status": "running"}) + "\n"

        resume_text = resume_result.get("resume_text", "")
        if not resume_text:
            raise ValueError("Resume text is missing. Ensure that resume parsing is working correctly.")

        # Now call the generate_cover_letter tool with the correct inputs
        cover_letter_result = generate_cover_letter.run({
            "resume_text": resume_text,  # Ensure resume_text is passed correctly
            "job_data": jobs  # This should be a list of job objects (make sure it's properly formatted)
        })

        yield json.dumps({
            "step": "cover_letter_generation",
            "status": "completed",
            "cover_letter": cover_letter_result
        }) + "\n"

        # --- Done ---
        yield json.dumps({"step": "done", "status": "completed"}) + "\n"

    except Exception as e:
        yield json.dumps({
            "step": "error",
            "status": "failed",
            "message": str(e)
        }) + "\n"


@app.post("/apply/stream")
async def apply_job_stream(file: UploadFile = File(...), role: str = Form(...)):
    """
    Endpoint to stream the job application process using resume and job role query.
    """
    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # Return a streaming response
    return StreamingResponse(stream_pipeline(file_path, role), media_type="text/event-stream")
