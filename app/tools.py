from typing import Dict, Any, Optional, List
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader

from app.config import tavily_client, llm


# --------------------------
# Utility to read PDF text
# --------------------------
def load_resume_text(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return "\n".join([d.page_content for d in docs])


# --------------------------
# Resume Validator Tool
# --------------------------
@tool
def resume_file_validator(file_path: str) -> Dict[str, Any]:
    """
    Validates whether the uploaded PDF is a resume.
    :param file_path:
    :return:
    """
    text = load_resume_text(file_path)
    return {"resume_text": text}


# --------------------------
# Query Validator Tool
# --------------------------
@tool
def query_validator(query: str) -> Dict[str, Any]:
    """
    Validates whether the user query is job-related.
    :param query:
    :return:
    """
    return {"query": query}


# --------------------------
# Job Search Tool
# --------------------------
def search_jobs(role: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Finds relevant jobs using Tavily search API.
    :param role:
    :param max_results:
    :return:
    """
    results = tavily_client.search(query=f"{role} job openings", max_results=max_results)
    jobs = []
    for r in results.get("results", [])[:max_results]:
        jobs.append({
            "title": r.get("title", ""),
            "company": r.get("domain", ""),
            "description": r.get("content", "")[:300],
            "url": r.get("url", "")
        })
    return {"jobs": jobs}


# --------------------------
# Cover Letter Generator Tool
# --------------------------
@tool
def generate_cover_letter(resume_text: str, job_data: Optional[List[Dict]] = None) -> str:
    """
    Generates a tailored cover letter using resume and job info.
    :param resume_text: Text extracted from resume
    :param job_data: List of jobs
    """
    if job_data is None:
        job_data = []

    prompt = f"""You are an expert cover-letter writer.
Using this resume data:
{resume_text}
And these job postings:
{job_data}
Write a 300-word professional cover letter."""

    return llm.invoke(prompt).content