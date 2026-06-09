# context-hub/ — local backup of Context Hub repos

**This directory is NOT the runtime source of truth for Nova's memory or skills.**

At runtime, `main.py` pulls the `nova` agent and its 3 linked skills directly
from LangSmith Context Hub via `ContextHubBackend` (see `_build_hub_backend()`).
The Hub identifier and workspace are configured at the top of `main.py`:

```python
HUB_AGENT_NAME = "nova"
HUB_WORKSPACE_ID = "4015447c-43ab-4414-8539-633d4cb47217"  # Jake's Workspace
```

This directory exists for two purposes:

1. **Source files for the initial push.** `scripts/link_skills.py` reads
   `nova/AGENTS.md`, `nova/tools.json`, and `nova/config.json` from here when
   re-pushing the agent manifest with linked SkillEntry references.

2. **Documentation / human review.** A readable copy of every skill and the
   agent prompt, so reviewers can see what Nova currently runs without
   logging into LangSmith.

If you edit any of these files, push the change to Context Hub via:

```bash
# For an agent re-push (e.g., updated AGENTS.md):
uv run scripts/link_skills.py

# For a skill update:
source ~/.zshrc
langsmith hub push <skill-name> \
  --type skill \
  --dir context-hub/<skill-name> \
  --workspace 4015447c-43ab-4414-8539-633d4cb47217 \
  --api-key "$LANGSMITH_API_KEY_CORP"
```

Nova will pick up the new commit on the next agent invocation (no restart
needed; `ContextHubBackend` caches per instance, but a fresh agent is created
each `create_nova()` call).
