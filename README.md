# Nova - Personal Financial Assistant

Nova is a deep agent that helps users manage their finances through natural
conversation. Its agent instructions and skills are versioned in **LangSmith
Context Hub** — this repository contains only the runtime code.

## Features

- **Savings Suggestions**: "Your paycheck just came in, want to save some?"
- **Spending Insights**: "You've spent $878 on dining this month. Top 3: Uber Eats, Starbucks, McDonald's"
- **Chat Queries**: "How much have I spent in the last week?" → $347.23
- **Savings Potential**: "How much could I save making coffee at home?" → $263/month

## Setup

```bash
cd nova

# Copy the example env file and add your keys
cp .env.example .env
```

Edit `.env` with your API keys:
```
ANTHROPIC_API_KEY=sk-ant-...
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=nova
LANGSMITH_TRACING=true
```

## Usage

```bash
# Single query
uv run main.py "your question here"

# Interactive mode
uv run main.py -i

# Run via langgraph dev + frontend
langgraph dev                                    # backend on :2024
cd frontend && npm run dev                       # frontend on :5174
```

## Architecture

Nova's runtime code lives in this repo. Its **memory and skills are pulled
from Context Hub** at every agent invocation via `ContextHubBackend` —
nothing about the agent's behavior is stored in this repo.

```
nova/
├── main.py                 # Entry point; builds the agent against Context Hub
├── graph.py                # LangGraph export for `langgraph dev`
├── pyproject.toml          # Python dependencies
├── frontend/               # React UI for `langgraph dev`
├── scripts/                # Eval helpers (test question runners)
├── src/                    # Tools and mock data
│   ├── models/
│   ├── tools/
│   └── data/
└── tests/
```

## Memory and skills (Context Hub)

| Repo | Type | Purpose |
|---|---|---|
| `nova` | agent | Top-level manifest. Contains `AGENTS.md` (hard rules + delegation policy) and three `SkillEntry` links to the skills below. |
| `currency-formatting` | skill | How to render dollar amounts and percentages. |
| `chart-data-emission` | skill | When and how to emit `chartdata` blocks. |
| `category-vocabulary` | skill | Canonical spending-category names and aliases. |

The skill links are **unpinned** — they auto-resolve to the latest skill commit.
This means a fix proposed by LangSmith Engine to a skill is picked up on the
next agent invocation, no restart required.

To edit these files, open them in the LangSmith Context Hub UI (Context →
nova, or any of the skill repos). Engine-proposed fixes commit directly to
Context Hub once accepted.

## Tools

| Tool                            | Description                     |
| ------------------------------- | ------------------------------- |
| `get_transactions`              | Query transactions with filters |
| `get_recent_income`             | Find recent paychecks           |
| `get_spending_summary`          | Aggregate by category/merchant  |
| `get_category_spending`         | Deep dive into categories       |
| `get_merchant_spending_pattern` | Analyze habits                  |
| `get_savings_recommendation`    | Calculate safe-to-save amount   |
| `calculate_savings_potential`   | "What if" scenarios             |
| `transfer_to_savings`           | Execute transfers               |
| `get_accounts`                  | List accounts and balances      |
| `get_recurring_bills`           | List monthly bills              |
| `enrich_transaction`            | Categorize raw descriptions     |
| `build_chart_spec`              | Build chart specs for the UI    |

## Mock Data

Nova uses generated mock data for demonstration:
- 90 days of realistic transactions
- Bi-weekly paychecks ($3,250)
- Common merchants: Starbucks, Uber Eats, McDonald's, etc.
- Recurring bills: Rent, utilities, subscriptions

The data is designed to produce realistic spending patterns that match common scenarios.
