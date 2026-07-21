from dataclasses import dataclass,asdict
import json

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


def batch_load_questions(count,PATH):
    with open(PATH,"r",encoding="utf-8") as f:
        data = json.load(f)

        retrieval_inputs = []
        generation_inputs = []

        for i in range(count):
            ques = data["question"][i]
            contexts = data["contexts"][i]
            ground_truth = data["ground_truth"][i]
            response = data["responses"][i][0]["text"]  
            retrieval_inputs.append(RetrievalInput(ques,contexts,ground_truth))
            generation_inputs.append(GenerationInput(ques,contexts,response))

    return retrieval_inputs,generation_inputs

def save_results(retrieval_results, generation_results, PATH):
    combined_data = []
    
    for ret_res, gen_res in zip(retrieval_results, generation_results):
        entry = {
            "retrieval_evaluation": asdict(ret_res),
            "generation_evaluation": asdict(gen_res)
        }
        
        combined_data.append(entry)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)
