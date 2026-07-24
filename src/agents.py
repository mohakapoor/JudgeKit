import os
from groq import Groq
from dotenv import load_dotenv
import json
import time
from config import RETRIEVAL_SYSTEM_PROMPT,GENERATION_SYSTEM_PROMPT
from config import TEMPERATURE,MODEL_NAME
from src.utils import calculate_cost,RetrievalMetrics,GenerationMetrics,EvalOutput

load_dotenv()


def retrieval_eval_agent(usr_prompt_retrieval):
    
    groq_api_key = os.getenv("GROQ_API_KEY")

    client = Groq(
        api_key=groq_api_key
    )
    start = time.time()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": RETRIEVAL_SYSTEM_PROMPT},
            {"role": "user", "content": usr_prompt_retrieval}
        ],
        response_format={"type":"json_object"}
    )
    end = time.time()
    raw_text = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    cost = calculate_cost(input_tokens,output_tokens)
    parsed_json = json.loads(raw_text)
    parsed_json["cost"] = cost
    parsed_json["latency"] = end - start
    parsed_json["inference_time"] = response.usage.total_time

    return RetrievalMetrics(**parsed_json)

def generation_eval_agent(usr_prompt_generation):
    groq_api_key = os.getenv("GROQ_API_KEY")

    client = Groq(
        api_key=groq_api_key
    )
    start = time.time()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": usr_prompt_generation}
        ],
        response_format={"type":"json_object"}
    )
    end = time.time()
    raw_text = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    cost = calculate_cost(input_tokens,output_tokens)
    parsed_json = json.loads(raw_text)
    parsed_json["cost"] = cost
    parsed_json["latency"] = end-start
    parsed_json["inference_time"] = response.usage.total_time

    return GenerationMetrics(**parsed_json)
