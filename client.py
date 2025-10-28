import streamlit as st
import requests
import json
import tempfile
import pandas as pd

st.set_page_config(page_title="Job Application Assistant", layout="wide")
st.title("🚀 Job Application Assistant")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
role = st.text_input("Enter Job Role / Query", "")

if st.button("Submit") and uploaded_file and role:
    st.info("Pipeline started...")

    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        file_path = tmp.name

    # Create placeholders for each step (updated dynamically)
    sections = {
        "resume_validation": st.empty(),
        "query_validation": st.empty(),
        "resume_parsing": st.empty(),
        "job_search": st.empty(),
        "job_match_validation": st.empty(),
        "cover_letter_generation": st.empty(),
        "error": st.empty(),
    }

    url = "http://localhost:8000/apply/stream"

    with requests.post(url, data={"role": role}, files={"file": open(file_path, "rb")}, stream=True) as r:
        for line in r.iter_lines():
            if not line:
                continue

            try:
                event = json.loads(line.decode("utf-8"))
                step = event.get("step")
                status = event.get("status")

                if step not in sections:
                    continue

                container = sections[step]
                container.empty()

                with container.container():
                    st.markdown(f"### {step.replace('_',' ').title()}")
                    st.write(f"**Status:** {status}")

                    # --- Resume Validation ---
                    if step == "resume_validation" and "resume_text_snippet" in event:
                        st.text_area("Resume Text Snippet", event["resume_text_snippet"], height=150)

                    # --- Query Validation ---
                    elif step == "query_validation" and "query" in event:
                        st.write(f"Query: {event['query']}")

                    # --- Resume Parsing (PRETTY UI with auto JSON fix) ---
                    elif step == "resume_parsing" and "resume_data" in event:
                        raw_data = event["resume_data"]

                        # --- Try to parse structured JSON ---
                        resume_data = None
                        if isinstance(raw_data, dict):
                            resume_data = raw_data
                        else:
                            try:
                                resume_data = json.loads(raw_data)
                            except Exception:
                                resume_data = {}

                        # --- If still empty, extract key fields manually ---
                        if not resume_data or len(resume_data.keys()) <= 3:
                            text = str(raw_data)
                            resume_data = {}

                            # Extract common fields with basic heuristics
                            import re

                            name_match = re.search(r"(?i)(?:name|full name)[:\-]?\s*([A-Za-z\s]+)", text)
                            contact_match = re.search(r"(?i)(?:email|contact|phone)[:\-]?\s*([^\n,]+)", text)
                            skills_match = re.findall(
                                r"(?i)\b(?:Python|Java|C\+\+|JavaScript|React|Node|SQL|AWS|Docker|LangChain|ML|AI|Data)\b",
                                text)
                            education_match = re.search(r"(?i)(B\.?Tech|M\.?Tech|Bachelor|Master|PhD|BSc|MSc)[^,\n]*",
                                                        text)
                            exp_match = re.findall(r"(?i)([0-9]+(?:\+)?\s*(?:years|yrs)[^.\n]*)", text)

                            if name_match:
                                resume_data["name"] = name_match.group(1).strip()
                            if contact_match:
                                resume_data["contact"] = contact_match.group(1).strip()
                            if skills_match:
                                resume_data["skills"] = list(set(skills_match))
                            if education_match:
                                resume_data["education"] = [education_match.group(0)]
                            if exp_match:
                                resume_data["experience"] = exp_match

                            if not resume_data:
                                st.warning("⚠️ Could not extract structured resume details. Showing raw data below:")
                                st.text(text)

                        # --- Render the structured resume nicely ---
                        st.markdown("## 🧾 Parsed Resume Preview")

                        col1, col2 = st.columns([2, 1])
                        name = resume_data.get("name") or resume_data.get("Name") or "N/A"
                        contact = (
                                resume_data.get("contact")
                                or resume_data.get("Contact")
                                or resume_data.get("Contact Info", "N/A")
                        )
                        summary = resume_data.get("summary") or resume_data.get("Summary", "")

                        with col1:
                            st.markdown(f"### 👤 **{name}**")
                            st.markdown(f"📞 {contact}")
                        with col2:
                            if summary:
                                st.markdown(f"**Summary:** {summary}")

                        st.divider()

                        # ----- Skills -----
                        skills = resume_data.get("Skills") or resume_data.get("skills", [])
                        if skills:
                            st.markdown("### 🧠 Skills")
                            if isinstance(skills, str):
                                skill_list = [s.strip() for s in skills.split(",") if s.strip()]
                            else:
                                skill_list = skills
                            st.markdown(
                                "<div style='background-color:#f0f2f6; padding:10px; border-radius:5px;'>"
                                + ", ".join(skill_list)
                                + "</div>",
                                unsafe_allow_html=True,
                            )

                        # ----- Experience -----
                        experience = resume_data.get("Experience") or resume_data.get("experience", [])
                        if experience:
                            st.markdown("### 💼 Experience")
                            exp_list = experience if isinstance(experience, list) else [experience]
                            for exp in exp_list:
                                st.markdown(
                                    f"""
                                    <div style='background-color:#eef6ff; padding:10px; border-radius:5px; margin-bottom:5px;'>
                                    {exp}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                        # ----- Education -----
                        education = resume_data.get("Education") or resume_data.get("education", [])
                        if education:
                            st.markdown("### 🎓 Education")
                            edu_list = education if isinstance(education, list) else [education]
                            for edu in edu_list:
                                st.markdown(
                                    f"""
                                    <div style='background-color:#f5fff2; padding:10px; border-radius:5px; margin-bottom:5px;'>
                                    {edu}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                    # --- Job Search ---
                    elif step == "job_search" and "jobs" in event:
                        jobs = event["jobs"]
                        if jobs:
                            st.markdown("### 💼 Jobs Found")
                            table_data = []
                            for job in jobs:
                                table_data.append({
                                    "Title": job.get("title", ""),
                                    "Company": job.get("company", ""),
                                    "URL": f"[Link]({job.get('url','')})"
                                })
                            df = pd.DataFrame(table_data)
                            st.table(df)
                        else:
                            st.write("No jobs found.")

                    # --- Job Match Validation ---
                    elif step == "job_match_validation" and "alignment_score" in event:
                        st.write(f"Alignment Score: {event['alignment_score']}")
                        try:
                            score = float(event["alignment_score"])
                            if score < 70:
                                st.warning("⚠️ Some jobs may not match the resume well.")
                        except:
                            pass

                    # --- Cover Letter Generation ---
                    elif step == "cover_letter_generation" and "cover_letter" in event:
                        st.markdown("### 📝 Generated Cover Letter")
                        st.text_area("Cover Letter", event["cover_letter"], height=250)
                        st.download_button(
                            label="📄 Download Cover Letter",
                            data=event["cover_letter"],
                            file_name="cover_letter.txt",
                            mime="text/plain",
                        )

                    # --- Error Handling ---
                    elif step == "error":
                        st.error(f"Pipeline Error: {event.get('message')}")

            except Exception as e:
                st.error(f"Error decoding event: {e}")
