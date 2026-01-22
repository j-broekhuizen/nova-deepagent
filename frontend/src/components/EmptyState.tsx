import { Wallet } from "lucide-react";

interface EmptyStateProps {
  suggestions: string[];
  onSuggestionClick: (suggestion: string) => void;
}

export function EmptyState({ suggestions, onSuggestionClick }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 animate-fade-in">
      <div className="w-16 h-16 rounded-full bg-gray-800 flex items-center justify-center mb-6">
        <Wallet className="w-8 h-8 text-blue-400" />
      </div>

      <h2 className="text-xl font-semibold text-white mb-2">
        Welcome to Nova
      </h2>
      <p className="text-gray-400 text-center mb-8 max-w-md">
        Your personal financial assistant. Ask me about your spending, savings,
        or anything related to your finances.
      </p>

      <div className="w-full max-w-md space-y-2">
        <p className="text-sm text-gray-500 mb-3">Try asking:</p>
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => onSuggestionClick(suggestion)}
            className="w-full text-left px-4 py-3 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white transition-colors text-sm"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
}
