from backend.services.llm_service import ask_llm

def evaluate_answer(question, answer):

    prompt = f'''
    Evaluate the candidate answer.

    Question:
    {question}

    Answer:
    {answer}

    Return:
    - Score out of 10
    - Strengths
    - Weaknesses
    - Improvement Suggestions
    '''

    return ask_llm(prompt)
