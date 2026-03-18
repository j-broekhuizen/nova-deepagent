"""
Nova Online Evaluator Prompts

Paste these prompts into the LangSmith UI when creating LLM-as-judge online evaluators
for the Nova tracing project.

Variables available in LangSmith prompt templates:
  {input}   - the user's input to the run
  {output}  - the final output of the run
"""

# ---------------------------------------------------------------------------
# 1. Rule Compliance
# ---------------------------------------------------------------------------
RULE_COMPLIANCE_PROMPT = """
You are evaluating whether a financial assistant's response follows strict formatting rules.

Assistant response:
{output}

The assistant must follow these rules:
- No emojis of any kind
- No ASCII art, box-drawing characters, or text-based visual representations (e.g. bars made of █ or |)

Score 1 (PASS) if the response contains no violations.
Score 0 (FAIL) if the response contains any emojis or ASCII art.

Return only a JSON object:
{"score": 1, "reasoning": "brief explanation"}
"""

# ---------------------------------------------------------------------------
# 2. No Hallucinated Numbers
# ---------------------------------------------------------------------------
NO_HALLUCINATED_NUMBERS_PROMPT = """
You are evaluating whether a financial assistant invented numbers that were not grounded in the user's actual data.

User question:
{input}

Assistant response:
{output}

Check every specific dollar amount, percentage, and count in the response. A number is hallucinated if:
- It is a precise financial figure (e.g. $2,915.67, 14 transactions, 83%) that could not be inferred logically
- It appears to be fabricated rather than derived from real data

Score 1 (PASS) if all specific figures appear reasonable and consistent with each other.
Score 0 (FAIL) if any figure appears to be made up, contradictory, or suspiciously precise without basis.

Return only a JSON object:
{"score": 1, "reasoning": "brief explanation"}
"""

# ---------------------------------------------------------------------------
# 3. Subagent Routing
# ---------------------------------------------------------------------------
SUBAGENT_ROUTING_PROMPT = """
You are evaluating whether a financial assistant routed a user query to the correct specialist.

Nova has three specialists:
- account_manager:  account balances, account details, transfers, recurring bills
- spending_analyst: spending breakdowns, category/merchant analysis, trends over time
- savings_advisor:  savings recommendations, "what if" scenarios, savings potential

User question:
{input}

Assistant response:
{output}

Based on the question, determine which specialist(s) should have been called, then assess whether the
response reflects the correct specialist was used (e.g. correct data, correct framing, correct capabilities).

Score 1 (PASS) if the response reflects correct routing.
Score 0 (FAIL) if the response reflects the wrong specialist was used (e.g. savings framing on a balance question).

Return only a JSON object:
{"score": 1, "reasoning": "brief explanation"}
"""
