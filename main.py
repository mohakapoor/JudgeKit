from src.orchestrator import orchestrator
from config import PATH
import time
import argparse
import json
import os
from src.utils import batch_load_questions, append_result_jsonl


def main(in_path, out_path, sample=None, start_idx=0):
    eval_inputs = batch_load_questions(in_path, sample)
    
    if start_idx > 0:
        print(f"Resuming from test case {start_idx + 1}...")
    elif os.path.exists(out_path):
        os.remove(out_path) # Clear the file if we are starting fresh from 0
            
    print(f"Starting evaluation of {len(eval_inputs)} test cases...\n")
    
    for i in range(start_idx, len(eval_inputs)):
        input = eval_inputs[i]
        eval_out = orchestrator(input)
        
        print(i+1,"test case(s) evaluated")
        time.sleep()
        append_result_jsonl(eval_out, out_path)
            
    # Generate a pretty-printed JSON file for human readability
    pretty_path = out_path.replace(".json", "_readable.json")
    if pretty_path == out_path:
        pretty_path = out_path + "_readable.json"
        
    data = []
    with open(out_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
                
    with open(pretty_path, "w", encoding="utf-8") as out_f:
        json.dump(data, out_f, indent=4)
        
    print(f"\nReadable JSON successfully exported to: {pretty_path}")
            
    return len(eval_inputs)

if __name__ == "__main__":
    from dataclasses import asdict
    parser = argparse.ArgumentParser(description="JudgeKit CLI")
    parser.add_argument("--input", type=str, default=PATH)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--idx", type=int, default=0, help="Starting index (0-based) to resume from.")
    
    args = parser.parse_args()
    count = main(args.input, args.output, args.sample, args.idx)
    print(f"\nSuccessfully evaluated and saved {count} questions to {args.output}!")
        
