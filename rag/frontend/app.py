
import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Interview System", layout="wide")

st.title("AI-Powered Interview System")

if "question" not in st.session_state:
    st.session_state.question = None

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

role = st.selectbox(
    "Select Role",
    ["AI/ML Engineer", "Backend Engineer", "Data Scientist"]
)

if uploaded_file and st.button("Start Interview"):

    files = {
        "file": uploaded_file.getvalue()
    }

    upload_response = requests.post(
        f"{API}/upload-resume",
        files=files
    )

    response = requests.post(
        f"{API}/start-interview",
        params={"role": role}
    )

    st.session_state.question = response.json()["question"]

if st.session_state.question:

    st.subheader("Interview Question")

    st.info(st.session_state.question)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):

        response = requests.post(
            f"{API}/submit-answer",
            params={
                "question": st.session_state.question,
                "answer": answer
            }
        )

        data = response.json()

        st.subheader("Feedback")
        st.write(data["feedback"])

        st.session_state.question = data["next_question"]

if st.button("Generate Final Report"):
    report = requests.get(f"{API}/report").json()

    st.subheader("Interview Summary")
    st.json(report)
