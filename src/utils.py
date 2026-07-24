from dataclasses import dataclass,asdict
import json
from config import INPUT_COST,OUTPUT_COST,PATH
from random import randint

@dataclass
class EvalInput:
    query:str
    response: str
    contexts: list[str]
    ground_truth: str

@dataclass
class EvalOutput:
    precision_score: float = None
    precision_reasoning: str = None
    recall_score: float = None
    recall_reasoning: str = None
    faithfulness_score: float = None
    faithfulness_reasoning: str = None 
    relevance_score: float = None
    relevance_reasoning: str = None
    cost: float = 0.0
    latency: float = 0.0
    inference_time: float = 0.0    


@dataclass
class RetrievalInput:
    query: str
    contexts: list[str]
    ground_truth: str 

@dataclass
class RetrievalOutput:
    precision_score: float
    precision_reasoning: str
    recall_score: float
    recall_reasoning: str
    cost: float
    latency: float
    inference_time: float

@dataclass
class GenerationInput:
    query: str 
    contexts: list[str]
    response: str 

@dataclass
class GenerationOutput:
    faithfulness_score: float
    faithfulness_reasoning: str 
    relevance_score: float
    relevance_reasoning: str
    cost: float
    latency: float
    inference_time: float


def format_contexts(raw_contexts):
    formatted = []
    for c in raw_contexts:
        if isinstance(c, dict) and "text" in c and "metadata" in c:
            meta = c["metadata"]
            
            file_path = meta.get("path", meta.get("filename", "Unknown File"))
            
            # Strip out the knowledge_base/repos/ prefix so the Repo name is the root
            if file_path.startswith("knowledge_base\\repos\\"):
                file_path = file_path.replace("knowledge_base\\repos\\", "", 1)
            elif file_path.startswith("knowledge_base/repos/"):
                file_path = file_path.replace("knowledge_base/repos/", "", 1)
                
            start = meta.get("start_line", "?")
            end = meta.get("end_line", "?")
            formatted.append(f"File: {file_path} (Lines {start}-{end})\nContext:\n{c['text']}")
        else:
            formatted.append(str(c))
    return formatted

def batch_load_questions(PATH,count=5):
    with open(PATH,"r",encoding="utf-8") as f:
        data = json.load(f)

        inputs = []

        for i in range(count):
            ques = data["question"][i]
            contexts = format_contexts(data["contexts"][i])
            ground_truth = data["ground_truth"][i]
            response = data["responses"][i]  
            inputs.append(EvalInput(ques,response,contexts,ground_truth))

    return inputs


def random_ques_loader():
    with open(PATH,"r",encoding="utf-8") as f:
        data = json.load(f)
        i = randint(0,51)
        ques = data["question"][i]
        contexts = format_contexts(data["contexts"][i])
        ground_truth = data["ground_truth"][i]
        response = data["responses"][i]  
        e = EvalInput(ques,response,contexts,ground_truth)

    return e

def save_results(eval_res, PATH):
    combined_data = []
    
    for e in eval_res:
        combined_data.append(asdict(e))

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)


def calculate_cost(input_tokens,output_tokens):
    return ((input_tokens * INPUT_COST) + (output_tokens * OUTPUT_COST))/1000000