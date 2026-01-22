import { useCallback } from "react";
import { useStickToBottom } from "use-stick-to-bottom";
import { AlertCircle } from "lucide-react";
import type { UseStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";

import { MessageBubble } from "./MessageBubble";
import { ToolCallCard } from "./ToolCallCard";
import { SubAgentCard } from "./SubAgentCard";
import { MessageInput } from "./MessageInput";
import { LoadingIndicator } from "./LoadingIndicator";
import { EmptyState } from "./EmptyState";

interface ChatInterfaceProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  stream: UseStream<any, any>;
}

function hasContent(message: Message): boolean {
  if (typeof message.content === "string") {
    return message.content.trim().length > 0;
  }
  if (Array.isArray(message.content)) {
    return message.content.some(
      (c) => c.type === "text" && c.text?.trim().length > 0
    );
  }
  return false;
}

const SUGGESTIONS = [
  "How much did I spend on coffee this month?",
  "What if I made coffee at home instead?",
  "Show me my spending breakdown",
  "How much should I transfer to savings?",
];

export function ChatInterface({ stream }: ChatInterfaceProps) {
  const { scrollRef, contentRef } = useStickToBottom();

  const handleSubmit = useCallback(
    (content: string) => {
      stream.submit({ messages: [{ content, type: "human" }] });
    },
    [stream]
  );

  const hasMessages = stream.messages.length > 0;

  return (
    <div className="h-full flex flex-col">
      <header className="border-b border-gray-800 px-4 py-3">
        <h1 className="text-lg font-semibold text-white">Nova</h1>
        <p className="text-sm text-gray-400">Personal Financial Assistant</p>
      </header>

      <main ref={scrollRef} className="flex-1 overflow-y-auto">
        <div ref={contentRef} className="max-w-2xl mx-auto px-4 py-6">
          {!hasMessages ? (
            <EmptyState
              suggestions={SUGGESTIONS}
              onSuggestionClick={handleSubmit}
            />
          ) : (
            <div className="flex flex-col gap-4">
              {stream.messages.map((message, idx) => {
                if (message.type === "ai") {
                  const toolCalls = stream.getToolCalls(message);

                  // Separate subagent calls from regular tool calls
                  const subAgentCalls = toolCalls.filter(
                    (tc) =>
                      tc.call.name === "task" &&
                      tc.call.args &&
                      "subagent_type" in tc.call.args
                  );
                  const regularToolCalls = toolCalls.filter(
                    (tc) =>
                      !(
                        tc.call.name === "task" &&
                        tc.call.args &&
                        "subagent_type" in tc.call.args
                      )
                  );

                  // Render tool calls if present
                  if (toolCalls.length > 0) {
                    return (
                      <div key={message.id ?? idx} className="flex flex-col gap-2">
                        {subAgentCalls.map((tc) => (
                          <SubAgentCard key={tc.id} toolCall={tc} />
                        ))}
                        {regularToolCalls.map((tc) => (
                          <ToolCallCard key={tc.id} toolCall={tc} />
                        ))}
                        {hasContent(message) && (
                          <MessageBubble message={message} />
                        )}
                      </div>
                    );
                  }

                  // Skip AI messages without content
                  if (!hasContent(message)) {
                    return null;
                  }
                }

                // Skip tool messages (handled with their calls)
                if (message.type === "tool") {
                  return null;
                }

                return (
                  <MessageBubble key={message.id ?? idx} message={message} />
                );
              })}

              {stream.isLoading && <LoadingIndicator />}
            </div>
          )}
        </div>
      </main>

      {stream.error != null && (
        <div className="max-w-2xl mx-auto px-4 pb-3">
          <div className="bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3 text-red-400 text-sm">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>
                {stream.error instanceof Error
                  ? stream.error.message
                  : "An error occurred"}
              </span>
            </div>
          </div>
        </div>
      )}

      <MessageInput
        disabled={stream.isLoading}
        placeholder="Ask Nova about your finances..."
        onSubmit={handleSubmit}
      />
    </div>
  );
}
