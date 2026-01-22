import { useMemo, useState } from "react";
import {
  XYChart,
  AnimatedLineSeries,
  AnimatedBarSeries,
  AnimatedAreaSeries,
  AnimatedAreaStack,
  Axis,
  Grid,
  Tooltip,
} from "@visx/xychart";
import { Pie } from "@visx/shape";
import { Group } from "@visx/group";
import { scaleOrdinal } from "@visx/scale";
import { ParentSize } from "@visx/responsive";
import type { ChartSpec } from "../../types/chart";
import { getFormatter } from "./formatters";
import { novaChartTheme } from "./theme";

// Color palette for pie chart
const PIE_COLORS = [
  "#60a5fa", // blue-400
  "#34d399", // emerald-400
  "#fbbf24", // amber-400
  "#f87171", // red-400
  "#a78bfa", // violet-400
  "#2dd4bf", // teal-400
  "#fb923c", // orange-400
  "#e879f9", // fuchsia-400
];

interface ChartRendererProps {
  spec: ChartSpec;
}

type DataRecord = Record<string, unknown>;

export function ChartRenderer({ spec }: ChartRendererProps) {
  const { type, data, xKey, series, xAxis, yAxis, title } = spec;
  const height = spec.height ?? 300;

  // Check if x values are dates
  const isTimeScale = useMemo(() => {
    if (type === "bar") return false;
    const firstValue = data[0]?.[xKey];
    return (
      firstValue instanceof Date ||
      (typeof firstValue === "string" && !isNaN(Date.parse(firstValue)))
    );
  }, [type, data, xKey]);

  // Auto-detect date formatter for time scales
  const xFormatter = useMemo(
    () => getFormatter(xAxis?.formatter ?? (isTimeScale ? "date" : undefined)),
    [xAxis?.formatter, isTimeScale]
  );
  const yFormatter = useMemo(
    () => getFormatter(yAxis?.formatter ?? undefined),
    [yAxis?.formatter]
  );

  // Determine scale types based on chart type
  const xScaleConfig = useMemo(() => {
    if (type === "bar") {
      return { type: "band" as const, padding: 0.2 };
    }
    if (isTimeScale) {
      return { type: "time" as const };
    }
    return { type: "linear" as const };
  }, [type, isTimeScale]);

  const yScaleConfig = { type: "linear" as const };

  const accessors = useMemo(
    () => ({
      // For time scales, convert date strings to Date objects
      xAccessor: (d: DataRecord) => {
        const value = d[xKey];
        if (isTimeScale && typeof value === "string") {
          return new Date(value);
        }
        return value;
      },
      yAccessor: (key: string) => (d: DataRecord) => d[key] as number,
    }),
    [xKey, isTimeScale]
  );

  const renderSeries = () => {
    switch (type) {
      case "line":
        return series.map((s) => (
          <AnimatedLineSeries
            key={s.key}
            dataKey={s.key}
            data={data as DataRecord[]}
            xAccessor={accessors.xAccessor}
            yAccessor={accessors.yAccessor(s.key)}
          />
        ));
      case "bar":
        return series.map((s) => (
          <AnimatedBarSeries
            key={s.key}
            dataKey={s.key}
            data={data as DataRecord[]}
            xAccessor={accessors.xAccessor}
            yAccessor={accessors.yAccessor(s.key)}
          />
        ));
      case "area":
        return series.map((s) => (
          <AnimatedAreaSeries
            key={s.key}
            dataKey={s.key}
            data={data as DataRecord[]}
            xAccessor={accessors.xAccessor}
            yAccessor={accessors.yAccessor(s.key)}
            fillOpacity={0.4}
          />
        ));
      case "stackedArea":
        return (
          <AnimatedAreaStack>
            {series.map((s) => (
              <AnimatedAreaSeries
                key={s.key}
                dataKey={s.key}
                data={data as DataRecord[]}
                xAccessor={accessors.xAccessor}
                yAccessor={accessors.yAccessor(s.key)}
                fillOpacity={0.6}
              />
            ))}
          </AnimatedAreaStack>
        );
      case "scatter":
        // For scatter, we use LineSeries with no curve connection
        return series.map((s) => (
          <AnimatedLineSeries
            key={s.key}
            dataKey={s.key}
            data={data as DataRecord[]}
            xAccessor={accessors.xAccessor}
            yAccessor={accessors.yAccessor(s.key)}
            strokeWidth={0}
          />
        ));
      default:
        return null;
    }
  };

  // Pie chart color scale
  const pieColorScale = useMemo(
    () =>
      scaleOrdinal({
        domain: data.map((d) => String(d[xKey])),
        range: PIE_COLORS,
      }),
    [data, xKey]
  );

  // State for pie chart hover
  const [hoveredSlice, setHoveredSlice] = useState<string | null>(null);

  if (!data || data.length === 0) {
    return (
      <div className="text-gray-500 text-sm py-4 text-center">
        No data available for chart
      </div>
    );
  }

  // Render pie chart separately
  if (type === "pie") {
    const valueKey = series[0]?.key || "amount";

    return (
      <div className="w-full pt-3">
        {title && (
          <h3 className="text-sm font-medium text-gray-200 mb-3 text-center">
            {title}
          </h3>
        )}
        <ParentSize>
          {({ width }) => {
            if (width <= 0) return null;
            const radius = Math.min(width, height) / 2 - 40;
            const centerX = width / 2;
            const centerY = height / 2;

            return (
              <svg width={width} height={height}>
                <Group top={centerY} left={centerX}>
                  <Pie
                    data={data}
                    pieValue={(d) => Number(d[valueKey]) || 0}
                    outerRadius={radius}
                    innerRadius={radius * 0.4}
                    padAngle={0.02}
                  >
                    {(pie) =>
                      pie.arcs.map((arc, i) => {
                        const label = String(data[i][xKey]);
                        const isHovered = hoveredSlice === label;
                        const [centroidX, centroidY] = pie.path.centroid(arc);
                        const pathD = pie.path(arc) || "";

                        return (
                          <g
                            key={`arc-${label}`}
                            onMouseEnter={() => setHoveredSlice(label)}
                            onMouseLeave={() => setHoveredSlice(null)}
                            style={{ cursor: "pointer" }}
                          >
                            {/* Invisible larger hit area to prevent hover flicker */}
                            <path
                              d={pathD}
                              fill="transparent"
                              style={{ transform: "scale(1.1)", transformOrigin: `${centroidX}px ${centroidY}px` }}
                            />
                            {/* Visible slice */}
                            <path
                              d={pathD}
                              fill={pieColorScale(label)}
                              opacity={isHovered ? 1 : 0.85}
                              stroke={isHovered ? "#fff" : "transparent"}
                              strokeWidth={2}
                              pointerEvents="none"
                              style={{
                                transform: isHovered ? "scale(1.03)" : "scale(1)",
                                transformOrigin: `${centroidX}px ${centroidY}px`,
                                transition: "all 0.15s ease-out",
                              }}
                            />
                            {arc.endAngle - arc.startAngle > 0.4 && (
                              <text
                                x={centroidX}
                                y={centroidY}
                                textAnchor="middle"
                                dominantBaseline="middle"
                                fill="#fff"
                                fontSize={11}
                                fontWeight={500}
                                pointerEvents="none"
                              >
                                {Math.round(
                                  ((arc.endAngle - arc.startAngle) / (2 * Math.PI)) * 100
                                )}
                                %
                              </text>
                            )}
                          </g>
                        );
                      })
                    }
                  </Pie>
                </Group>
                {/* Legend */}
                <Group top={height - 30} left={20}>
                  {data.slice(0, 6).map((d, i) => {
                    const label = String(d[xKey]);
                    return (
                      <Group key={label} left={i * (width / 6)}>
                        <rect
                          width={10}
                          height={10}
                          fill={pieColorScale(label)}
                          rx={2}
                        />
                        <text
                          x={14}
                          y={9}
                          fill="#9ca3af"
                          fontSize={10}
                        >
                          {label.length > 10 ? label.slice(0, 10) + "…" : label}
                        </text>
                      </Group>
                    );
                  })}
                </Group>
                {/* Tooltip on hover */}
                {hoveredSlice && (
                  <Group top={20} left={width / 2}>
                    <text
                      textAnchor="middle"
                      fill="#e5e7eb"
                      fontSize={13}
                      fontWeight={500}
                    >
                      {hoveredSlice}:{" "}
                      {yFormatter(
                        data.find((d) => String(d[xKey]) === hoveredSlice)?.[valueKey]
                      )}
                    </text>
                  </Group>
                )}
              </svg>
            );
          }}
        </ParentSize>
      </div>
    );
  }

  // Check if we have axis labels to adjust margins accordingly
  const hasYLabel = Boolean(yAxis?.label);
  const hasXLabel = Boolean(xAxis?.label);

  return (
    <div className="w-full pt-3">
      {title && (
        <h3 className="text-sm font-medium text-gray-200 mb-3 text-center">{title}</h3>
      )}
      <ParentSize>
        {({ width }) =>
          width > 0 ? (
            <XYChart
              width={width}
              height={height}
              xScale={xScaleConfig}
              yScale={yScaleConfig}
              theme={novaChartTheme}
              margin={{
                top: 20,
                right: 20,
                bottom: isTimeScale ? 70 : hasXLabel ? 50 : 40,
                left: hasYLabel ? 80 : 60,
              }}
            >
              <Grid columns={false} numTicks={4} strokeDasharray="2,3" />
              <Axis
                orientation="bottom"
                tickFormat={(v) => xFormatter(v)}
                label={xAxis?.label ?? undefined}
                labelOffset={isTimeScale ? 25 : 15}
                numTicks={type === "bar" ? data.length : isTimeScale ? 6 : undefined}
                tickLabelProps={
                  isTimeScale
                    ? { angle: -45, textAnchor: "end", fontSize: 10 }
                    : undefined
                }
              />
              <Axis
                orientation="left"
                tickFormat={(v) => yFormatter(v)}
                label={yAxis?.label ?? undefined}
                labelOffset={45}
                numTicks={4}
              />
              {renderSeries()}
              {spec.showTooltip !== false && (
                <Tooltip
                  snapTooltipToDatumX
                  snapTooltipToDatumY
                  showSeriesGlyphs
                  renderTooltip={({ tooltipData }) => {
                    const datum = tooltipData?.nearestDatum?.datum as
                      | DataRecord
                      | undefined;
                    if (!datum) return null;
                    return (
                      <div className="bg-gray-800 rounded px-2 py-1 text-sm border border-gray-700">
                        <div className="text-gray-400 text-xs">
                          {xFormatter(datum[xKey])}
                        </div>
                        {series.map((s) => (
                          <div key={s.key} className="text-gray-100">
                            {s.label}: {yFormatter(datum[s.key])}
                          </div>
                        ))}
                      </div>
                    );
                  }}
                />
              )}
            </XYChart>
          ) : null
        }
      </ParentSize>
    </div>
  );
}
