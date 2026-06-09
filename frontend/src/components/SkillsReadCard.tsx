import { useState } from "react";
import { BookOpen, CheckCircle, ChevronDown, ChevronUp } from "lucide-react";

interface SkillsReadCardProps {
  skillNames: string[];
}

export function SkillsReadCard({ skillNames }: SkillsReadCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (skillNames.length === 0) return null;

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800/50 animate-fade-in">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 px-3 py-2 w-full text-left hover:bg-gray-800 rounded-lg transition-colors"
      >
        <BookOpen className="w-4 h-4 text-amber-400" />
        <span className="text-sm text-gray-200 flex-1">
          Reading {skillNames.length} skill{skillNames.length === 1 ? "" : "s"} from Context Hub
        </span>
        <CheckCircle className="w-4 h-4 text-green-400" />
        {isExpanded ? (
          <ChevronUp className="w-4 h-4 text-gray-500" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-500" />
        )}
      </button>

      <div className="px-3 pb-2 space-y-1.5">
        {skillNames.map((name, idx) => (
          <div
            key={name}
            className="flex items-center gap-2 text-xs animate-fade-in"
            style={{ animationDelay: `${idx * 120}ms`, animationFillMode: "both" }}
          >
            <span className="text-gray-500 select-none">→</span>
            <span className="text-gray-500">read skill:</span>
            <code className="text-amber-300 font-mono">{name}</code>
          </div>
        ))}
      </div>
    </div>
  );
}
