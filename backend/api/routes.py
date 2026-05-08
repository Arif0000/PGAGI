from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from backend.services.resume_service import extract_resume_text
from backend.services.interview_service import generate_question
from backend.services.evaluation_service import evaluate_answer

router = APIRouter()

SESSION = {
    "resume_text": "",
    "role": "",
    "history": []
}


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    try:

        content = await file.read()

        text = extract_resume_text(content)

        SESSION["resume_text"] = text

        return {
            "message": "Resume processed successfully",
            "resume_preview": text[:1000]
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )


@router.post("/start-interview")
async def start_interview(role: str):

    try:

        SESSION["role"] = role

        question = generate_question(
            SESSION["resume_text"],
            role,
            SESSION["history"]
        )

        return {
            "question": question
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )


@router.post("/submit-answer")
async def submit_answer(question: str, answer: str):

    try:

        feedback = evaluate_answer(
            question,
            answer
        )

        SESSION["history"].append({
            "question": question,
            "answer": answer,
            "feedback": feedback
        })

        next_question = generate_question(
            SESSION["resume_text"],
            SESSION["role"],
            SESSION["history"]
        )

        return {
            "feedback": feedback,
            "next_question": next_question
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )


@router.get("/report")
async def get_report():

    try:

        return {
            "total_questions": len(SESSION["history"]),
            "history": SESSION["history"]
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )
