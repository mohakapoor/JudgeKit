# Project Plan: JudgeKit (Two-Agent Evaluator)

This is your roadmap to building **JudgeKit** from scratch. Following our discussions, this plan outlines the exact architecture, the files you need to write, and the step-by-step process you should follow to implement it yourself. 

## The Architecture
You will have 3 main Python files in your project:
1. `prompt_builder.py` *(The Brains: Stores the logic for how we talk to the LLM)*
2. `agent.py` *(The Engine: Handles the Groq API calls and parses the JSON)*
3. `main.py` *(The Orchestrator: Loads your JSON, loops through the data, and runs the agents)*

---

## Phase 1: Build the Prompts (`prompt_builder.py`)
This is where you should start. Your goal is to write two functions that return formatted strings.

### Tasks
- [ ] Create `prompt_builder.py`.
- [ ] Write a function: `build_retrieval_prompt(query, contexts, ground_truth)`.
  - **Goal:** This is for Agent 1 (Context Precision & Recall).
  - **Instructions to include in prompt:** Tell the LLM to output JSON `{"reasoning": "...", "precision_score": x, "recall_score": y}`. Force it to write the reasoning first!
  - **Rubric:** Provide a simple 0 or 1 scale for precision (was the context relevant?) and recall (did the context contain the ground truth?).
- [ ] Write a function: `build_generation_prompt(query, contexts, answer)`.
  - **Goal:** This is for Agent 2 (Faithfulness & Relevancy).
  - **Instructions to include in prompt:** Tell the LLM to output JSON `{"reasoning": "...", "faithfulness_score": x, "relevancy_score": y}`.
  - **Rubric:** Provide a simple 0 or 1 scale for faithfulness (no hallucinations) and relevancy (answered the query).

> **Tip:** Use Python f-strings to inject the function arguments cleanly into your prompt text!

---

## Phase 2: Build the Agent Engine (`agent.py`)
Once you have your prompts, you need to update `agent.py` to use them.

### Tasks
- [ ] Import your new builder functions: `from prompt_builder import build_retrieval_prompt, build_generation_prompt`.
- [ ] Write a function: `evaluate_retrieval(query, contexts, ground_truth)`.
  - Inside, call `build_retrieval_prompt`.
  - Send it to the Groq API (keep `temperature=0.0`).
  - *Bonus:* Look up how to use `response_format={"type": "json_object"}` in the Groq API to guarantee it returns JSON!
  - Return the parsed JSON dictionary.
- [ ] Write a function: `evaluate_generation(query, contexts, answer)`.
  - Do the exact same thing, but use `build_generation_prompt`.

---

## Phase 3: The Orchestrator (`main.py`)
Now you tie it all together and run it on your data!

### Tasks
- [ ] Import your evaluation functions from `agent.py`.
- [ ] Import `json` and load your `generated_responses.json` file.
- [ ] Write a loop to iterate through the first 5 questions (e.g., `for i in range(5):`).
- [ ] Extract the specific `query`, `contexts`, `answer`, and `ground_truth` for that index.
- [ ] Call `evaluate_retrieval()` and `evaluate_generation()` for that index.
- [ ] Print out the results beautifully to the terminal!

> **Note:** Because you are only doing the first 5 questions, you can just print the results to the terminal for now. Later, we can add logic to save the results back into a new JSON file.
