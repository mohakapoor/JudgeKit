from dataclasses import dataclass,asdict
import json
from config import INPUT_COST,OUTPUT_COST,PATH
from random import randint
from pathlib import Path

def clean_path(p_str):
    p = Path(p_str)
    parts = p.parts
    if len(parts) >= 2 and parts[0] == "knowledge_base" and parts[1] == "repos":
        return Path(*parts[2:])
    return p

@dataclass
class EvalInput:
    query:str
    response: str
    contexts: list[str]
    ground_truth: str
    relevant_files: list[str] = None

@dataclass
class RetrievalMetrics:
    precision_score: float = None
    precision_reasoning: list[str] = None
    recall_score: float = None
    recall_reasoning: list[str] = None
    hit_at_k: float = None
    mrr: float = None
    cost: float = 0.0
    latency: float = 0.0
    inference_time: float = 0.0

@dataclass
class GenerationMetrics:
    faithfulness_score: float = None
    faithfulness_reasoning: list[str] = None
    relevance_score: float = None
    relevance_reasoning: list[str] = None
    correctness_score: float = None
    correctness_reasoning: list[str] = None
    cost: float = 0.0
    latency: float = 0.0
    inference_time: float = 0.0

@dataclass
class EvalOutput:
    retrieval_metrics: RetrievalMetrics = None
    generation_metrics: GenerationMetrics = None
    total_cost: float = 0.0
    total_latency: float = 0.0
    total_inference_time: float = 0.0




def format_contexts(raw_contexts):
    formatted = []
    for c in raw_contexts:
        if isinstance(c, dict) and "text" in c and "metadata" in c:
            meta = c["metadata"]
            
            file_path = meta.get("path", meta.get("filename", "Unknown File"))
            
            # Use pathlib to cleanly extract the path relative to repos
            clean_p = clean_path(file_path)
                
            start = meta.get("start_line", "?")
            end = meta.get("end_line", "?")
            formatted.append(f"File: {str(clean_p)} (Lines {start}-{end})\nContext:\n{c['text']}")
        else:
            formatted.append(str(c))
    return formatted

def batch_load_questions(PATH):
    with open(PATH,"r",encoding="utf-8") as f:
        data = json.load(f)

        inputs = []
        count = len(data["question"])

        for i in range(count):
            ques = data["question"][i]
            contexts = format_contexts(data["contexts"][i])
            ground_truth = data["ground_truth"][i]
            response = data.get("answer", data.get("responses"))[i]  
            relevant_files = data["relevant_files"][i] if "relevant_files" in data and len(data["relevant_files"]) > i else None
            inputs.append(EvalInput(ques,response,contexts,ground_truth,relevant_files))

    return inputs


def random_ques_loader():
    with open(PATH,"r",encoding="utf-8") as f:
        data = json.load(f)
        i = randint(0,51)
        ques = data["question"][i]
        contexts = format_contexts(data["contexts"][i])
        ground_truth = data["ground_truth"][i]
        response = data.get("answer", data.get("responses"))[i]  
        relevant_files = data["relevant_files"][i] if "relevant_files" in data and len(data["relevant_files"]) > i else None
        e = EvalInput(ques,response,contexts,ground_truth,relevant_files)

    return e

def save_results(eval_res, path):
    combined_data = []
    
    for e in eval_res:
        combined_data.append(asdict(e))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)

def append_result_jsonl(eval_res, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(eval_res)) + "\n")


def calculate_cost(input_tokens,output_tokens):
    return ((input_tokens * INPUT_COST) + (output_tokens * OUTPUT_COST))/1000000