"""Chart specification models for frontend visualization."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class ChartType(str, Enum):
    """Supported chart types."""

    LINE = "line"
    AREA = "area"
    BAR = "bar"
    STACKED_AREA = "stackedArea"
    SCATTER = "scatter"
    PIE = "pie"


class FormatterType(str, Enum):
    """Value formatter types for axis display."""

    USD = "usd"
    PERCENT = "percent"
    DATE = "date"
    DATETIME = "datetime"
    NUMBER = "number"


class Series(BaseModel):
    """A data series definition."""

    key: str
    label: str
    color: Optional[str] = None


class AxisConfig(BaseModel):
    """Axis configuration."""

    label: Optional[str] = None
    formatter: Optional[FormatterType] = None


class ChartSpec(BaseModel):
    """
    Chart specification that the frontend can render.

    This schema matches the frontend's Zod validation schema.
    """

    version: int = 1
    type: ChartType
    title: Optional[str] = None
    data: list[dict[str, Any]]
    xKey: str
    series: list[Series]
    xAxis: Optional[AxisConfig] = None
    yAxis: Optional[AxisConfig] = None
    showLegend: Optional[bool] = True
    showTooltip: Optional[bool] = True
    height: Optional[int] = 300
