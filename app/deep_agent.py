from deepagents import create_deep_agent

from app.config import llm
from app.sub_agent import resume_validator_sub_agent, query_validator_sub_agent, job_match_validator_sub_agent, \
    resume_parser_sub_agent, job_search_sub_agent, cover_letter_sub_agent
from app.tools import resume_file_validator, query_validator, search_jobs, generate_cover_letter

# --------------------------
# Master DeepAgent
# --------------------------

master_agent = create_deep_agent(
    tools=[resume_file_validator, query_validator, search_jobs, generate_cover_letter],
    system_prompt="""You are MasterAgent. Coordinate the workflow:
    1. Validate resume
    2. Validate query
    3. Parse resume
    4. Search jobs
    5. Validate job match
    6. Generate cover letter
    Return JSON with status, resume_data, jobs, cover_letter.""",
    subagents=[
        resume_validator_sub_agent,
        query_validator_sub_agent,
        job_match_validator_sub_agent,
        resume_parser_sub_agent,
        job_search_sub_agent,
        cover_letter_sub_agent
    ],
    model=llm
)