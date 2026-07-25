from src.utils import EvalInput, clean_path
from pathlib import Path

def calc_metrics(eval_input):
    hit_at_k = 0.0
    mrr = 0.0

    if eval_input.relevant_files is None:
        raise ValueError("relevant_files must be provided in the dataset to calculate Hit@K and MRR. The old ground-truth string fallback has been permanently removed.")

    normalized_relevant = [clean_path(f) for f in eval_input.relevant_files]
    if len(normalized_relevant) == 0:
        return None, None

    for idx, context in enumerate(eval_input.contexts):
        first_line = context.split('\n')[0] 
        raw_path = first_line.replace("File: ", "").split(" (Lines")[0].strip()
        context_path = Path(raw_path)
        
        if context_path in normalized_relevant:
            hit_at_k = 1.0
            mrr = 1.0 / (idx + 1)
            break

    return hit_at_k,mrr