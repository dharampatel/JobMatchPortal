from app.config import llm
from app.tools import resume_file_validator, query_validator, search_jobs, generate_cover_letter

resume_validator_sub_agent = {
    "name": "resume-validator-agent",
    "description": "Validates uploaded resume file.",
    "system_prompt": "You are ResumeValidatorAgent. Check if a PDF is a valid resume. Return JSON with {valid: true/false, reason: string}.",
    "tools": [resume_file_validator],
    "model": llm
}

query_validator_sub_agent = {
    "name": "query-validator-agent",
    "description": "Validates job-related query.",
    "system_prompt": "You are QueryValidatorAgent. Check if the user query is about job search. Return JSON {is_job_query: true/false, reason: string}.",
    "tools": [query_validator],
    "model": llm
}

job_match_validator_sub_agent = {
    "name": "job-match-validator-agent",
    "description": "Checks alignment between resume and job postings.",
    "system_prompt": "You are JobMatchValidatorAgent. Compare resume text and job postings. Return JSON {alignment_score: number 0-100, aligned: true/false, reason: string}.",
    "tools": [],
    "model": llm
}

resume_parser_sub_agent = {
    "name": "resume-parser-agent",
    "description": "Parses resume into structured data.",
    "system_prompt": "You are ResumeParserAgent. Extract skills, experience_summary, achievements, education_summary. Return JSON.",
    "tools": [],
    "model": llm
}

job_search_sub_agent = {
    "name": "job-search-agent",
    "description": "Searches and structures job listings for a query.",
    "system_prompt": "You are JobSearchAgent. Use search_jobs tool and format output JSON list with title, company, description, url.",
    "tools": [search_jobs],
    "model": llm
}

cover_letter_sub_agent = {
    "name": "cover-letter-agent",
    "description": "Generates tailored cover letters.",
    "system_prompt": "You are CoverLetterAgent. Use provided resume info + job info to create a compelling cover letter.",
    "tools": [generate_cover_letter],
    "model": llm
}