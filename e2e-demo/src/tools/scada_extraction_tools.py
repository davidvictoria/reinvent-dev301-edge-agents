"""SCADA data extraction tools for structured output.

Provides tools for extracting validated, type-safe data from unstructured
SCADA reports using Pydantic models for schema validation.
"""

from typing import Optional
from pydantic import ValidationError

from strands import tool

from ..models.scada_models import ProductionMetrics


@tool
def extract_scada_metrics(report_text: str) -> str:
    """Extract structured production metrics from a SCADA report.
    
    This tool parses unstructured SCADA report text and extracts validated
    production metrics conforming to the ProductionMetrics Pydantic schema.
    The extraction uses pattern matching and heuristics to identify key
    metrics from the report text.
    
    Args:
        report_text: The raw text content of a SCADA report containing
                    production metrics, equipment status, and sensor readings.
        
    Returns:
        A formatted string containing the extracted metrics in a structured
        format, or an error message if extraction or validation fails.
        
    Example:
        >>> extract_scada_metrics('''
        ... Production Line: LINE-001
        ... Shift: Morning
        ... Units Produced: 450
        ... Target: 500
        ... Efficiency: 90%
        ... ''')
    """
    if not report_text or not report_text.strip():
        return "Error: Empty report text provided. Please provide a valid SCADA report."
    
    try:
        # Parse the report text to extract metrics
        metrics = _parse_scada_report(report_text)
        
        # Format the extracted metrics for display
        return _format_production_metrics(metrics)
        
    except ValidationError as e:
        # Handle Pydantic validation errors gracefully
        error_details = []
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            msg = error["msg"]
            error_details.append(f"  - {field}: {msg}")
        
        return (
            "Error: Extracted data failed validation.\n"
            "Validation errors:\n" + "\n".join(error_details) + "\n\n"
            "Please provide a report with the following required fields:\n"
            "  - line_id: Production line identifier\n"
            "  - shift: Shift name (e.g., 'morning', 'afternoon', 'night')\n"
            "  - units_produced: Number of units produced (non-negative integer)\n"
            "  - units_target: Target units (non-negative integer)\n"
            "  - efficiency_percent: Efficiency percentage (non-negative number)"
        )
    except ExtractionError as e:
        return f"Error: Failed to extract metrics from report. {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error during extraction: {str(e)}"


class ExtractionError(Exception):
    """Raised when SCADA report extraction fails."""
    pass


def _parse_scada_report(report_text: str) -> ProductionMetrics:
    """Parse SCADA report text and extract ProductionMetrics.
    
    This function uses pattern matching to extract key metrics from
    unstructured report text. It looks for common patterns like:
    - "Line: XXX" or "Production Line: XXX"
    - "Shift: XXX"
    - "Units Produced: NNN"
    - "Target: NNN" or "Units Target: NNN"
    - "Efficiency: NN%" or "Efficiency Percent: NN"
    
    Args:
        report_text: Raw SCADA report text
        
    Returns:
        Validated ProductionMetrics object
        
    Raises:
        ExtractionError: If required fields cannot be extracted
        ValidationError: If extracted data fails Pydantic validation
    """
    import re
    
    text = report_text.strip()
    
    # Extract line_id
    line_id = _extract_field(
        text,
        [
            r"(?:Production\s+)?Line(?:\s+ID)?[:\s]+([A-Za-z0-9_-]+)",
            r"line_id[:\s]+([A-Za-z0-9_-]+)",
        ],
        "line_id"
    )
    
    # Extract shift
    shift = _extract_field(
        text,
        [
            r"Shift[:\s]+(\w+)",
            r"shift[:\s]+(\w+)",
        ],
        "shift"
    )
    
    # Extract units_produced
    units_produced_str = _extract_field(
        text,
        [
            r"Units\s+Produced[:\s]+(\d+)",
            r"Produced[:\s]+(\d+)",
            r"units_produced[:\s]+(\d+)",
        ],
        "units_produced"
    )
    units_produced = int(units_produced_str)
    
    # Extract units_target
    units_target_str = _extract_field(
        text,
        [
            r"(?:Units\s+)?Target[:\s]+(\d+)",
            r"units_target[:\s]+(\d+)",
        ],
        "units_target"
    )
    units_target = int(units_target_str)
    
    # Extract efficiency_percent
    efficiency_str = _extract_field(
        text,
        [
            r"Efficiency(?:\s+Percent)?[:\s]+(\d+(?:\.\d+)?)\s*%?",
            r"efficiency_percent[:\s]+(\d+(?:\.\d+)?)",
            r"efficiency[:\s]+(\d+(?:\.\d+)?)",
        ],
        "efficiency_percent"
    )
    efficiency_percent = float(efficiency_str)
    
    # Extract optional equipment status (if present)
    equipment = _extract_equipment_status(text)
    
    # Create and validate the ProductionMetrics object
    return ProductionMetrics(
        line_id=line_id,
        shift=shift,
        units_produced=units_produced,
        units_target=units_target,
        efficiency_percent=efficiency_percent,
        equipment=equipment
    )


def _extract_field(text: str, patterns: list[str], field_name: str) -> str:
    """Extract a field value using multiple regex patterns.
    
    Args:
        text: Text to search
        patterns: List of regex patterns to try (in order)
        field_name: Name of the field (for error messages)
        
    Returns:
        Extracted field value
        
    Raises:
        ExtractionError: If no pattern matches
    """
    import re
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    raise ExtractionError(
        f"Could not extract '{field_name}' from report. "
        f"Please ensure the report contains this field."
    )


def _extract_equipment_status(text: str) -> list:
    """Extract equipment status information from report text.
    
    This is an optional extraction - returns empty list if no
    equipment information is found.
    
    Args:
        text: Report text to parse
        
    Returns:
        List of EquipmentStatus objects (may be empty)
    """
    import re
    from ..models.scada_models import EquipmentStatus, SensorReading, AlarmInfo
    
    equipment_list = []
    
    # Look for equipment blocks in the text
    # Pattern: "Equipment: ID - Name (status)"
    equipment_pattern = r"Equipment[:\s]+([A-Za-z0-9_-]+)\s*[-–]\s*([^(]+)\s*\((\w+)\)"
    
    for match in re.finditer(equipment_pattern, text, re.IGNORECASE):
        equipment_id = match.group(1).strip()
        name = match.group(2).strip()
        status_str = match.group(3).strip().lower()
        
        # Validate status
        valid_statuses = ["running", "stopped", "maintenance", "fault"]
        if status_str not in valid_statuses:
            continue
        
        # Extract sensor readings for this equipment (if any)
        readings = _extract_sensor_readings(text, equipment_id)
        
        # Extract alarms for this equipment (if any)
        alarms = _extract_alarms(text, equipment_id)
        
        try:
            equipment = EquipmentStatus(
                equipment_id=equipment_id,
                name=name,
                status=status_str,
                readings=readings,
                active_alarms=alarms
            )
            equipment_list.append(equipment)
        except ValidationError:
            # Skip invalid equipment entries
            continue
    
    return equipment_list


def _extract_sensor_readings(text: str, equipment_id: str) -> list:
    """Extract sensor readings associated with equipment.
    
    Args:
        text: Report text
        equipment_id: Equipment ID to find readings for
        
    Returns:
        List of SensorReading objects
    """
    import re
    from ..models.scada_models import SensorReading
    
    readings = []
    
    # Pattern: "Sensor: ID = value unit" or "sensor_id: value unit"
    sensor_pattern = r"Sensor[:\s]+([A-Za-z0-9_-]+)\s*[=:]\s*(\d+(?:\.\d+)?)\s*(\S+)"
    
    for match in re.finditer(sensor_pattern, text, re.IGNORECASE):
        sensor_id = match.group(1).strip()
        value = float(match.group(2))
        unit = match.group(3).strip()
        
        try:
            reading = SensorReading(
                sensor_id=sensor_id,
                value=value,
                unit=unit
            )
            readings.append(reading)
        except ValidationError:
            continue
    
    return readings


def _extract_alarms(text: str, equipment_id: str) -> list:
    """Extract alarm information associated with equipment.
    
    Args:
        text: Report text
        equipment_id: Equipment ID to find alarms for
        
    Returns:
        List of AlarmInfo objects
    """
    import re
    from ..models.scada_models import AlarmInfo
    
    alarms = []
    
    # Pattern: "Alarm: ID (severity) - message"
    alarm_pattern = r"Alarm[:\s]+([A-Za-z0-9_-]+)\s*\((\w+)\)\s*[-–:]\s*(.+?)(?:\n|$)"
    
    for match in re.finditer(alarm_pattern, text, re.IGNORECASE):
        alarm_id = match.group(1).strip()
        severity_str = match.group(2).strip().lower()
        message = match.group(3).strip()
        
        # Validate severity
        valid_severities = ["low", "medium", "high", "critical"]
        if severity_str not in valid_severities:
            continue
        
        try:
            alarm = AlarmInfo(
                alarm_id=alarm_id,
                severity=severity_str,
                message=message
            )
            alarms.append(alarm)
        except ValidationError:
            continue
    
    return alarms


def _format_production_metrics(metrics: ProductionMetrics) -> str:
    """Format ProductionMetrics as a human-readable string.
    
    Args:
        metrics: Validated ProductionMetrics object
        
    Returns:
        Formatted string representation
    """
    lines = [
        "Extracted Production Metrics:",
        "=" * 50,
        f"  Line ID: {metrics.line_id}",
        f"  Shift: {metrics.shift}",
        f"  Units Produced: {metrics.units_produced}",
        f"  Units Target: {metrics.units_target}",
        f"  Efficiency: {metrics.efficiency_percent:.1f}%",
    ]
    
    if metrics.equipment:
        lines.append("\n  Equipment Status:")
        lines.append("  " + "-" * 40)
        
        for equip in metrics.equipment:
            lines.append(f"\n    Equipment: {equip.equipment_id} - {equip.name}")
            lines.append(f"      Status: {equip.status}")
            
            if equip.readings:
                lines.append("      Sensor Readings:")
                for reading in equip.readings:
                    lines.append(f"        - {reading.sensor_id}: {reading.value} {reading.unit}")
            
            if equip.active_alarms:
                lines.append("      Active Alarms:")
                for alarm in equip.active_alarms:
                    ack_status = "✓" if alarm.acknowledged else "✗"
                    lines.append(f"        - [{alarm.severity.upper()}] {alarm.alarm_id}: {alarm.message} (Ack: {ack_status})")
    
    lines.append("\n" + "=" * 50)
    lines.append("Extraction completed successfully.")
    
    return "\n".join(lines)
