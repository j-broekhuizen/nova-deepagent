import { useStream } from "@langchain/langgraph-sdk/react";
import { ChatInterface } from "./components/ChatInterface";

interface NovaState {
  messages: Array<{
    type: string;
    content: string | Array<{ type: string; text?: string }>;
    id?: string;
  }>;
}

const LANGGRAPH_PORT = import.meta.env.VITE_LANGGRAPH_PORT || "2024";

export function App() {
  const stream = useStream<NovaState>({
    assistantId: "nova",
    apiUrl: `http://localhost:${LANGGRAPH_PORT}`,
    fetchStateHistory: true,
  });

  return (
    <div className="h-screen bg-gray-900">
      <ChatInterface stream={stream} />
    </div>
  );
}
