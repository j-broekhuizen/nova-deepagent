import { useState } from "react";
import {
  CheckCircle,
  Loader2,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Wrench,
} from "lucide-react";
import type { ToolCallWithResult } from "@langchain/langgraph-sdk/react";
import { ChartSpecSchema, type ChartSpec } from "../types/chart";
import { ChartRenderer } from "./charts";

interface ToolCallCardProps {
  toolCall: ToolCallWithResult;
}

function isChartSpec(value: unknown): value is ChartSpec {
  return ChartSpecSchema.safeParse(value).success;
}

interface ExtractedResult {
  text: string;
  chart: ChartSpec | null;
}

function extractResultContent(result: unknown): ExtractedResult {
  if (!result) return { text: "", chart: null };

  // Check if result itself is a ChartSpec
  if (isChartSpec(result)) {
    return { text: "", chart: result };
  }

  // Check if result has a chart property
  if (typeof result === "object" && result !== null) {
    const obj = result as Record<string, unknown>;

    // Extract chart if present
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

    // If we found a chart, return the rest as text (excluding the chart key)
    if (chart) {
      const { chart: _, ...rest } = obj;
      if (Object.keys(rest).length > 0) {
        text = JSON.stringify(rest, null, 2);
      }
      return { text, chart };
    }

    // No chart found, return full object as text
    if (!text) {
      text = JSON.stringify(result, null, 2);
    }
    return { text, chart: null };
  }

  if (typeof result === "string") {
    return { text: result, chart: null };
  }

  return { text: JSON.stringify(result, null, 2), chart: null };
}

export function ToolCallCard({ toolCall }: ToolCallCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

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
        <Wrench className="w-4 h-4 text-gray-400" />
        <span className="font-mono text-sm text-gray-300 flex-1">
          {toolCall.call.name}
        </span>
        {statusIcon}
        {isExpanded ? (
          <ChevronUp className="w-4 h-4 text-gray-500" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-500" />
        )}
      </button>

      {isExpanded && (
        <div className="px-3 pb-3 space-y-3 border-t border-gray-700 pt-3">
          <div>
            <h4 className="text-xs uppercase text-gray-500 mb-1">Arguments</h4>
            <pre className="text-xs text-gray-300 bg-gray-900 p-2 rounded overflow-x-auto">
              {JSON.stringify(toolCall.call.args, null, 2)}
            </pre>
          </div>

          {toolCall.result && (
            <div>
              <h4 className="text-xs uppercase text-gray-500 mb-1">Result</h4>
              {resultContent.chart && (
                <div className="mb-3 bg-gray-900 p-3 rounded">
                  <ChartRenderer spec={resultContent.chart} />
                </div>
              )}
              {resultContent.text && (
                <pre className="text-xs text-gray-300 bg-gray-900 p-2 rounded overflow-x-auto whitespace-pre-wrap max-h-64 overflow-y-auto">
                  {resultContent.text}
                </pre>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
