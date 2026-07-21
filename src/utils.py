from dataclasses import dataclass
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

        retrieval_list = []
        generation_list = []

        for i in range(count):
            ques = data["question"][i]
            contexts = data["contexts"][i]
            ground_truth = data["ground_truth"][i]
            response = data["responses"][i][0]["text"]  
            retrieval_list.append(RetrievalInput(ques,contexts,ground_truth))
            generation_list.append(GenerationInput(ques,contexts,response))

    return retrieval_list,generation_list

