<div align="center">

# JudgeKit
### LLM-as-a-Judge Evaluation Framework for RAG Pipelines

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)](https://fastapi.tiangolo.com/)
[![Pipeline: RAG](https://img.shields.io/badge/Pipeline-RAG-32a852.svg)](#)
[![LLM: Llama 3.3 70B](https://img.shields.io/badge/LLM-Llama_3.3_70B-orange.svg)](#)
[![Provider: Groq](https://img.shields.io/badge/Provider-Groq-black.svg)](#)

[**Full Documentation**](docs/documentation.md)

</div>

---

JudgeKit is an **LLM-as-a-Judge** evaluation framework for scoring Retrieval-Augmented Generation (RAG) pipelines. Powered by Llama 3.3 70B via the Groq API, it evaluates vector retrieval accuracy and generated responses using both semantic LLM reasoning and cross-platform deterministic metrics.

## Core Features
- **Multi-Criteria Scoring**: A 12-dimension semantic checklist for Generation metrics (Faithfulness, Relevance, Correctness). Scores are continuous (0.0 to 1.0).
- **Fact-Based Recall**: Context Recall evaluates essential information units (facts/propositions) rather than simple string entities, preventing artificially inflated scores.


### Evaluated Metrics
- **Retrieval (LLM)**: Context Precision (Chunk-level Signal-to-Noise), Context Recall (Information-unit verification)
- **Generation (LLM)**: Faithfulness (5 checklist criteria), Relevance (3 criteria), Correctness (4 criteria)
- **Deterministic**: Hit@K, Mean Reciprocal Rank (MRR)
- **Observability**: Tracks API Cost, Latency, and Inference Time per request

*For more details, please see the [Full Documentation](docs/documentation.md).*

## Getting Started

### 1. Set Up Environment
Create a `.env` file in the root directory and add API keys:
```env
API_TOKEN=secure-token  #only needed if using the API
GROQ_API_KEY=groq-api-key
```

### 2. Run the CLI
To batch evaluate a dataset of questions and contexts:
```bash
uv run python main.py --input test_responses.json --output test_results.json --sample 5
```

### 3. Run the API Backend
To spin up the FastAPI server and expose the `/judge_all` endpoints for external integration:
```bash
uv run uvicorn api.main:app --reload
```
Once running, navigate to `http://127.0.0.1:8000/docs` (or the configured port) to test the secure endpoints.

## Cost Comparison

Judge_Kit is a simpler alternative to frameworks like RAGAS and uses a lighter model configuration. On a test set of 52 cases (evaluating questions, contexts, responses, and ground truth), a standard RAGAS evaluation using GPT-4o costs approximately **$2.08**. By comparison, running the exact same 52 test cases through Judge_Kit using `llama-3.3-70b-versatile` on Groq cost **$0.1350**.