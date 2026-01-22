import type { Message } from "@langchain/langgraph-sdk";
import { MarkdownContent } from "./MarkdownContent";

interface MessageBubbleProps {
  message: Message;
}

function extractTextContent(message: Message): string {
  if (typeof message.content === "string") {
    return message.content;
  }
  if (Array.isArray(message.content)) {
    return message.content
      .filter((c) => c.type === "text")
      .map((c) => c.text ?? "")
      .join("");
  }
  return "";
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const content = extractTextContent(message);

  if (message.type === "human") {
    return (
      <div className="flex justify-end animate-fade-in">
        <div className="bg-blue-600 text-white rounded-2xl px-4 py-2 max-w-[80%]">
          <p className="whitespace-pre-wrap">{content}</p>
        </div>
      </div>
    );
  }

  if (message.type === "ai") {
    return (
      <div className="flex justify-start animate-fade-in">
        <div className="text-gray-100 max-w-[90%]">
          <MarkdownContent content={content} />
        </div>
      </div>
    );
  }

  return null;
}
