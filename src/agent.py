import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_test_reponse(ques):
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    client = Groq(
        api_key=groq_api_key
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        messages=[
            {"role": "system", "content": "You are a LLM response Judge. You will get query, context, llm_answer and ground_truth. You give a 1-10 scale score that tells if the llm_answer matches what the user asked for. After that 1-10 score you will return a single line of reasoning behind your score "},
            {"role": "user", "content": ques}
        ]
    )

    return response
