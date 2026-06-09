---
name: chart-data-emission
description: How and when to emit chart data blocks so the frontend can render charts.
---

# chart-data-emission

The frontend renders charts only when it finds a fenced `chartdata` block
at the end of a response. This skill defines that contract.

## When to emit

- The user (or the delegating agent) asked for a chart, graph, pie, bar,
  line, area, or visualization.
- You called `build_chart_spec` to produce the spec.

If neither is true, do not emit a chart block.

## How to emit

End your response with a fenced block, language `chartdata`, containing
exactly one JSON object with a single `chart` key:

````
```chartdata
{"chart": <the JSON returned by build_chart_spec>}
```
````

## Rules

- The block must be the **last** thing in your response.
- No commentary inside the block, no extra keys, no trailing prose.
- Never inline chart JSON into prose — it belongs in the fenced block.
- Never describe chart data using ASCII art, unicode block characters
  (`█ ▒`), or text-drawn bar/pie/line representations.
- If `build_chart_spec` was not called, do not invent chart JSON. Reply
  in prose instead.
