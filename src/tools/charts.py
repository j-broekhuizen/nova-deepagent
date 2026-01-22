"""Chart generation tools."""

from typing import Literal

from langchain_core.tools import tool

from src.models.chart import AxisConfig, ChartSpec, ChartType, FormatterType, Series


@tool
def build_chart_spec(
    chart_type: Literal["line", "area", "bar", "stackedArea", "scatter", "pie"],
    data: list[dict],
    x_key: str,
    series_configs: list[dict],
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    x_formatter: Literal["usd", "percent", "date", "datetime", "number"] | None = None,
    y_formatter: Literal["usd", "percent", "date", "datetime", "number"] | None = None,
    height: int = 300,
) -> dict:
    """Build a chart specification for frontend visualization.

    Use this tool to create interactive charts that visualize financial data.
    The frontend will render the chart based on the returned specification.

    Args:
        chart_type: Type of chart to render.
            - "line": Line chart for trends over time
            - "area": Filled area chart
            - "bar": Bar chart for category comparisons
            - "stackedArea": Stacked areas for composition
            - "scatter": Scatter plot for correlations
            - "pie": Pie chart for showing proportions/percentages
        data: Array of data points. Each item should be a dict with keys
            matching x_key and the keys specified in series_configs.
            Example: [{"name": "Coffee", "amount": 127.50}, ...]
        x_key: Key in data objects to use for x-axis values.
        series_configs: List of series configurations. Each should have:
            - "key": The data key for y-values
            - "label": Display label for the series
            Example: [{"key": "amount", "label": "Spending"}]
        title: Optional chart title displayed above the chart.
        x_label: Optional label for the x-axis.
        y_label: Optional label for the y-axis.
        x_formatter: How to format x-axis values - "usd", "percent", "date", "datetime", or "number".
        y_formatter: How to format y-axis values - "usd", "percent", "date", "datetime", or "number".
        height: Chart height in pixels (default 300).

    Returns:
        A dictionary containing the chart specification that the frontend can render.

    Example:
        build_chart_spec(
            chart_type="bar",
            data=[
                {"name": "Coffee", "amount": 127.50},
                {"name": "Dining", "amount": 342.00},
                {"name": "Groceries", "amount": 456.78}
            ],
            x_key="name",
            series_configs=[{"key": "amount", "label": "Amount Spent"}],
            title="Monthly Spending by Category",
            y_formatter="usd"
        )
    """
    spec = ChartSpec(
        version=1,
        type=ChartType(chart_type),
        title=title,
        data=data,
        xKey=x_key,
        series=[Series(**s) for s in series_configs],
        xAxis=AxisConfig(
            label=x_label,
            formatter=FormatterType(x_formatter) if x_formatter else None,
        ),
        yAxis=AxisConfig(
            label=y_label,
            formatter=FormatterType(y_formatter) if y_formatter else None,
        ),
        height=height,
    )

    return {"chart": spec.model_dump()}
