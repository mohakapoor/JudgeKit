from src.utils import EvalInput

def calc_metrics(eval_input):
    hit_at_k = 0.0
    mrr = 0.0

    for idx, context in enumerate(eval_input.contexts):
        first_line = context.split('\n')[0] 
        file_path = first_line.replace("File: ", "").split(" (Lines")[0].strip()
        file_name = file_path.split("/")[-1].split("\\")[-1]
        if file_name in eval_input.ground_truth:
            hit_at_k = 1.0
            
            # Rank is index + 1 (so index 0 becomes Rank 1)
            mrr = 1.0 / (idx + 1)
            
            # We found the highest ranked hit, so stop looking!
            break 

    return hit_at_k,mrr