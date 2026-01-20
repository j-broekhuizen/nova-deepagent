# Nova Demo Scenarios

Different demo paths for showcasing Nova. Each demo is designed for different audiences and time constraints.

---

## Demo 1: The 30-Second Wow (Single Query)

**Audience**: Quick showcase, hallway conversation
**Time**: 30 seconds

Pick ONE of these single-shot queries:

```bash
# Paycheck just landed - shows proactive savings suggestion
uv run main.py "My paycheck just came in"

# Spending breakdown - shows data analysis
uv run main.py "How much have I spent on dining and delivery this month?"

# Habit analysis with actionable savings
uv run main.py "How much could I save if I made coffee at home?"
```

**What it shows**: Agent calling tools, getting real data, giving actionable advice

---

## Demo 2: The Payday Flow (2-3 minutes)

**Audience**: Product demo, stakeholder presentation
**Time**: 2-3 minutes
**Mode**: Interactive (`uv run main.py -i`)

### Script

```
You: My paycheck just came in. How much should I save?

[Nova analyzes income, bills, recommends amount]

You: What bills do I have coming up?

[Nova lists recurring bills]

You: Ok, transfer $200 to savings

[Nova executes transfer, confirms new balances]

You: What's my savings balance now?

[Nova shows updated balance]
```

**What it shows**:
- Multi-turn conversation with memory
- Tool orchestration (income → bills → recommendation → transfer)
- Stateful actions (balance updates persist)
- Conversational UX

---

## Demo 3: The Spending Deep Dive (2-3 minutes)

**Audience**: Product demo, showing analytical capabilities
**Time**: 2-3 minutes
**Mode**: Interactive

### Script

```
You: Where is my money going?

[Nova shows category breakdown]

You: Tell me more about my dining spending

[Nova breaks down dining by merchant: Uber Eats, Starbucks, McDonald's]

You: How often am I going to Starbucks?

[Nova shows pattern: 4x/week on weekdays, busiest day, avg amount]

You: What if I cut that in half?

[Nova calculates: current spend, new spend, monthly/yearly savings]
```

**What it shows**:
- Progressive drill-down (overview → category → merchant → pattern)
- "What if" scenario analysis
- Natural follow-up questions

---

## Demo 4: The Coffee Savings Story (90 seconds)

**Audience**: Focused demo on habit change / savings potential
**Time**: 90 seconds
**Mode**: Interactive

### Script

```
You: How much am I spending on coffee?

[Nova shows Starbucks spending: ~$215/month, 30+ visits]

You: What if I made coffee at home during the week?

[Nova calculates: $0.50/cup at home, ~$200/month savings, ~$2,400/year]

You: That's a lot! What else could I cut back on?

[Nova suggests looking at delivery spending - another big category]
```

**What it shows**:
- Habit analysis
- Concrete savings calculations
- Proactive suggestions

---

## Demo 5: The Full Financial Checkup (5 minutes)

**Audience**: Comprehensive product demo, investor pitch
**Time**: 5 minutes
**Mode**: Interactive

### Script

```
You: Give me a financial health check

[Nova shows accounts, balances, net worth]

You: How much did I spend last month?

[Nova shows total + category breakdown]

You: That seems high. What are my biggest spending categories?

[Nova highlights: delivery, coffee, shopping with specific amounts]

You: How much could I realistically save each month?

[Nova analyzes habits, suggests $300-400/month through small changes]

You: Ok let's start. Transfer $200 to savings.

[Nova executes transfer]

You: Set a reminder to check my spending next week

[Nova acknowledges - shows conversational capability even without that tool]
```

**What it shows**:
- Full financial picture
- Data-driven insights
- Actionable recommendations
- Multi-step workflows

---

## Demo 6: Quick Q&A Rapid Fire (60 seconds)

**Audience**: Showing breadth of capabilities quickly
**Time**: 60 seconds
**Mode**: Interactive - rapid questions

### Script

```
You: How much did I spend last week?
[Quick answer: $347]

You: What's my checking balance?
[Quick answer: $2,915]

You: How much are my monthly bills?
[Quick answer: $2,237]

You: Top 3 places I spend money?
[Quick answer: Uber Eats, Starbucks, Whole Foods]
```

**What it shows**:
- Fast, accurate responses
- Different query types
- Natural language understanding

---

## Key Talking Points

### DeepAgents Architecture
- "Nova is built on DeepAgents - tools are just Python functions"
- "The agent decides which tools to call based on the question"
- "All the financial data comes from tools, not hardcoded responses"

### LangSmith Tracing
- Show the trace in LangSmith after a query
- Point out: tool calls, reasoning, response generation

### Customization
- "The personality is defined in AGENTS.md - easy to customize"
- "Adding new tools is just writing Python functions with @tool decorator"
- "Mock data can be swapped for real banking APIs (Plaid, etc.)"

---

## Demo Tips

1. **Start interactive mode before the demo** - avoids cold start
2. **Use LangSmith** - have it open in another tab to show traces
3. **Have backup queries ready** - in case something goes wrong
4. **Show the spinner** - "Thinking..." shows the agent is working
5. **End with an action** - transfer to savings is satisfying

---

## Queries That Work Well

### Guaranteed crowd-pleasers:
- "My paycheck just came in"
- "How much could I save making coffee at home?"
- "Where is my money going?"

### Good follow-ups:
- "Tell me more about [category]"
- "Transfer $X to savings"
- "What if I cut that in half?"

### Avoid (can be slow or verbose):
- Very open-ended: "Help me with my finances"
- Multi-part: "Show me X and Y and Z" (better as separate questions)
