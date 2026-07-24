from src.utils import EvalInput

def build_retrieval_prompt(data:EvalInput) -> str:
    return f"""
    Query: {data.query}
    Context: {data.contexts}
    Ground Truth: {data.ground_truth}
    """

def build_generation_prompt(data:EvalInput) -> str:
    return f"""
    Query: {data.query}
    Context: {data.contexts}
    Response: {data.response}
    Ground Truth: {data.ground_truth}
    """
    

    
        
