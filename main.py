from src.orchestrator import orchestrator
from config import PATH
import time
import argparse
import json
from src.utils import batch_load_questions,save_results


def main(in_path, out_path, sample=None):
    eval_inputs = batch_load_questions(in_path, sample)
    res = []
    
    print(f"Starting evaluation of {len(eval_inputs)} test cases...\n")
    
    for i, input in enumerate(eval_inputs):
        eval_out = orchestrator(input)
        res.append(eval_out)
        
        print(i+1,"test case(s) evaluated")
        
        time.sleep(6) #this is due to rpm limits
    
    save_results(res, out_path)
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
        
