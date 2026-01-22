import { useState } from "react";
import { CheckCircle, Loader2, AlertCircle, ChevronDown, ChevronUp, Bot } from "lucide-react";
import type { ToolCallWithResult } from "@langchain/langgraph-sdk/react";
import { MarkdownContent } from "./MarkdownContent";
import { ChartSpecSchema, type ChartSpec } from "../types/chart";
import { ChartRenderer } from "./charts";

interface SubAgentCardProps {
  toolCall: ToolCallWithResult;
}

const AGENT_LABELS: Record<string, string> = {
  spending_analyst: "Spending Analyst",
  savings_advisor: "Savings Advisor",
  account_manager: "Account Manager",
};

function isChartSpec(value: unknown): value is ChartSpec {
  return ChartSpecSchema.safeParse(value).success;
}

interface ExtractedResult {
  text: string;
  chart: ChartSpec | null;
}

// Parse chartdata block from text content (```chartdata ... ```)
function parseChartFromText(text: string): { text: string; chart: ChartSpec | null } {
  const chartDataRegex = /```chartdata\s*([\s\S]*?)```/;
  const match = text.match(chartDataRegex);

  if (!match) {
    return { text, chart: null };
  }

  try {
    const jsonStr = match[1].trim();
    const parsed = JSON.parse(jsonStr);

    // The chart spec might be directly the chart or wrapped in { chart: ... }
    const chartData = parsed.chart || parsed;
    if (isChartSpec(chartData)) {
      // Remove the chartdata block from text
      const cleanText = text.replace(chartDataRegex, "").trim();
      return { text: cleanText, chart: chartData };
    }
  } catch {
    // JSON parse failed, return original text
  }

  return { text, chart: null };
}

function extractResultContent(result: unknown): ExtractedResult {
  if (!result) return { text: "", chart: null };

  // Check if result itself is a ChartSpec
  if (isChartSpec(result)) {
    return { text: "", chart: result };
  }

  // For string results (common for subagent responses), look for chartdata block
  if (typeof result === "string") {
    return parseChartFromText(result);
  }

  if (typeof result === "object" && result !== null) {
    const obj = result as Record<string, unknown>;

    // Extract chart if present directly in object
    let chart: ChartSpec | null = null;
    if ("chart" in obj && isChartSpec(obj.chart)) {
      chart = obj.chart;
    }

    // Extract text content
    let text = "";
    if ("content" in obj) {
      if (typeof obj.content === "string") {
        text = obj.content;
      } else if (Array.isArray(obj.content)) {
        text = obj.content
          .filter((c) => c.type === "text")
          .map((c) => c.text ?? "")
          .join("");
      }
    }

    // If we found a chart in object, return it
    if (chart) {
      const { chart: _, ...rest } = obj;
      if (!text && Object.keys(rest).length > 0) {
        text = JSON.stringify(rest, null, 2);
      }
      return { text, chart };
    }

    // If text content exists, check for chartdata block in it
    if (text) {
      return parseChartFromText(text);
    }

    if (!text) {
      text = JSON.stringify(result, null, 2);
    }
    return { text, chart: null };
  }

  return { text: JSON.stringify(result, null, 2), chart: null };
}

export function SubAgentCard({ toolCall }: SubAgentCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const args = toolCall.call.args as Record<string, unknown>;
  const subAgentType = String(args.subagent_type || "agent");
  const prompt = String(args.prompt || "");

  const label = AGENT_LABELS[subAgentType] || subAgentType;

  const statusIcon = {
    pending: <Loader2 className="w-4 h-4 animate-spin text-blue-400" />,
    completed: <CheckCircle className="w-4 h-4 text-green-400" />,
    error: <AlertCircle className="w-4 h-4 text-red-400" />,
  }[toolCall.state];

  const resultContent = extractResultContent(toolCall.result);

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800/50 animate-fade-in">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 px-3 py-2 w-full text-left hover:bg-gray-800 rounded-lg transition-colors"
      >
        <Bot className="w-4 h-4 text-purple-400" />
        <span className="text-sm text-gray-200 flex-1">{label}</span>
        {statusIcon}
        {isExpanded ? (
          <ChevronUp className="w-4 h-4 text-gray-500" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-500" />
        )}
      </button>

      {/* Chart displayed prominently outside collapsed section */}
      {resultContent.chart && (
        <div className="px-3 pb-3 bg-gray-900 border-t border-gray-700">
          <ChartRenderer spec={resultContent.chart} />
        </div>
      )}

      {isExpanded && (
        <div className="px-3 pb-3 space-y-3 border-t border-gray-700 pt-3">
          {prompt && (
            <div>
              <h4 className="text-xs uppercase text-gray-500 mb-1">Task</h4>
              <p className="text-sm text-gray-300">{prompt}</p>
            </div>
          )}

          {toolCall.result && resultContent.text && (
            <div>
              <h4 className="text-xs uppercase text-gray-500 mb-1">Result</h4>
              <div className="text-sm text-gray-300">
                <MarkdownContent content={resultContent.text} />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
