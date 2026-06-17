# Context Hub Demo

This folder contains the notebook walkthrough for building Nova with LangSmith
Context Hub and DeepAgents.

## Environment

Set these variables before running `demo.ipynb`:

```bash
ANTHROPIC_API_KEY=your-anthropic-api-key
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=nova-context-hub-scene3
NOVA_CONTEXT_HUB_AGENT=nova
NOVA_CONTEXT_HUB_WORKSPACE=your-workspace-id
```

If you keep your LangSmith key in `LANGSMITH_API_KEY_CORP`, the notebook will
copy it into `LANGSMITH_API_KEY` for the demo session.

## Flow

Run the notebook cells top to bottom. It starts with a basic `StateBackend`,
inspects the `nova` Context Hub repo, then swaps Nova to a `CompositeBackend`
that mounts Context Hub under `/memories/` while leaving `StateBackend` as the
scratchpad for other file paths.
