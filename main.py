from src.agent import eval_retrieval,eval_generation
from config import PATH
import time
import json
from src.utils import batch_load_questions,save_results
def main():
    retrieval_results,generation_results = batch_load_questions(PATH)
    res = []
    for ret_res, gen_res in zip(retrieval_results, generation_results):
        r_res = eval_retrieval(ret_res)
        g_res = eval_generation(gen_res)
        res.append((r_res,g_res))
        time.sleep(6)
    
    return res

if __name__ == "__main__":
    from dataclasses import asdict
    results = main()
    
    for i, (r_res, g_res) in enumerate(results):
        print("\n" + "="*60)
        print(f"TEST CASE {i+1}")
        print("="*60)
        
        print("\n[RETRIEVAL EVALUATION]")
        print(json.dumps(asdict(r_res), indent=4))
        
        print("\n[GENERATION EVALUATION]")
        print(json.dumps(asdict(g_res), indent=4))
        
    print("\nAll test cases completed!")
