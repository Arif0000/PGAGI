import streamlit as st
import requests

API = "https://pgagi-backend.onrender.com"

st.set_page_config(
    page_title="AI Interview System",
    layout="wide"
)

st.title("AI-Powered Interview System")

if "question" not in st.session_state:
    st.session_state.question = None

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

role = st.selectbox(
    "Select Role",
    [
        "AI/ML Engineer",
        "Backend Engineer",
        "Data Scientist"
    ]
)

if uploaded_file and st.button("Start Interview"):

    try:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        upload_response = requests.post(
            f"{API}/upload-resume",
            files=files,
            timeout=120
        )

        st.write("Upload Status:", upload_response.status_code)

        if upload_response.status_code != 200:
            st.error(upload_response.text)
            st.stop()

        response = requests.post(
            f"{API}/start-interview",
            params={"role": role},
            timeout=120
        )

        st.write("Interview Status:", response.status_code)

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        try:
            data = response.json()
        except Exception:
            st.error("Backend returned invalid JSON")
            st.code(response.text)
            st.stop()

        st.session_state.question = data.get("question")

    except Exception as e:
        st.error(str(e))

if st.session_state.question:

    st.subheader("Interview Question")

    st.info(st.session_state.question)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):

        try:

            response = requests.post(
                f"{API}/submit-answer",
                params={
                    "question": st.session_state.question,
                    "answer": answer
                },
                timeout=120
            )

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            try:
                data = response.json()
            except Exception:
                st.error("Invalid JSON from backend")
                st.code(response.text)
                st.stop()

            st.subheader("Feedback")
            st.write(data.get("feedback"))

            st.session_state.question = data.get("next_question")

        except Exception as e:
            st.error(str(e))

if st.button("Generate Final Report"):

    try:

        response = requests.get(
            f"{API}/report",
            timeout=120
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        report = response.json()

        st.subheader("Interview Summary")
        st.json(report)

    except Exception as e:
        st.error(str(e))
