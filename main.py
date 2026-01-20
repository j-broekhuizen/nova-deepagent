#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "deepagents",
#     "pydantic>=2.0.0",
#     "rich>=13.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Nova - Personal Financial Assistant

A DeepAgent that helps users manage their money through:
- Savings suggestions based on income and bills
- Spending insights and category breakdowns
- "What if" savings potential calculations
- Natural language queries about transactions

Usage:
    uv run main.py
    uv run main.py "How much did I spend on coffee this month?"
    uv run main.py "What if I made coffee at home?"
    uv run main.py -i  # Interactive mode
"""

import asyncio
import sys
from pathlib import Path

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

# Add the demo directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from deepagents import create_deep_agent

# Import all tools
from nova.tools.transactions import get_transactions, get_recent_income
from nova.tools.spending import (
    get_spending_summary,
    get_category_spending,
    get_merchant_spending_pattern,
)
from nova.tools.savings import (
    get_savings_recommendation,
    calculate_savings_potential,
    transfer_to_savings,
)
from nova.tools.accounts import get_accounts, get_recurring_bills
from nova.tools.enrichment import enrich_transaction

EXAMPLE_DIR = Path(__file__).parent
console = Console()


def create_nova():
    """Create the Nova financial assistant agent."""

    # All financial tools
    tools = [
        # Transaction tools
        get_transactions,
        get_recent_income,
        # Spending analysis
        get_spending_summary,
        get_category_spending,
        get_merchant_spending_pattern,
        # Savings tools
        get_savings_recommendation,
        calculate_savings_potential,
        transfer_to_savings,
        # Account tools
        get_accounts,
        get_recurring_bills,
        # Enrichment
        enrich_transaction,
    ]

    return create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        memory=[str(EXAMPLE_DIR / "AGENTS.md")],
        tools=tools,
        system_prompt="""You are Nova, a personal financial assistant.

Your primary capabilities:
1. Analyze spending patterns and provide insights
2. Suggest savings amounts based on income and bills
3. Calculate potential savings from lifestyle changes
4. Answer questions about transactions and balances

Always use the available tools to get accurate data - never make up numbers.
Be conversational, supportive, and actionable in your responses.
Never use emojis in your responses.

When discussing spending categories, these are the valid categories:
- coffee, fast_food, delivery, dining, entertainment
- groceries, transportation, shopping, subscription
- utilities, healthcare, income, transfer, other""",
    )


async def run_query(query: str) -> None:
    """Run a single query through Nova."""
    agent = create_nova()

    console.print(Panel(query, title="You", border_style="blue"))

    with console.status("[bold green]Thinking...", spinner="dots"):
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": "nova-demo"}},
        )

    # Display response
    if result.get("messages"):
        # Find the last AI message
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content and msg.type == "ai":
                console.print(
                    Panel(Markdown(msg.content), title="Nova", border_style="green")
                )
                break


async def interactive_mode() -> None:
    """Run Nova in interactive chat mode."""
    console.print("\n[bold green]Nova[/bold green] - Personal Financial Assistant")
    console.print("[dim]Type 'quit' to exit[/dim]\n")

    agent = create_nova()
    messages: list = []

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ["quit", "exit", "q"]:
                break

            if not user_input.strip():
                continue

            messages.append(HumanMessage(content=user_input))

            with console.status("[bold green]Thinking...", spinner="dots"):
                result = await agent.ainvoke(
                    {"messages": messages},
                    config={"configurable": {"thread_id": "nova-interactive"}},
                )

            if result.get("messages"):
                messages = result["messages"]  # Keep conversation history

                # Find the last AI message
                for msg in reversed(messages):
                    if hasattr(msg, "content") and msg.content and msg.type == "ai":
                        console.print()
                        console.print(
                            Panel(
                                Markdown(msg.content), title="Nova", border_style="green"
                            )
                        )
                        console.print()
                        break

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    console.print("\n[dim]Goodbye![/dim]")


def main() -> None:
    """Main entry point."""
    # Check for interactive mode
    if "--interactive" in sys.argv or "-i" in sys.argv:
        asyncio.run(interactive_mode())
        return

    # Check for query argument
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if args:
        query = " ".join(args)
        asyncio.run(run_query(query))
        return

    # No arguments - show demo menu
    demos = [
        ("Savings suggestion", "My paycheck just came in. How much should I save?"),
        (
            "Spending insight",
            "How much have I spent on dining and entertainment this month?",
        ),
        ("Quick query", "How much did I spend in the last week?"),
        ("Savings potential", "How much could I save by making coffee at home?"),
    ]

    console.print("\n[bold green]Nova[/bold green] - Personal Financial Assistant\n")
    console.print("Example queries:\n")
    for i, (name, query) in enumerate(demos, 1):
        console.print(f"  [bold]{i}.[/bold] {name}")
        console.print(f"     [dim]{query}[/dim]\n")

    console.print("Usage:")
    console.print('  uv run nova.py "your question here"')
    console.print("  uv run nova.py -i  # Interactive mode\n")

    # Run the first demo by default
    console.print("[dim]Running demo: Savings suggestion[/dim]\n")
    asyncio.run(run_query(demos[0][1]))


if __name__ == "__main__":
    main()
