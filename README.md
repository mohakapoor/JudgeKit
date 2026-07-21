# JudgeKit

JudgeKit is an LLM-as-a-Judge evaluation framework for scoring Retrieval-Augmented Generation (RAG) pipelines. 

Using Llama 3 via the Groq API, JudgeKit implements a dual-agent architecture to evaluate the retrieval engine and the generation engine independently.

## Features
- **Dual-Agent Architecture**: Implements two evaluators (`eval_retrieval` and `eval_generation`).
- **RAG Triad Metrics**: Evaluates Context Precision, Context Recall, Faithfulness, and Relevance.
- **Ternary Scoring Rubric**: Utilizes a 0.0, 0.5, and 1.0 scoring system to minimize evaluation variance.
- **Chain of Thought (CoT)**: Enforces reasoning generation prior to scoring.
- **Structured JSON Output**: Guarantees parseable JSON output for all evaluations.
- **Observability Metrics**: Calculates and logs API cost, end-to-end latency, and inference time per request.
- **Rate Limiting**: Includes request throttling to comply with API limits.

## Project Structure
- `main.py`: The entry point that loads data, iterates through the evaluation dataset, and outputs results.
- `config.py`: Contains system prompts, rubrics, and model configuration parameters.
- `src/agent.py`: Handles API requests and JSON response parsing.
- `src/prompt_builder.py`: Formats the evaluation context and query for the model.
- `src/utils.py`: Provides data models, file I/O operations, and cost calculation logic.

## Setup
1. Clone the repository.
2. Install the `uv` package manager if not already installed.
3. Install dependencies:
   ```bash
   uv pip install groq python-dotenv
   ```
4. Create a `.env` file in the root directory and add the required environment variable:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Usage
Run the pipeline to evaluate the dataset in `generated_responses.json`:

```bash
uv run main.py
```

The script processes the specified number of test cases and outputs a structured JSON evaluation to stdout.
