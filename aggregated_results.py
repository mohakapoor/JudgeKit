import json
import os

def aggregate_results(file_path="test_results.json"):
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON. Make sure it's fully formatted: {e}")
        return

    if not data:
        print("No test cases found in the file.")
        return

    aggregates = {
        "retrieval": {"precision_score": [], "recall_score": [], "hit_at_k": [], "mrr": []},
        "generation": {"faithfulness_score": [], "relevance_score": [], "correctness_score": []},
        "totals": {"total_cost": [], "total_latency": [], "total_inference_time": []}
    }

    for item in data:
        rm = item.get("retrieval_metrics")
        if rm:
            for k in aggregates["retrieval"]:
                if rm.get(k) is not None:
                    aggregates["retrieval"][k].append(rm[k])

        gm = item.get("generation_metrics")
        if gm:
            for k in aggregates["generation"]:
                if gm.get(k) is not None:
                    aggregates["generation"][k].append(gm[k])

        for k in aggregates["totals"]:
            if item.get(k) is not None:
                aggregates["totals"][k].append(item[k])

    print(f"--- Aggregated Results ({len(data)} test cases) ---\n")
    
    print("Retrieval Metrics:")
    for k, v in aggregates["retrieval"].items():
        if v:
            print(f"  Average {k}: {sum(v)/len(v):.4f}")
    
    print("\nGeneration Metrics:")
    for k, v in aggregates["generation"].items():
        if v:
            print(f"  Average {k}: {sum(v)/len(v):.4f}")

    print("\nSystem Performance:")
    for k, v in aggregates["totals"].items():
        if v:
            print(f"  Average {k}: {sum(v)/len(v):.4f} (Total Sum: {sum(v):.4f})")

if __name__ == "__main__":
    aggregate_results()
