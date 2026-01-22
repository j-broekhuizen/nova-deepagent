import { useStream } from "@langchain/langgraph-sdk/react";
import { ChatInterface } from "./components/ChatInterface";

interface NovaState {
  messages: Array<{
    type: string;
    content: string | Array<{ type: string; text?: string }>;
    id?: string;
  }>;
}

export function App() {
  const stream = useStream<NovaState>({
    assistantId: "nova",
    apiUrl: "http://localhost:2024",
    fetchStateHistory: true,
  });

  return (
    <div className="h-screen bg-gray-900">
      <ChatInterface stream={stream} />
    </div>
  );
}
