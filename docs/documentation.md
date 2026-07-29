# JudgeKit v2.0 Documentation

## 1. Overview
JudgeKit is an "LLM-as-a-Judge" evaluation framework explicitly designed to score Retrieval-Augmented Generation (RAG) pipelines. The core idea of JudgeKit is to extract the most accurate, granular, graded score possible (rather than relying on simple yes/no outputs), while keeping inference costs exceptionally low. 

It uses a dual-agent architecture powered by Groq (defaulting to Llama 3.3 70B) to independently grade the retrieval system and the generation system. *(Note: The model can be swapped to Llama 3.1 8B Instant 128k for even cheaper inference.)*

## 2. Architecture
The system is divided into two primary processing pathways:
- **Retrieval Evaluation**: Analyzes the retrieved chunks for signal-to-noise ratio, and verifies if the context contains the essential facts required to answer the query.
- **Generation Evaluation**: Analyzes the LLM's final response against the user's query and the retrieved contexts using a multi-criteria semantic checklist.

An **Orchestrator** coordinates these two agents and merges their outputs with deterministic mathematical metrics, handling edge cases such as null-set queries where appropriate.

## 3. Evaluation Metrics

### 3.1 LLM-Evaluated Metrics
JudgeKit abandons subjective grading in favor of structured, granular scoring. The model evaluates specific questions, assigning 1.0 (Yes), 0.5 (Partial), 0.0 (No), or `null` (N/A) to each. The scores are dynamically averaged, filtering out N/A criteria, to produce a final continuous score between 0.0 and 1.0.

* **Context Precision (Retrieval)**: Evaluates exactly 5 retrieved chunks individually. Scores each chunk on how useful it is for answering the query.
* **Context Recall (Retrieval)**: Fact-based verification. The LLM extracts independent information units (facts/propositions) from the Ground Truth, and scores whether the context provides enough evidence to establish each fact.
* **Faithfulness (Generation)**: A 5-point checklist verifying that the response is grounded in the provided context (e.g., no outside knowledge, numbers/dates supported).
* **Relevance (Generation)**: A 3-point checklist ensuring the response directly addresses the query without excessive rambling.
* **Correctness (Generation)**: A 4-point checklist verifying the response matches the Ground Truth without introducing material falsehoods.

### 3.2 Deterministic Metrics
JudgeKit calculates exact-match retrieval algorithms using cross-platform `pathlib` logic.
* **Hit@K**: Returns `1.0` if a file in the dataset's `relevant_files` list is found in the retrieved contexts, else `0.0`.
* **Mean Reciprocal Rank (MRR)**: Returns `1 / rank` where `rank` is the position (1-indexed) of the first correctly retrieved file. Returns `0.0` if not found.
* **Null-Set Handling**: If the query is intentionally out-of-scope and `relevant_files` is an empty list `[]`, Hit@K and MRR return `null` (N/A) so the retriever is not unfairly penalized.

## 4. Data Schemas

### 4.1 Batch Input Schema
For CLI evaluations, the framework expects a JSON file (e.g., `test_responses.json`) structured as a dictionary of parallel arrays.

```json
{
  "question": [
    "Where is the CaptchaDataset defined?"
  ],
  "contexts": [
    [
      {
        "text": "class CaptchaDataset(Dataset): ...",
        "metadata": {
          "path": "knowledge_base/repos/CaptchaOCR/src/captcha_dataset.py",
          "start_line": 10,
          "end_line": 15
        }
      }
    ]
  ],
  "answer": [
    "It is defined in CaptchaOCR/src/captcha_dataset.py"
  ],
  "ground_truth": [
    "CaptchaDataset is defined in src/captcha_dataset.py."
  ],
  "relevant_files": [
    [
      "CaptchaOCR/src/captcha_dataset.py"
    ]
  ]
}
```

### 4.2 `EvalInput`
The unified Python dataclass payload required by all evaluators.
```json
{
  "query": "Where is the CaptchaDataset defined?",
  "contexts": [
    "File: CaptchaOCR/src/captcha_dataset.py (Lines 10-15)\nContext:\nclass CaptchaDataset..."
  ],
  "response": "It is defined in CaptchaOCR/src/captcha_dataset.py",
  "ground_truth": "CaptchaDataset is defined in src/captcha_dataset.py.",
  "relevant_files": [
    "CaptchaOCR/src/captcha_dataset.py"
  ]
}
```

### 4.3 `EvalOutput`
The final payload containing nested metrics.
```json
{
  "retrieval_metrics": {
    "precision_score": 0.8,
    "precision_reasoning": ["Chunk 1 is useful...", "..."],
    "recall_score": 1.0,
    "recall_reasoning": ["Fact 1 is established...", "..."],
    "hit_at_k": 1.0,
    "mrr": 1.0,
    "cost": 0.0001,
    "latency": 0.5,
    "inference_time": 0.4
  },
  "generation_metrics": { 
    "faithfulness_score": 1.0,
    "faithfulness_reasoning": ["..."],
    "relevance_score": 1.0,
    "relevance_reasoning": ["..."],
    "correctness_score": 1.0,
    "correctness_reasoning": ["..."],
    "cost": 0.0001,
    "latency": 0.6,
    "inference_time": 0.5
  },
  "total_cost": 0.0002,
  "total_latency": 1.1,
  "total_inference_time": 0.9
}
```

## 5. API Reference

The FastAPI backend is protected by an `HTTPBearer` token lock (`API_TOKEN` in `.env`).

### `GET /status`
Returns system status and currently loaded model.

### `POST /judge_retrieval`
Evaluates context precision and recall using the LLM agent.

### `POST /judge_generation`
Evaluates faithfulness, relevance, and correctness using the LLM agent.

### `POST /judge_deterministic`
Calculates Hit@K and MRR using the cross-platform path logic.

### `POST /judge_all`
The primary endpoint. Runs the orchestrator and returns a full `EvalOutput` object.

## 6. Future Improvements & Roadmap
These are the current limitations discovered in the system that I plan to fix in future updates. Feel free to contribute if you want to tackle any of them:

### 6.1 Dynamic Schema Validation (Type Safety)
* **Vulnerability**: The pipeline assumes the LLM will output floats inside its JSON arrays, allowing `sum(p_scores)` to execute blindly. If the LLM hallucinates strings (`["1.0"]`) or booleans, the script crashes with a `TypeError`.
* **Improvement**: Integrate typed `Pydantic` models (via `instructor` or native structured outputs) to enforce schema shapes and guarantee type-safety *before* the data touches the deterministic math.

### 6.2 Asynchronous Execution Pipeline
* **Vulnerability**: The pipeline runs sequentially with hardcoded sleep timers (`time.sleep(6)`), making the evaluation of datasets slow.
* **Improvement**: Transition to a fully concurrent `asyncio` pipeline utilizing token-bucket rate limiters to saturate API quotas safely, maximizing throughput.

### 6.3 De-Coupled Metric Agents
* **Vulnerability**: Generation metrics are currently "clubbed" into a single LLM prompt, risking "context pollution" where the LLM's reasoning for Relevance accidentally bleeds into its score for Faithfulness.
* **Improvement**: Break these out into isolated micro-agents (e.g., a dedicated `FaithfulnessAgent`) to guarantee independent scoring and reduce cross-contamination.


### Aggregated Results on my Test case (52 test cases)

After running `main.py`, Judge_Kit automatically runs `aggregated_results.py` to give you a breakdown like this:

```text
--- Aggregated Results (52 test cases) ---

Retrieval Metrics:
  Average precision_score: 0.4596
  Average recall_score: 0.4835
  Average hit_at_k: 0.7447
  Average mrr: 0.4691

Generation Metrics:
  Average faithfulness_score: 0.8942
  Average relevance_score: 0.8686
  Average correctness_score: 0.8077

System Performance:
  Average total_cost: 0.0026 (Total Sum: 0.1350)
  Average total_latency: 4.3361 (Total Sum: 225.4774)
  Average total_inference_time: 2.3116 (Total Sum: 120.2013)
```
