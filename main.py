from src.orchestrator import orchestrator
from config import PATH
import time
import argparse
import json
import os
from src.utils import batch_load_questions, append_result_jsonl


def main(in_path, out_path, sample=None):
    eval_inputs = batch_load_questions(in_path, sample)
    
    start_idx = 0
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            start_idx = sum(1 for line in f if line.strip())
        if start_idx > 0:
            print(f"Resuming from test case {start_idx + 1}...")
            
    print(f"Starting evaluation of {len(eval_inputs)} test cases...\n")
    
    for i in range(start_idx, len(eval_inputs)):
        input = eval_inputs[i]
        eval_out = orchestrator(input)
        
        print(i+1,"test case(s) evaluated")
        
        append_result_jsonl(eval_out, out_path)
        
        if i < len(eval_inputs) - 1:
            time.sleep(5) #this is due to rpm limits
            
    return len(eval_inputs)

if __name__ == "__main__":
    from dataclasses import asdict
    parser = argparse.ArgumentParser(description="JudgeKit CLI")
    parser.add_argument("--input", type=str, default=PATH)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--sample", type=int, default=None)
    
    args = parser.parse_args()
    count = main(args.input, args.output, args.sample)
    print(f"\nSuccessfully evaluated and saved {count} questions to {args.output}!")
        
