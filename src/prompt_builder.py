from src.utils import EvalInput

def build_retrieval_prompt(data:EvalInput) -> str:
    return f"""
    <user_query>{data.query}</user_query>
    <context>{data.contexts}</context>
    Ground Truth: {data.ground_truth}
    """

def build_generation_prompt(data:EvalInput) -> str:
    return f"""
    <user_query>{data.query}</user_query>
    <context>{data.contexts}</context>
    <response>{data.response}</response>
    Ground Truth: {data.ground_truth}
    """
    

    
        
