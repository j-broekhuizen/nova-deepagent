import { buildChartTheme } from "@visx/xychart";

// Dark theme matching Nova's gray-900 background
export const novaChartTheme = buildChartTheme({
  backgroundColor: "transparent",
  colors: [
    "#3B82F6", // blue-500
    "#10B981", // green-500
    "#F59E0B", // amber-500
    "#EF4444", // red-500
    "#8B5CF6", // purple-500
    "#EC4899", // pink-500
  ],
  gridColor: "#374151", // gray-700
  gridColorDark: "#1F2937", // gray-800
  svgLabelSmall: { fill: "#9CA3AF" }, // gray-400
  svgLabelBig: { fill: "#F3F4F6" }, // gray-100
  tickLength: 4,
});
