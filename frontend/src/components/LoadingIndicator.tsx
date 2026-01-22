export function LoadingIndicator() {
  return (
    <div className="flex items-center gap-1 py-2">
      <div
        className="w-2 h-2 rounded-full bg-gray-400 animate-pulse-dot"
        style={{ animationDelay: "0ms" }}
      />
      <div
        className="w-2 h-2 rounded-full bg-gray-400 animate-pulse-dot"
        style={{ animationDelay: "200ms" }}
      />
      <div
        className="w-2 h-2 rounded-full bg-gray-400 animate-pulse-dot"
        style={{ animationDelay: "400ms" }}
      />
    </div>
  );
}
