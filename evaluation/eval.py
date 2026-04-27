# evaluation.py

import time
from agent import run_agent
from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


tool_selection_eval_path = Path("eval_results/tool_selection_eval.txt")
latency_eval_path = Path("eval_results/latency_eval.txt")
response_quality_eval_path = Path("eval_results/response_quality_eval.txt")

# TEST DATASET (you can expand)
test_queries = [
    {"query": "latest AI news", "expected_tool": "web_search"},
    {"query": "recent machine learning papers", "expected_tool": "fetch_arxiv"},
    {"query": "latest AI github repos", "expected_tool": "fetch_ai_repos"},
    {"query": "top AI trends today", "expected_tool": "web_search"},
]



# 1. TOOL SELECTION EVALUATION
def evaluate_tool_selection():
    correct = 0
    total = len(test_queries)

    print("\n Tool Selection Evaluation\n")

    for item in test_queries:
        query = item["query"]
        expected = item["expected_tool"]

        # Run agent (modify agent to return tool used optionally if needed)
        response = run_agent(query, [])

        # Simple heuristic detection (based on keywords in response)
        if "GitHub" in response:
            actual = "fetch_ai_repos"
        elif "Research" in response:
            actual = "fetch_arxiv"
        elif "News" in response:
            actual = "web_search"
        else:
            actual = "none"

        result = expected == actual
        if result:
            correct += 1

        print(f"Query: {query}")
        print(f"Expected: {expected} | Actual: {actual} | {result}\n")

    accuracy = correct / total * 100
    print(f"Tool Selection Accuracy: {accuracy:.2f}%\n")
    return accuracy


# 2. LATENCY EVALUATION
def evaluate_latency():
    print("\n⏱ Latency Evaluation\n")

    times = []

    for item in test_queries:
        query = item["query"]

        start = time.time()
        run_agent(query, [])
        end = time.time()

        latency = end - start
        times.append(latency)

        print(f"{query} → {latency:.2f} sec")

    avg_time = sum(times) / len(times)
    print(f"\n⚡ Average Response Time: {avg_time:.2f} sec\n")
    return avg_time

# 3. RESPONSE QUALITY (LLM JUDGE)
def evaluate_response_quality():
    print("\n Response Quality Evaluation\n")
    
    evaluations = []

    for item in test_queries:
        query = item["query"]

        answer = run_agent(query, [])

        eval_prompt = f"""
        Evaluate the following answer:

        Question: {query}
        Answer: {answer}

        Rate from 1 to 5:
        - Relevance
        - Clarity
        - Completeness

        Give output like:
        Relevance: X
        Clarity: X
        Completeness: X
        """

        eval_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": eval_prompt}]
        )

        evaluations.append(eval_response.choices[0].message.content)
        print(f"\nQuery: {query}")
        print(eval_response.choices[0].message.content)
        print("-" * 50)

    return evaluations


# RUN ALL
if __name__ == "__main__":
    tool_selection_accuracy = evaluate_tool_selection()
    latency_evaluation = evaluate_latency()
    response_quality_evaluation = evaluate_response_quality()
    
    # storing the results in files
    with open(tool_selection_eval_path, "w") as f:
        f.write(f"Tool Selection Accuracy: {tool_selection_accuracy:.2f}%\n")
    with open(latency_eval_path, "w") as f:
        f.write(f"Average Response Time: {latency_evaluation:.2f} sec\n")
    with open(response_quality_eval_path, "w") as f:
        f.write(f"Response Quality Evaluation:\n{response_quality_evaluation}\n")