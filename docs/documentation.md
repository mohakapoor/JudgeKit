# JudgeKit Documentation

## 1. Overview
JudgeKit is an "LLM-as-a-Judge" evaluation framework explicitly designed to score Retrieval-Augmented Generation (RAG) pipelines. It uses a dual-agent architecture powered by Groq (defaulting to Llama 3.3 70B) to independently grade the retrieval engine and the generation engine.

## 2. Architecture
The system is divided into two primary processing pathways:
- **Retrieval Evaluation**: Analyzes the provided contexts against the ground truth to determine if the correct information was successfully retrieved.
- **Generation Evaluation**: Analyzes the LLM's final response against the user's query and the retrieved contexts to ensure accuracy and relevance.

An **Orchestrator** coordinates these two agents sequentially and merges their outputs with deterministic mathematical metrics.

## 3. Evaluation Metrics

### 3.1 LLM-Evaluated Metrics
JudgeKit employs a strict ternary scoring rubric (0.0, 0.5, 1.0) to minimize LLM variance. Before scoring, the model is forced to output a "Chain of Thought" reasoning block to ensure logical consistency.

* **Context Precision (Retrieval)**: Does the retrieved context contain the exact answer?
* **Context Recall (Retrieval)**: Is the retrieved context relevant without unnecessary noise?
* **Faithfulness (Generation)**: Is the generated answer fully supported by the retrieved contexts, or did the model hallucinate?
* **Relevance (Generation)**: Does the generated answer actually address the user's initial query?
* **Correctness (Generation)**: Does the generated response factually match the provided human-curated Ground Truth answer?

### 3.2 Deterministic Metrics
JudgeKit mathematically calculates exact-match retrieval algorithms:
* **Hit@K**: Returns `1.0` if the exact source file (ground truth) is found anywhere in the top-K retrieved contexts, else `0.0`.
* **Mean Reciprocal Rank (MRR)**: Returns `1 / rank` where `rank` is the position (1-indexed) of the correct ground truth file in the retrieved contexts. Returns `0.0` if not found.

## 4. Data Schemas

### 4.1 Batch Input Schema
For CLI evaluations, the framework expects a JSON file (e.g., `test_responses.json`) structured as a dictionary of parallel arrays. Each index across the arrays corresponds to a single evaluation test case.

```json
{
  "question": [
    "What is the capital of France?"
  ],
  "contexts": [
    [
      {
        "text": "Paris is the capital of France.",
        "metadata": {
          "path": "knowledge_base/repos/geography.md",
          "start_line": 10,
          "end_line": 15,
          "and other fields": 0
        }
      }
    ]
  ],
  "responses": [
    "The capital is Paris."
  ],
  "ground_truth": [
    "The capital of France is Paris."
  ]
}
```
The `batch_load_questions` utility dynamically parses this file, converting each parallel index into an `EvalInput` instance.

### 4.2 `EvalInput`
The unified input payload required by all evaluators.
```json
{
  "query": "What is the capital of France?",
  "contexts": [
    "File: geography.md (Lines 10-15)\nContext:\nParis is the capital of France."
  ],
  "response": "The capital is Paris.",
  "ground_truth": "The capital of France is Paris, located in Europe."
}
```

### `EvalOutput`
The final payload containing nested metrics.
```json
{
  "retrieval_metrics": {
    "precision_score": 1.0,
    "precision_reasoning": "...",
    "recall_score": 1.0,
    "recall_reasoning": "...",
    "hit_at_k": 1.0,
    "mrr": 1.0,
    "cost": 0.0001,
    "latency": 0.5,
    "inference_time": 0.4
  },
  "generation_metrics": { 
    "faithfulness_score": 1.0,
    "relevance_score": 1.0,
    "correctness_score": 1.0,
    "cost": 0.0001,
    "latency": 0.6,
    "inference_time": 0.5
  },
  "total_cost": 0.0002,
  "total_latency": 1.0,
  "total_inference_time": 0.8
}
```

## 5. API Reference

The FastAPI backend is protected by an `HTTPBearer` token lock (`API_TOKEN` in `.env`).

### `GET /status`
Returns system status and currently loaded model.

### `POST /judge_retrieval`
Evaluates context precision and recall using the LLM agent.

### `POST /judge_generation`
Evaluates faithfulness and relevance using the LLM agent.

### `POST /judge_deterministic`
Calculates Hit@K and MRR purely mathematically (no LLM cost).

### `POST /judge_all`
The primary endpoint. Runs the orchestrator and returns a full `EvalOutput` object.
