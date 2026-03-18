#!/usr/bin/env python3
"""
Nova Agent Evaluation Experiment

Tests Nova agent outputs against reference outputs using an LLM-as-judge evaluator.

Usage:
    uv run evals/experiment.py
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langsmith import aevaluate
from langsmith.evaluation import run_evaluator

# Load environment variables from project root
load_dotenv(Path(__file__).parent.parent / ".env", override=True)

# Make project root importable
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Nova agent
from main import create_nova

# Configuration
DATASET_NAME = "simple-balance-dataset"
MODEL = os.getenv("MODEL", "anthropic:claude-haiku-4-5-20251001")


async def run_nova_agent(inputs: dict) -> dict:
    """
    Target function that runs Nova agent on a question.

    Args:
        inputs: Dictionary with 'question' key

    Returns:
        Dictionary with agent's response
    """
    question = inputs["question"]

    # Create agent and run query
    agent = create_nova()

    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=question)]},
        config={"configurable": {"thread_id": "evaluation-run"}},
    )

    # Extract the last AI message
    output = ""
    if result.get("messages"):
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content and msg.type == "ai":
                output = msg.content
                break

    return {"output": output}


@run_evaluator
def correctness_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """
    LLM-as-judge evaluator for correctness.

    Compares the agent's output against the reference output to assess
    if the information provided is factually correct.

    Args:
        outputs: Dictionary with 'output' key containing agent's response
        reference_outputs: Dictionary with 'balance' key containing reference answer

    Returns:
        Dictionary with score (0 or 1) and comment
    """
    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)

    agent_output = outputs.get("output", "")
    reference = reference_outputs.get("balance", "")

    prompt = f"""You are evaluating the correctness of an AI agent's response against a reference output.

Reference Output (Ground Truth): {reference}

Agent's Actual Output: {agent_output}

Your task is to evaluate if the agent's output is CORRECT compared to the reference output.

Scoring Criteria:
- Score 1 (CORRECT): The agent's output contains the same key information as the reference output. Minor wording differences are acceptable if the facts match.
- Score 0 (INCORRECT): The agent's output contains different facts, wrong numbers, or is missing critical information compared to the reference.

Key considerations:
1. Focus on factual accuracy (numbers, categories, amounts, account types)
2. Allow for different phrasing if the meaning is the same
3. Check that all critical information from the reference is present
4. Additional helpful context in the agent's output is fine as long as core facts match

Return your evaluation as a JSON object with this exact format:
{{
    "score": 1,
    "reasoning": "Brief explanation of why the output is correct or incorrect"
}}

Respond with ONLY the JSON object, no other text."""

    response = llm.invoke(prompt)

    import json
    import re

    try:
        content = response.content.strip()
        content = re.sub(r"^```json\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        result = json.loads(content)
        return {
            "key": "correctness",
            "score": result.get("score", 0),
            "comment": result.get("reasoning", ""),
        }
    except json.JSONDecodeError:
        return {
            "key": "correctness",
            "score": 0,
            "comment": f"Failed to parse LLM response: {response.content}",
        }


async def main():
    """Run the evaluation experiment."""

    print("\n" + "=" * 60)
    print("Nova Agent Correctness Evaluation Experiment")
    print("=" * 60 + "\n")

    print(f"Using dataset: {DATASET_NAME}")
    print(f"Model: {MODEL}")
    print("-" * 60 + "\n")

    results = await aevaluate(
        run_nova_agent,
        data=DATASET_NAME,
        evaluators=[correctness_evaluator],
        experiment_prefix="nova-correctness-experiment",
    )

    print("\n" + "=" * 60)
    print("Experiment Complete!")
    print("=" * 60)
    print(f"\nResults: {results}")
    print(f"\nView detailed results at: https://smith.langchain.com")


if __name__ == "__main__":
    asyncio.run(main())
