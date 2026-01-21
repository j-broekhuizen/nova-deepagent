import type { FormatterType } from "../../types/chart";

export function getFormatter(
  type: FormatterType | undefined
): (value: unknown) => string {
  switch (type) {
    case "usd":
      return (v) => {
        const num = Number(v);
        return new Intl.NumberFormat("en-US", {
          style: "currency",
          currency: "USD",
          minimumFractionDigits: 0,
          maximumFractionDigits: 2,
        }).format(num);
      };
    case "percent":
      return (v) => `${Number(v).toFixed(1)}%`;
    case "date":
      return (v) => {
        const date = v instanceof Date ? v : new Date(String(v));
        return date.toLocaleDateString();
      };
    case "datetime":
      return (v) => {
        const date = v instanceof Date ? v : new Date(String(v));
        return date.toLocaleString();
      };
    case "number":
    default:
      return (v) => String(v);
  }
}
