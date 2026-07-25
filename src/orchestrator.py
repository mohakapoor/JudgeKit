from src.utils import EvalInput,EvalOutput
from src.prompt_builder import build_retrieval_prompt,build_generation_prompt
from src.agents import retrieval_eval_agent,generation_eval_agent
from src.deterministic import calc_metrics

def orchestrator(data:EvalInput):
    ret_prompt = build_retrieval_prompt(data)
    gen_prompt = build_generation_prompt(data)

    gen_metrics = generation_eval_agent(gen_prompt)
    ret_metrics = None
    if data.relevant_files is not None:
        ret_metrics = retrieval_eval_agent(ret_prompt)
        h, k = calc_metrics(data)
        ret_metrics.hit_at_k = h
        ret_metrics.mrr = k

    return EvalOutput(
        retrieval_metrics=ret_metrics,
        generation_metrics=gen_metrics,
        total_cost=gen_metrics.cost + (ret_metrics.cost if ret_metrics else 0.0),
        total_latency=gen_metrics.latency + (ret_metrics.latency if ret_metrics else 0.0),
        total_inference_time=gen_metrics.inference_time + (ret_metrics.inference_time if ret_metrics else 0.0)
    )