import json
from config import PATH


def build_question_prompt(idx: int):
    with open(PATH,"r",encoding="utf-8") as f:
        data = json.load(f)
        ques = data["question"][idx]
        contexts = data["contexts"][idx]
        ground_truth = data["ground_truth"][idx]
        response = data["responses"][idx][0]["text"]

        prompt = f"""Query: "{ques}"

        LLM Answer: "{response}"

        Context: {contexts}

        Ground Truth:
        {ground_truth}"""

        return prompt
        
