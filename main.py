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
import os
import sys
import uuid
from pathlib import Path

# Load environment variables from .env
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

# Model configuration
MODEL = os.getenv("MODEL", "anthropic:claude-haiku-4-5-20251001")

# Add the directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain_core.messages import HumanMessage, AIMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.status import Status

from deepagents import create_deep_agent, SubAgent

# Import all tools
from src.tools.transactions import get_transactions, get_recent_income
from src.tools.spending import (
    get_spending_summary,
    get_category_spending,
    get_merchant_spending_pattern,
)
from src.tools.savings import (
    get_savings_recommendation,
    calculate_savings_potential,
    transfer_to_savings,
)
from src.tools.accounts import get_accounts, get_recurring_bills
from src.tools.enrichment import enrich_transaction
from src.tools.charts import build_chart_spec

EXAMPLE_DIR = Path(__file__).parent
console = Console()


def create_nova():
    """Create Nova."""

    # Define subagents
    spending_analyst = SubAgent(
        name="spending_analyst",
        description="Deep dive into spending patterns, trends, and comparisons. Use for analyzing spending by category, merchant, or time period.",
        model=MODEL,
        tools=[
            get_transactions,
            get_spending_summary,
            get_category_spending,
            get_merchant_spending_pattern,
            build_chart_spec,
        ],
        system_prompt="""You are a spending analyst. Your job is to analyze spending data and report back.

WORKFLOW:
1. Use your tools to gather the spending data you need
2. Check if the request mentions "chart", "pie", "bar", "line", "graph", or "visualiz" - if so, you MUST call build_chart_spec
3. Respond with your analysis

CRITICAL - CHART RULES:
- If the task mentions ANY chart/graph/visualization request, you MUST call build_chart_spec. This is mandatory.
- NEVER create ASCII art, unicode blocks, or text-based visual representations. Only use build_chart_spec.
- After calling build_chart_spec, include the returned JSON in a ```chartdata block at the END of your response.

CHART TYPE SELECTION:
- "pie": Breakdowns showing proportions (spending by category, by merchant)
- "bar": Comparing discrete categories
- "line": Trends over time
- "area": Cumulative trends over time

WHEN TO USE CHARTS:
- Task mentions "chart", "pie", "bar", "line", "graph", "visualization" → MANDATORY: call build_chart_spec
- Breakdowns with 2+ categories → Use chart
- Trends over time → Use chart

WHEN TO SKIP CHARTS:
- Single value lookups with no chart request → Just return the number
- Simple totals → Just answer directly

RESPONSE FORMAT when chart is created:
1. Your text analysis
2. Then at the very end:
```chartdata
{"chart": <the exact JSON from build_chart_spec>}
```

Keep responses concise and data-driven. Do not use emojis.""",
    )

    savings_advisor = SubAgent(
        name="savings_advisor",
        description="Calculate savings potential, run 'what if' scenarios, and recommend savings amounts. Use for questions about how much to save or what could be saved by changing habits.",
        model=MODEL,
        tools=[
            get_transactions,
            get_recent_income,
            get_recurring_bills,
            get_savings_recommendation,
            calculate_savings_potential,
            build_chart_spec,
        ],
        system_prompt="""You are a savings advisor. Your job is to calculate savings potential and report back.

WORKFLOW:
1. Use your tools to gather income, bills, and spending data as needed
2. Check if the request mentions "chart", "pie", "bar", "line", "graph", or "visualiz" - if so, you MUST call build_chart_spec
3. Respond with your recommendations

CRITICAL - CHART RULES:
- If the task mentions ANY chart/graph/visualization request, you MUST call build_chart_spec. This is mandatory.
- NEVER create ASCII art, unicode blocks, or text-based visual representations. Only use build_chart_spec.
- After calling build_chart_spec, include the returned JSON in a ```chartdata block at the END of your response.

CHART TYPE SELECTION:
- "bar": Comparing savings scenarios or categories
- "pie": Breakdown of where savings come from

WHEN TO USE CHARTS:
- Task mentions "chart", "pie", "bar", "line", "graph", "visualization" → MANDATORY: call build_chart_spec
- Comparing multiple "what if" scenarios → Use chart

WHEN TO SKIP CHARTS:
- Simple savings recommendations → Just provide the numbers
- Single category "what if" questions → Just show the calculation

RESPONSE FORMAT when chart is created:
1. Your text analysis with concrete numbers
2. Then at the very end:
```chartdata
{"chart": <the exact JSON from build_chart_spec>}
```

Include concrete numbers: how much to save, potential savings, monthly and yearly projections.
Be encouraging but realistic. No emojis.""",
    )

    account_manager = SubAgent(
        name="account_manager",
        description="Handle account lookups, check balances, and execute transfers. Use for viewing accounts, checking balances, or moving money to savings.",
        model=MODEL,
        tools=[
            get_accounts,
            get_recurring_bills,
            transfer_to_savings,
        ],
        system_prompt="""You are an account manager. Your job is to handle account inquiries and execute transfers.

1. Use your tools to look up accounts, balances, or bills as needed
2. For transfers, execute them and confirm the result
3. Once complete, respond with the information or confirmation

Do not continue making unnecessary calls - provide your response when ready.
Confirm all actions clearly. No emojis.""",
    )

    return create_deep_agent(
        model=MODEL,
        memory=[str(EXAMPLE_DIR / "AGENTS.md")],
        subagents=[spending_analyst, savings_advisor, account_manager],
        system_prompt="""You are Nova, a personal financial assistant and orchestrator.

CRITICAL RULES:
1. Do not use emojis anywhere in your responses. No emoji characters whatsoever.
2. NEVER create ASCII art, text-based charts, or visual representations using characters. If the user requests a chart/graph and the subagent response contains a ```chartdata block, pass it through exactly. If there's no chart data, just present the information as text/tables - do NOT attempt to draw charts yourself.

You coordinate three specialist subagents to help users with their finances:
- spending_analyst: Analyzes spending patterns, trends, and breakdowns by category or merchant. Can create charts.
- savings_advisor: Calculates savings potential, runs "what if" scenarios, recommends savings amounts. Can create charts.
- account_manager: Looks up account balances, lists bills, and executes transfers.

You MUST delegate all financial queries to the appropriate subagent. You do not have direct access to financial data.

IMPORTANT: When the user asks for a chart or visualization, make sure to include that request when delegating to the subagent (e.g., "create a pie chart showing...").

For complex requests, you may need to delegate to multiple subagents in sequence.

Be conversational, supportive, and actionable in your responses.
Keep responses clean and professional - use markdown formatting.

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
    """Run Nova in interactive chat mode with streaming responses."""
    console.print("\n[bold green]Nova[/bold green] - Personal Financial Assistant")
    console.print("[dim]Type 'quit' to exit[/dim]\n")

    agent = create_nova()
    messages: list = []
    thread_id = f"nova-{uuid.uuid4().hex[:8]}"

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ["quit", "exit", "q"]:
                break

            if not user_input.strip():
                continue

            messages.append(HumanMessage(content=user_input))

            # Stream the response
            response_content = ""
            is_streaming = False
            status: Status | None = None

            # Start with thinking spinner
            status = Status("[bold green]Thinking...", spinner="dots", console=console)
            status.start()

            async for event in agent.astream_events(
                {"messages": messages},
                config={"configurable": {"thread_id": thread_id}},
                version="v2",
            ):
                event_type = event.get("event")

                # When we get streaming tokens from the final response
                if event_type == "on_chat_model_stream":
                    chunk = event.get("data", {}).get("chunk")
                    if chunk and hasattr(chunk, "content") and chunk.content:
                        # Extract text from content (may be string or list of blocks)
                        content = chunk.content
                        if isinstance(content, list):
                            # Extract text from content blocks
                            text = "".join(
                                block.get("text", "")
                                for block in content
                                if isinstance(block, dict)
                                and block.get("type") == "text"
                            )
                        else:
                            text = content

                        if text:
                            # Stop the spinner when we start streaming text
                            if not is_streaming:
                                if status:
                                    status.stop()
                                    status = None
                                console.print()
                                console.print("[bold green]Nova:[/bold green] ", end="")
                                is_streaming = True

                            # Print the token
                            console.print(text, end="")
                            response_content += text

            # Clean up spinner if still running
            if status:
                status.stop()

            # Add newlines after streaming completes
            if is_streaming:
                console.print("\n")

            # Add the complete response to message history
            if response_content:
                messages.append(AIMessage(content=response_content))

        except KeyboardInterrupt:
            if status:
                status.stop()
            break
        except Exception as e:
            if status:
                status.stop()
            console.print(f"\n[red]Error: {e}[/red]")

    console.print("\n[dim]Goodbye![/dim]")


def main() -> None:
    """Main entry point."""
    # Check for query argument
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if args:
        query = " ".join(args)
        asyncio.run(run_query(query))
        return

    # No arguments or -i flag - start interactive mode
    asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
