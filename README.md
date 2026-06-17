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
ANTHROPIC_API_KEY=your-anthropic-api-key
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=nova
LANGSMITH_TRACING=true
NOVA_CONTEXT_HUB_AGENT=nova
NOVA_CONTEXT_HUB_WORKSPACE=your-workspace-id
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
├── src/                    # Tools and mock data
│   ├── models/
│   ├── tools/
│   └── data/
└── context_hub_demo/       # Notebook walkthrough for Context Hub setup
```

## Memory and skills (Context Hub)

| Path in `nova` | Purpose |
|---|---|
| `AGENTS.md` | Hard rules, delegation policy, tone, and applied skill list. |
| `skills/currency-formatting/SKILL.md` | How to render dollar amounts and percentages. |
| `skills/chart-data-emission/SKILL.md` | When and how to emit `chartdata` blocks. |
| `skills/category-vocabulary/SKILL.md` | Canonical spending-category names and aliases. |

All skills are embedded in the single `nova` agent repo. To edit these files,
open them in the LangSmith Context Hub UI under Context → nova. Engine-proposed
fixes commit directly to the `nova` agent repo once accepted and are picked up
on the next agent invocation, no restart required.

At runtime, Nova mounts this Context Hub repo under `/memories/` with a
`CompositeBackend`. The default backend remains a `StateBackend`, so file paths
outside `/memories/` can still be used as scratchpad state without writing back
to Context Hub.

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
