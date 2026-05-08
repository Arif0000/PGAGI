
from backend.services.llm_service import ask_llm

def generate_question(resume_text, role, history):

    previous_context = "\n".join([
        f"Q: {h['question']} A: {h['answer']}"
        for h in history
    ])

    prompt = f'''
    Candidate Role: {role}

    Resume:
    {resume_text[:4000]}

    Previous Interview Context:
    {previous_context}

    Generate ONE advanced technical interview question.
    Make it adaptive and relevant to the candidate background.
    Avoid generic questions.
    '''

    return ask_llm(prompt)
