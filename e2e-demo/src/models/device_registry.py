"""Device registry for managing IoT devices.

Provides a registry of available IoT devices with sample devices
for temperature sensing, humidity sensing, and valve control.
"""

from typing import Dict, Optional, List, Union
from .iot_devices import IoTDevice, SensorDevice, ActuatorDevice


class DeviceRegistry:
    """Registry for managing IoT devices.
    
    Provides methods to register, retrieve, and list devices.
    """
    
    def __init__(self):
        self._devices: Dict[str, Union[SensorDevice, ActuatorDevice]] = {}
    
    def register(self, device: Union[SensorDevice, ActuatorDevice]) -> None:
        """Register a device in the registry."""
        self._devices[device.device_id] = device
    
    def get(self, device_id: str) -> Optional[Union[SensorDevice, ActuatorDevice]]:
        """Get a device by ID, returns None if not found."""
        return self._devices.get(device_id)
    
    def list_devices(self) -> List[Union[SensorDevice, ActuatorDevice]]:
        """Return list of all registered devices."""
        return list(self._devices.values())
    
    def list_device_ids(self) -> List[str]:
        """Return list of all device IDs."""
        return list(self._devices.keys())
    
    def get_sensors(self) -> List[SensorDevice]:
        """Return list of all sensor devices."""
        return [d for d in self._devices.values() if isinstance(d, SensorDevice)]
    
    def get_actuators(self) -> List[ActuatorDevice]:
        """Return list of all actuator devices."""
        return [d for d in self._devices.values() if isinstance(d, ActuatorDevice)]


def create_default_registry() -> DeviceRegistry:
    """Create a device registry with sample devices.
    
    Returns:
        DeviceRegistry populated with sample IoT devices
    """
    registry = DeviceRegistry()
    
    # Temperature sensor
    temp_sensor = SensorDevice(
        device_id="temp-sensor",
        device_type="sensor",
        location="Production Floor - Zone A",
        metadata={"manufacturer": "SensorCorp", "model": "TC-100"},
        unit="°C",
        min_value=-10.0,
        max_value=50.0
    )
    registry.register(temp_sensor)
    
    # Humidity sensor
    humidity_sensor = SensorDevice(
        device_id="humidity-sensor",
        device_type="sensor",
        location="Production Floor - Zone A",
        metadata={"manufacturer": "SensorCorp", "model": "HC-200"},
        unit="%",
        min_value=0.0,
        max_value=100.0
    )
    registry.register(humidity_sensor)
    
    # Valve actuator
    valve_actuator = ActuatorDevice(
        device_id="valve-actuator",
        device_type="actuator",
        location="Cooling System - Main Line",
        metadata={"manufacturer": "ActuatorTech", "model": "VA-500"},
        states=["open", "closed", "partial"],
        current_state="closed"
    )
    registry.register(valve_actuator)
    
    return registry


# Global default registry instance
default_registry = create_default_registry()
