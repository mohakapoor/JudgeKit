from src.utils import EvalInput,EvalOutput
from src.prompt_builder import build_retrieval_prompt,build_generation_prompt
from src.agents import retrieval_eval_agent,generation_eval_agent

def orchestrator(data:EvalInput):
    ret_prompt = build_retrieval_prompt(data)
    gen_prompt = build_generation_prompt(data)

    ret_metrics = retrieval_eval_agent(ret_prompt)
    gen_metrics = generation_eval_agent(gen_prompt)

    return EvalOutput(
        retrieval_metrics=ret_metrics,
        generation_metrics=gen_metrics,
        total_cost=ret_metrics.cost+gen_metrics.cost,
        total_latency=ret_metrics.latency+gen_metrics.latency,
        total_inference_time=ret_metrics.inference_time+gen_metrics.inference_time
    )