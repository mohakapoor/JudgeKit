import os
from groq import Groq, RateLimitError
from dotenv import load_dotenv
import json
import time
from functools import wraps
from config import RETRIEVAL_SYSTEM_PROMPT,GENERATION_SYSTEM_PROMPT
from config import TEMPERATURE,MODEL_NAME
from src.utils import calculate_cost,RetrievalMetrics,GenerationMetrics,EvalOutput

load_dotenv()


def with_key_rotation(env_var_name):
    api_keys_str = os.getenv(env_var_name, "")
    keys = [k for k in api_keys_str.split(",") if k]
    state = {"idx": 0}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                # Force the environment variable to the current key
                os.environ[env_var_name] = keys[state["idx"]]
                
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    error_msg = str(e).lower()
                    if "tokens per day" in error_msg or "tpd" in error_msg:
                        state["idx"] += 1
                        if state["idx"] >= len(keys):
                            print(f"All {len(keys)} keys exhausted")
                            raise e
                            
                        print("TPD limit hit retrying...")
                        time.sleep(1)
                    else:
                        print("TPM/RPM limit hit, waiting 60 seconds before retrying...")
                        time.sleep(60)
                except Exception as e:
                    retries += 1
                    if retries > 5:
                        print(f"Max retries exceeded for unexpected error: {e}")
                        raise e
                    sleep_time = 2 ** retries  # Exponential backoff: 2s, 4s, 8s, 16s, 32s
                    print(f"Unexpected error (network/json): {e}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
        return wrapper
    return decorator


@with_key_rotation("GROQ_API_KEY")
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
    p_scores = [s for s in parsed_json.get("precision_score", []) if s is not None]
    parsed_json["precision_score"] = sum(p_scores) / len(p_scores) if p_scores else 0.0

    r_scores = [s for s in parsed_json.get("recall_score", []) if s is not None]
    parsed_json["recall_score"] = sum(r_scores) / len(r_scores) if r_scores else 0.0

    parsed_json["cost"] = cost
    parsed_json["latency"] = end - start
    parsed_json["inference_time"] = response.usage.total_time

    return RetrievalMetrics(**parsed_json)

@with_key_rotation("GROQ_API_KEY")
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
    f_scores = [s for s in parsed_json.get("faithfulness_score", []) if s is not None]
    parsed_json["faithfulness_score"] = sum(f_scores) / len(f_scores) if f_scores else 0.0

    r_scores = [s for s in parsed_json.get("relevance_score", []) if s is not None]
    parsed_json["relevance_score"] = sum(r_scores) / len(r_scores) if r_scores else 0.0

    c_scores = [s for s in parsed_json.get("correctness_score", []) if s is not None]
    parsed_json["correctness_score"] = sum(c_scores) / len(c_scores) if c_scores else 0.0
    parsed_json["cost"] = cost
    parsed_json["latency"] = end-start
    parsed_json["inference_time"] = response.usage.total_time

    return GenerationMetrics(**parsed_json)
