"""Root agent must delegate financial questions instead of computing them."""

import sys
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage, HumanMessage

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import create_nova


def _has_task_call_before_final_ai(messages) -> bool:
    """Return True if some AI message issues a `task` tool call before the last AI."""
    last_ai_idx = None
    for i in range(len(messages) - 1, -1, -1):
        msg = messages[i]
        if isinstance(msg, AIMessage) and getattr(msg, "content", None):
            last_ai_idx = i
            break
    if last_ai_idx is None:
        return False
    for msg in messages[:last_ai_idx]:
        tool_calls = getattr(msg, "tool_calls", None) or []
        for call in tool_calls:
            name = call.get("name") if isinstance(call, dict) else getattr(call, "name", None)
            if name == "task":
                return True
    return False


@pytest.mark.asyncio
async def test_what_if_coffee_savings_delegates():
    """Trivial arithmetic ($100/mo coffee → yearly) must still go through `task`."""
    agent = create_nova()
    result = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="If I spend $100 monthly on coffee, how much could I save yearly?"
                )
            ]
        },
        config={"configurable": {"thread_id": "test-delegation-coffee"}},
    )

    messages = result.get("messages", [])
    assert _has_task_call_before_final_ai(messages), (
        "Root agent answered without delegating via `task` — it must not compute "
        "dollar amounts from the user's input directly."
    )
