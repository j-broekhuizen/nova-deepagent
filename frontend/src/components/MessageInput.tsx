import { ArrowUp, Square } from "lucide-react";

interface MessageInputProps {
  disabled?: boolean;
  placeholder?: string;
  onSubmit: (content: string) => void;
}

export function MessageInput({
  disabled,
  placeholder = "Type a message...",
  onSubmit,
}: MessageInputProps) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);
    const content = formData.get("content") as string;
    if (!content.trim()) return;
    form.reset();
    onSubmit(content);
  };

  return (
    <footer className="border-t border-gray-800 p-4">
      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
        <div className="flex gap-2">
          <textarea
            name="content"
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-3 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            style={{ fieldSizing: "content" } as React.CSSProperties}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                e.currentTarget.form?.requestSubmit();
              }
            }}
          />
          <button
            type="submit"
            disabled={disabled}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg px-4 py-3 transition-colors"
          >
            {disabled ? (
              <Square className="w-5 h-5" />
            ) : (
              <ArrowUp className="w-5 h-5" />
            )}
          </button>
        </div>
      </form>
    </footer>
  );
}
