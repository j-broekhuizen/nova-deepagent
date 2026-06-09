---
name: currency-formatting
description: How to format dollar amounts and percentages in Nova's responses.
---

# currency-formatting

Apply these rules every time you render a money value or percentage in a
response.

## Dollar amounts

- Use a leading `$` and commas for thousands: `$1,234.56`.
- Show two decimal places when there are cents: `$45.30`.
- Omit decimals for round dollar amounts: `$200`, not `$200.00`.
- Negative balances use parentheses, never a minus sign: `($45.00)`.

## Percentages

- One decimal place: `12.4%`.
- Drop trailing zeros: write `15%`, not `15.0%`.
- Round at the rule above — do not write more precision than one decimal.

## Ranges

- Use an en-dash with no spaces: `$50–$75`.
- Both endpoints carry the `$`.

## Examples

| Raw                    | Render as     |
| ---------------------- | ------------- |
| `1234.5`               | `$1,234.50`   |
| `200.00`               | `$200`        |
| `-45`                  | `($45.00)`    |
| `0.124` (as a percent) | `12.4%`       |
| `0.15` (as a percent)  | `15%`         |
| `50 to 75 dollars`     | `$50–$75`     |
