from src.agent import eval_retrieval,eval_generation
from config import PATH
import json
from src.utils import batch_load_questions,save_results
def main():
    r,g = batch_load_questions(PATH,2)

    r_res = eval_retrieval(r[0])
    g_res = eval_generation(g[0])
    
    return r_res,g_res

if __name__ == "__main__":
    r_res, g_res = main()
    
    print("\n" + "="*50)
    print("RETRIEVAL EVALUATION")
    print("="*50)
    print(json.dumps(r_res, indent=4))
    
    print("\n" + "="*50)
    print("GENERATION EVALUATION")
    print("="*50)
    print(json.dumps(g_res, indent=4))
    print("\n")
