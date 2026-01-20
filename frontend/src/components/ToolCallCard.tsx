import { useState } from "react";
import { CheckCircle, Loader2, AlertCircle, ChevronDown, ChevronUp, Wrench } from "lucide-react";
import type { ToolCallWithResult } from "@langchain/langgraph-sdk/react";

interface ToolCallCardProps {
  toolCall: ToolCallWithResult;
}

function extractResultContent(result: unknown): string {
  if (!result) return "";
  if (typeof result === "string") return result;
  if (typeof result === "object" && result !== null) {
    const obj = result as Record<string, unknown>;
    if ("content" in obj) {
      if (typeof obj.content === "string") return obj.content;
      if (Array.isArray(obj.content)) {
        return obj.content
          .filter((c) => c.type === "text")
          .map((c) => c.text ?? "")
          .join("");
      }
    }
  }
  return JSON.stringify(result, null, 2);
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
              <pre className="text-xs text-gray-300 bg-gray-900 p-2 rounded overflow-x-auto whitespace-pre-wrap">
                {resultContent}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
