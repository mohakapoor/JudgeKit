from src.utils import RetrievalInput,GenerationInput

def build_retrieval_prompt(data:RetrievalInput) -> str:
    return f"""
    Query: {data.query}
    Context: {data.contexts}
    Ground Truth: {data.ground_truth}
    """

def build_generation_prompt(data:GenerationInput) -> str:
    return f"""
    Query: {data.query}
    Context: {data.contexts}
    Response: {data.response}
    """
    

    
        
