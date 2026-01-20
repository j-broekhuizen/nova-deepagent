# Nova - Personal Financial Assistant

Nova is a deep agent that helps users manage their finances through natural conversation.

## Features

- **Savings Suggestions**: "Your paycheck just came in, want to save some?"
- **Spending Insights**: "You've spent $878 on dining this month. Top 3: Uber Eats, Starbucks, McDonald's"
- **Chat Queries**: "How much have I spent in the last week?" → $347.23
- **Savings Potential**: "How much could I save making coffee at home?" → $263/month

## Setup

```bash
cd demos/nova

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
```

## Architecture

```
nova/
├── main.py                 # Main entry point
├── AGENTS.md               # Nova's personality and guidelines
├── pyproject.toml          # Dependencies
├── src/                    # Main package
│   ├── models/
│   │   ├── transaction.py  # Transaction, MerchantInfo, Category
│   │   └── account.py      # Account, RecurringBill
│   ├── tools/
│   │   ├── transactions.py # get_transactions, get_recent_income
│   │   ├── spending.py     # spending summaries and patterns
│   │   ├── savings.py      # recommendations and transfers
│   │   ├── accounts.py     # balances and bills
│   │   └── enrichment.py   # categorize transactions
│   └── data/
│       └── mock_data.py    # Realistic transaction generator
└── tests/
```

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

## Mock Data

Nova uses generated mock data for demonstration:
- 90 days of realistic transactions
- Bi-weekly paychecks ($3,250)
- Common merchants: Starbucks, Uber Eats, McDonald's, etc.
- Recurring bills: Rent, utilities, subscriptions

The data is designed to produce realistic spending patterns that match common scenarios.

## Customization

Edit `AGENTS.md` to customize Nova's personality and response style.
