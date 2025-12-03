"""IoT tools for sensor reading and actuator control.

Provides tools for the Edge Operator Agent to interact with IoT devices
including reading sensor values and controlling actuators.
"""

from strands import tool
from typing import Optional
from datetime import datetime

from ..models.device_registry import default_registry
from ..models.iot_devices import SensorDevice, ActuatorDevice


@tool
def read_sensor(device_id: str) -> str:
    """Read current sensor values from an IoT device.
    
    Args:
        device_id: The unique identifier of the sensor device to read
        
    Returns:
        A formatted string containing device info and the current reading,
        or an error message if the device is not found or not a sensor.
    """
    device = default_registry.get(device_id)
    
    if device is None:
        available_ids = default_registry.list_device_ids()
        return f"Error: Device '{device_id}' not found. Available devices: {', '.join(available_ids)}"
    
    if not isinstance(device, SensorDevice):
        return f"Error: Device '{device_id}' is not a sensor. It is a {device.device_type}."
    
    # Read the sensor value
    reading = device.read()
    timestamp = datetime.now().isoformat()
    
    return (
        f"Sensor Reading:\n"
        f"  Device ID: {device.device_id}\n"
        f"  Type: {device.device_type}\n"
        f"  Location: {device.location}\n"
        f"  Value: {reading} {device.unit}\n"
        f"  Timestamp: {timestamp}"
    )


@tool
def control_device(device_id: str, action: str) -> str:
    """Send a control command to an IoT actuator device.
    
    Args:
        device_id: The unique identifier of the actuator device to control
        action: The action/state to set the actuator to
        
    Returns:
        A confirmation message if successful, or an error message if the
        device is not found, not an actuator, or the action is invalid.
    """
    device = default_registry.get(device_id)
    
    if device is None:
        available_ids = default_registry.list_device_ids()
        return f"Error: Device '{device_id}' not found. Available devices: {', '.join(available_ids)}"
    
    if not isinstance(device, ActuatorDevice):
        return f"Error: Device '{device_id}' is not an actuator. It is a {device.device_type}."
    
    # Validate and execute the action
    valid_actions = device.get_valid_actions()
    if action not in valid_actions:
        return (
            f"Error: Invalid action '{action}' for device '{device_id}'.\n"
            f"Valid actions: {', '.join(valid_actions)}"
        )
    
    previous_state = device.current_state
    success = device.set_state(action)
    timestamp = datetime.now().isoformat()
    
    if success:
        return (
            f"Device Control Successful:\n"
            f"  Device ID: {device.device_id}\n"
            f"  Type: {device.device_type}\n"
            f"  Location: {device.location}\n"
            f"  Previous State: {previous_state}\n"
            f"  New State: {device.current_state}\n"
            f"  Timestamp: {timestamp}"
        )
    else:
        return f"Error: Failed to set device '{device_id}' to state '{action}'."


@tool
def list_devices() -> str:
    """List all available IoT devices.
    
    Returns:
        A formatted string listing all registered devices with their
        type, location, and relevant details.
    """
    devices = default_registry.list_devices()
    
    if not devices:
        return "No devices registered in the system."
    
    lines = ["Available IoT Devices:", "=" * 40]
    
    for device in devices:
        lines.append(f"\nDevice ID: {device.device_id}")
        lines.append(f"  Type: {device.device_type}")
        lines.append(f"  Location: {device.location}")
        
        if isinstance(device, SensorDevice):
            lines.append(f"  Unit: {device.unit}")
            lines.append(f"  Range: {device.min_value} - {device.max_value}")
        elif isinstance(device, ActuatorDevice):
            lines.append(f"  Valid States: {', '.join(device.states)}")
            lines.append(f"  Current State: {device.current_state}")
    
    lines.append("\n" + "=" * 40)
    lines.append(f"Total: {len(devices)} device(s)")
    
    return "\n".join(lines)
