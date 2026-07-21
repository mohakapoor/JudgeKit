from dataclasses import dataclass
@dataclass
class RetrievalInput:
    query: str
    contexts: list[str]
    ground_truth: str 

@dataclass
class GenerationOutput:
    faithfulness_score: float
    faithfulness_reasoning: str 
    relevance_score: float
    relevance_reasoning: str



@dataclass
class GenerationInput:
    query: str 
    contexts: list[str]
    response: str 

