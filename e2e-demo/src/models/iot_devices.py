"""IoT device models for sensors and actuators.

Provides dataclasses for representing IoT devices in the edge operator system,
including sensors (temperature, humidity, etc.) and actuators (valves, motors, etc.).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Literal, Optional
import random
from datetime import datetime


@dataclass
class IoTDevice:
    """Base class for all IoT devices.
    
    Attributes:
        device_id: Unique identifier for the device
        device_type: Type of device - either "sensor" or "actuator"
        location: Physical location of the device
        metadata: Additional device-specific information
    """
    device_id: str
    device_type: Literal["sensor", "actuator"]
    location: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SensorDevice(IoTDevice):
    """Sensor device that reads environmental or process values.
    
    Attributes:
        unit: Unit of measurement (e.g., "°C", "%", "PSI")
        min_value: Minimum expected reading value
        max_value: Maximum expected reading value
    """
    unit: str = ""
    min_value: float = 0.0
    max_value: float = 100.0
    
    def __post_init__(self):
        self.device_type = "sensor"
    
    def read(self) -> float:
        """Simulate reading a sensor value within the valid range."""
        return round(random.uniform(self.min_value, self.max_value), 2)


@dataclass
class ActuatorDevice(IoTDevice):
    """Actuator device that can be controlled to change state.
    
    Attributes:
        states: List of valid states the actuator can be in
        current_state: The current state of the actuator
    """
    states: List[str] = field(default_factory=list)
    current_state: str = ""
    
    def __post_init__(self):
        self.device_type = "actuator"
        if self.states and not self.current_state:
            self.current_state = self.states[0]
    
    def set_state(self, new_state: str) -> bool:
        """Set the actuator to a new state if valid.
        
        Args:
            new_state: The desired state to set
            
        Returns:
            True if state was changed, False if invalid state
        """
        if new_state in self.states:
            self.current_state = new_state
            return True
        return False
    
    def get_valid_actions(self) -> List[str]:
        """Return list of valid actions/states for this actuator."""
        return self.states.copy()
