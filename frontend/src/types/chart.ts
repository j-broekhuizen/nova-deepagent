import { z } from "zod";

// Chart type enum
export const ChartTypeSchema = z.enum([
  "line",
  "area",
  "bar",
  "stackedArea",
  "scatter",
  "pie",
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
  color: z.string().nullish(), // nullish = null | undefined
});
export type Series = z.infer<typeof SeriesSchema>;

// Axis configuration
export const AxisConfigSchema = z.object({
  label: z.string().nullish(),
  formatter: FormatterTypeSchema.nullish(),
});
export type AxisConfig = z.infer<typeof AxisConfigSchema>;

// Main ChartSpec
export const ChartSpecSchema = z.object({
  version: z.literal(1),
  type: ChartTypeSchema,
  title: z.string().nullish(),
  data: z.array(z.record(z.string(), z.unknown())),
  xKey: z.string(),
  series: z.array(SeriesSchema),
  xAxis: AxisConfigSchema.nullish(),
  yAxis: AxisConfigSchema.nullish(),
  showLegend: z.boolean().nullish(),
  showTooltip: z.boolean().nullish(),
  height: z.number().nullish(),
});
export type ChartSpec = z.infer<typeof ChartSpecSchema>;
