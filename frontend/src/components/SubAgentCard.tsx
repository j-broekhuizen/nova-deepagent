import { useState } from "react";
import { CheckCircle, Loader2, AlertCircle, ChevronDown, ChevronUp, Bot } from "lucide-react";
import type { ToolCallWithResult } from "@langchain/langgraph-sdk/react";
import { MarkdownContent } from "./MarkdownContent";

interface SubAgentCardProps {
  toolCall: ToolCallWithResult;
}

const AGENT_LABELS: Record<string, string> = {
  spending_analyst: "Spending Analyst",
  savings_advisor: "Savings Advisor",
  account_manager: "Account Manager",
};

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

      {isExpanded && (
        <div className="px-3 pb-3 space-y-3 border-t border-gray-700 pt-3">
          {prompt && (
            <div>
              <h4 className="text-xs uppercase text-gray-500 mb-1">Task</h4>
              <p className="text-sm text-gray-300">{prompt}</p>
            </div>
          )}

          {toolCall.result && (
            <div>
              <h4 className="text-xs uppercase text-gray-500 mb-1">Result</h4>
              <div className="text-sm text-gray-300">
                <MarkdownContent content={resultContent} />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
