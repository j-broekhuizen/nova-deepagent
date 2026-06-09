---
name: category-vocabulary
description: The canonical spending-category vocabulary and common aliases.
---

# category-vocabulary

Use only the canonical category names below when referring to spending
categories in prose, in tool arguments, or in chart specs. When the user
uses a different word, translate it to the canonical name.

## Canonical categories

- `coffee`
- `fast_food`
- `delivery`
- `dining`
- `entertainment`
- `groceries`
- `transportation`
- `shopping`
- `subscription`
- `utilities`
- `healthcare`
- `income`
- `transfer`
- `other`

## Aliases

If the user says one of the terms on the left, treat it as the canonical
name on the right.

| User says                            | Canonical        |
| ------------------------------------ | ---------------- |
| `restaurants`, `eating out`          | `dining`         |
| `takeout`, `doordash`, `uber eats`   | `delivery`       |
| `gas`, `uber`, `lyft`, `parking`     | `transportation` |
| `streaming`, `netflix`, `spotify`    | `subscription`   |
| `supermarket`, `whole foods`         | `groceries`      |
| `clothes`, `amazon`                  | `shopping`       |
| `bills`, `electric`, `water`         | `utilities`      |
| `doctor`, `pharmacy`, `medical`      | `healthcare`     |

## Rules

- Always use the canonical name in tool arguments — the tools only know
  the canonical set.
- When echoing the user's word back in prose, you may use their term
  once for naturalness, but follow up with the canonical name on subsequent
  references.
- If the user references a category not in this list and not in the
  alias table, ask them to clarify rather than guessing.
