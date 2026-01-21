import { z } from "zod";

// Chart type enum
export const ChartTypeSchema = z.enum([
  "line",
  "area",
  "bar",
  "stackedArea",
  "scatter",
]);
export type ChartType = z.infer<typeof ChartTypeSchema>;

// Value formatter type
export const FormatterTypeSchema = z.enum([
  "usd",
  "percent",
  "date",
  "datetime",
  "number",
]);
export type FormatterType = z.infer<typeof FormatterTypeSchema>;

// Series definition
export const SeriesSchema = z.object({
  key: z.string(),
  label: z.string(),
  color: z.string().optional(),
});
export type Series = z.infer<typeof SeriesSchema>;

// Axis configuration
export const AxisConfigSchema = z.object({
  label: z.string().optional(),
  formatter: FormatterTypeSchema.optional(),
});
export type AxisConfig = z.infer<typeof AxisConfigSchema>;

// Main ChartSpec
export const ChartSpecSchema = z.object({
  version: z.literal(1),
  type: ChartTypeSchema,
  title: z.string().optional(),
  data: z.array(z.record(z.string(), z.unknown())),
  xKey: z.string(),
  series: z.array(SeriesSchema),
  xAxis: AxisConfigSchema.optional(),
  yAxis: AxisConfigSchema.optional(),
  showLegend: z.boolean().optional(),
  showTooltip: z.boolean().optional(),
  height: z.number().optional(),
});
export type ChartSpec = z.infer<typeof ChartSpecSchema>;
