import { useMemo } from "react";
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
import { ParentSize } from "@visx/responsive";
import type { ChartSpec } from "../../types/chart";
import { getFormatter } from "./formatters";
import { novaChartTheme } from "./theme";

interface ChartRendererProps {
  spec: ChartSpec;
}

type DataRecord = Record<string, unknown>;

export function ChartRenderer({ spec }: ChartRendererProps) {
  const { type, data, xKey, series, xAxis, yAxis, title, height = 300 } = spec;

  const xFormatter = useMemo(
    () => getFormatter(xAxis?.formatter),
    [xAxis?.formatter]
  );
  const yFormatter = useMemo(
    () => getFormatter(yAxis?.formatter),
    [yAxis?.formatter]
  );

  // Determine scale types based on chart type
  const xScaleConfig = useMemo(() => {
    if (type === "bar") {
      return { type: "band" as const, padding: 0.2 };
    }
    // Check if xKey values are dates
    const firstValue = data[0]?.[xKey];
    if (
      firstValue instanceof Date ||
      (typeof firstValue === "string" && !isNaN(Date.parse(firstValue)))
    ) {
      return { type: "time" as const };
    }
    return { type: "linear" as const };
  }, [type, data, xKey]);

  const yScaleConfig = { type: "linear" as const };

  const accessors = useMemo(
    () => ({
      xAccessor: (d: DataRecord) => d[xKey],
      yAccessor: (key: string) => (d: DataRecord) => d[key] as number,
    }),
    [xKey]
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

  if (!data || data.length === 0) {
    return (
      <div className="text-gray-500 text-sm py-4 text-center">
        No data available for chart
      </div>
    );
  }

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-sm font-medium text-gray-200 mb-2">{title}</h3>
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
              margin={{ top: 20, right: 20, bottom: 40, left: 60 }}
            >
              <Grid columns={false} numTicks={4} strokeDasharray="2,3" />
              <Axis
                orientation="bottom"
                tickFormat={(v) => xFormatter(v)}
                label={xAxis?.label}
                numTicks={type === "bar" ? data.length : undefined}
              />
              <Axis
                orientation="left"
                tickFormat={(v) => yFormatter(v)}
                label={yAxis?.label}
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
