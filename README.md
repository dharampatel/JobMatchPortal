# Job Application Assistant 🚀

An AI-powered Job Application Assistant that automates the entire process of job application submission, from resume parsing to job matching and cover letter generation.
Built using FastAPI, Streamlit, and DeepAgent (LLMs), this project leverages machine learning and automation to streamline the hiring process.

<img width="1641" height="877" alt="Screenshot 2025-10-28 at 11 41 10 AM" src="https://github.com/user-attachments/assets/e027fa98-d419-4cd8-874c-a7d7e2c9d937" />

# Project Overview

This project is a job application automation pipeline designed to help job seekers optimize their applications by automating the tedious tasks of:


1. Resume Validation – Check if the resume is valid and well-structured.

2. Query Validation – Validate and normalize job roles.

3. Resume Parsing – Extract structured data from unstructured resumes.

4. Job Search – Find relevant jobs based on a user-provided role.

5. Job Match Validation – Analyze how well the resume matches the job descriptions.

6. Cover Letter Generation – Generate a personalized cover letter for each job.

# Tech Stack

### Backend: FastAPI
 – Fast and modern web framework for building APIs.

### Frontend: Streamlit
 – Python framework for building interactive web applications.

**AI Models:** DeepAgent, LLMs (Large Language Models) – Used for resume parsing, job matching, and cover letter generation.

### File Handling: tempfile
 – Used to temporarily save uploaded files.

### Real-time Updates: Server-Sent Events (SSE)
 – For real-time pipeline updates.

# Features

1. **Upload Resume (PDF):** Users can upload a resume and query a job role.

2. **Real-time Streaming:** Receive real-time updates for each step of the process.

3. **Job Matching:** AI analyzes how well the resume fits with relevant job openings.

4. **Cover Letter Generation:** Generate a personalized cover letter based on job matching.

5. **Interactive UI:** User-friendly interface built with Streamlit for easy interaction.

6. **Error Handling:** Graceful error handling and detailed feedback at each step of the pipeline.

# Setup and Installation
### Prerequisites

Python 3.8+

Virtual environment (recommended for isolating dependencies)

## Steps

1. **Clone the repository:**

. git clone https://github.com/dharampatel/JobMatchPortal.git
. cd job-application-assistant


2. **Create a virtual environment (optional but recommended):**

. python -m venv venv
. source venv/bin/activate  # For Linux/MacOS
. venv\Scripts\activate     # For Windows


3. **Install dependencies:**

. pip install -r requirements.txt


4. **Start the backend API with FastAPI:**

. uvicorn app.main:app --reload


5. **Start the Streamlit frontend:**

. streamlit run app/frontend.py

#### Ensure that the FastAPI backend and Streamlit frontend are both running before interacting with the app.

# Usage

1. **Upload Resume:** Choose a .pdf resume from your computer and upload it.

2. **Enter Job Query:** Type in the job title (or role) you're applying for.

3. **Submit:** Click "Submit" to start the process.

4. **Track Progress:** You will see real-time updates at each step, including:

. Resume validation

. Resume parsing

. Job search results

. Job match validation

. Cover letter generation

5. **Download Cover Letter:** Once the cover letter is generated, you can download it as a .txt file.

# API Documentation

**The FastAPI backend serves the following endpoints:**

. POST /apply/stream

**Request:**

. file: The uploaded resume in .pdf format.

. role: The job role (e.g., "Software Engineer").

**Response:**

. Server-Sent Events (SSE) streaming updates at each stage of the pipeline (resume validation, job search, job match, cover letter generation).

**Example:**

. POST http://localhost:8000/apply/stream

# Frontend

The Streamlit UI allows users to interact with the Job Application Assistant easily. It provides:

. A file uploader to upload the resume.

. A text input to enter the job role.

. A real-time streaming interface that updates step-by-step, showing progress and results.

### Streamlit UI Screenshots:

<img width="1636" height="492" alt="Screenshot 2025-10-28 at 11 41 35 AM" src="https://github.com/user-attachments/assets/20ac9cfc-fe61-4c69-9d19-9c623a14452b" />

<img width="1650" height="819" alt="Screenshot 2025-10-28 at 11 48 36 AM" src="https://github.com/user-attachments/assets/56a87dce-709d-4548-9d3f-f1a737120e8d" />

<img width="1662" height="793" alt="Screenshot 2025-10-28 at 11 48 56 AM" src="https://github.com/user-attachments/assets/9c0348c8-dc5f-4fc4-ae8a-25a1e2ff27b1" />

# Acknowledgments

. FastAPI for building the backend API.

. Streamlit for simplifying the frontend UI.

. DeepAgent and LLMs for AI-driven resume parsing and job matching.



