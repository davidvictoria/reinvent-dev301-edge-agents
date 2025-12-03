"""SCADA/MES Pydantic models for structured data extraction.

Provides validated data models for extracting production metrics,
equipment status, sensor readings, and alarm information from
SCADA reports and MES systems.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    """A single sensor reading with value and metadata.
    
    Attributes:
        sensor_id: Unique identifier for the sensor
        value: The measured value
        unit: Unit of measurement
        timestamp: Optional ISO timestamp of the reading
    """
    sensor_id: str = Field(
        ...,
        description="Unique identifier for the sensor",
        min_length=1
    )
    value: float = Field(
        ...,
        description="The measured sensor value"
    )
    unit: str = Field(
        ...,
        description="Unit of measurement (e.g., '°C', '%', 'PSI')",
        min_length=1
    )
    timestamp: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp of the reading"
    )


class AlarmInfo(BaseModel):
    """Information about an active or historical alarm.
    
    Attributes:
        alarm_id: Unique identifier for the alarm
        severity: Alarm severity level
        message: Human-readable alarm description
        acknowledged: Whether the alarm has been acknowledged
    """
    alarm_id: str = Field(
        ...,
        description="Unique identifier for the alarm",
        min_length=1
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        ...,
        description="Severity level of the alarm"
    )
    message: str = Field(
        ...,
        description="Human-readable description of the alarm condition",
        min_length=1
    )
    acknowledged: bool = Field(
        default=False,
        description="Whether the alarm has been acknowledged by an operator"
    )



class EquipmentStatus(BaseModel):
    """Status information for a piece of equipment.
    
    Attributes:
        equipment_id: Unique identifier for the equipment
        name: Human-readable name of the equipment
        status: Current operational status
        readings: List of current sensor readings
        active_alarms: List of active alarms for this equipment
    """
    equipment_id: str = Field(
        ...,
        description="Unique identifier for the equipment",
        min_length=1
    )
    name: str = Field(
        ...,
        description="Human-readable name of the equipment",
        min_length=1
    )
    status: Literal["running", "stopped", "maintenance", "fault"] = Field(
        ...,
        description="Current operational status of the equipment"
    )
    readings: List[SensorReading] = Field(
        default_factory=list,
        description="List of current sensor readings from this equipment"
    )
    active_alarms: List[AlarmInfo] = Field(
        default_factory=list,
        description="List of active alarms for this equipment"
    )


class ProductionMetrics(BaseModel):
    """Production metrics for a manufacturing line.
    
    Attributes:
        line_id: Unique identifier for the production line
        shift: Current shift identifier (e.g., 'morning', 'afternoon', 'night')
        units_produced: Number of units produced in current shift
        units_target: Target number of units for current shift
        efficiency_percent: Production efficiency as percentage
        equipment: List of equipment status for this line
    """
    line_id: str = Field(
        ...,
        description="Unique identifier for the production line",
        min_length=1
    )
    shift: str = Field(
        ...,
        description="Current shift identifier",
        min_length=1
    )
    units_produced: int = Field(
        ...,
        description="Number of units produced in current shift",
        ge=0
    )
    units_target: int = Field(
        ...,
        description="Target number of units for current shift",
        ge=0
    )
    efficiency_percent: float = Field(
        ...,
        description="Production efficiency as percentage (0-100+)",
        ge=0.0
    )
    equipment: List[EquipmentStatus] = Field(
        default_factory=list,
        description="List of equipment status for this production line"
    )
