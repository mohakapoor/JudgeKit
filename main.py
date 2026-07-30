from src.orchestrator import orchestrator
from config import PATH
import time
import argparse
import json
import os
from src.utils import batch_load_questions, append_result_jsonl
from aggregated_results import aggregate_results


def main(in_path, out_path, sample=None, start_idx=0):
    eval_inputs = batch_load_questions(in_path)
    
    end_idx = len(eval_inputs)
    if sample is not None:
        end_idx = min(start_idx + sample, len(eval_inputs))
        
    eval_count = end_idx - start_idx
    if eval_count <= 0:
        print("No test cases to evaluate.")
        return 0
    
    if start_idx > 0:
        print(f"Resuming from test case {start_idx + 1}...")
        if os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content.startswith("[") and content.endswith("]"):
                try:
                    arr = json.loads(content)
                    with open(out_path, "w", encoding="utf-8") as f:
                        for item in arr:
                            f.write(json.dumps(item) + "\n")
                except json.JSONDecodeError:
                    pass
    elif os.path.exists(out_path):
        os.remove(out_path) 
            
    print(f"Starting evaluation of {eval_count} test cases...\n")
    
    for i in range(start_idx, end_idx):
        input = eval_inputs[i]
        eval_out = orchestrator(input)
        
        print(i+1,"test case(s) evaluated")
        append_result_jsonl(eval_out, out_path)
        
        time.sleep(5)

    data = []
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            if content.startswith("[") and content.endswith("]"):
                pass # Already formatted, do nothing
            else:
                for line in content.split('\n'):
                    if line.strip():
                        data.append(json.loads(line))
                with open(out_path, "w", encoding="utf-8") as out_f:
                    json.dump(data, out_f, indent=4)
            
    return eval_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JudgeKit CLI")
    parser.add_argument("--input", type=str, default=PATH)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--idx", type=int, default=0) # Starting index (0-based)
    
    args = parser.parse_args()
    count = main(args.input, args.output, args.sample, args.idx)
    print(f"\nSuccessfully evaluated and saved {count} questions to {args.output}!")
    aggregate_results(args.output)
