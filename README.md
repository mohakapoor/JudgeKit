# JudgeKit

JudgeKit is a fast, lightweight LLM-as-a-Judge evaluation framework for scoring Retrieval-Augmented Generation (RAG) pipelines. Powered by Llama 3.3 70B via the Groq API, it evaluates vector retrieval accuracy and generated responses using both LLM reasoning and deterministic metrics.

## Getting Started

### 1. Set Up Environment
Create a `.env` file in the root directory and add your API keys:
```env
API_TOKEN=your-secure-token-for-fastapi  #only needed if you want to use the API
GROQ_API_KEY=your-groq-api-key
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
Once running, navigate to `http://127.0.0.1:8000/docs` (or your configured port) to test the secure endpoints.