"""Extension framework for custom sensors, actuators, and behaviors."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SensorExtension(ABC):
    """Base class for custom sensor integrations.

    Example:
        class TemperatureSensor(SensorExtension):
            name = "custom-temp"
            async def read(self):
                return await get_temp_from_hardware()
    """

    name: str

    @abstractmethod
    async def read(self) -> float:
        """Read sensor value; return a float."""
        ...

    async def validate(self) -> list[str]:
        """Validate sensor connectivity. Return list of errors (empty if OK)."""
        return []


class ActuatorExtension(ABC):
    """Base class for custom actuator integrations.

    Example:
        class SmartRelay(ActuatorExtension):
            name = "relay-1"
            async def activate(self, intensity=None):
                await relay_hardware.set_state(intensity or 1.0)
    """

    name: str

    @abstractmethod
    async def activate(self, intensity: float | None = None) -> None:
        """Activate actuator; intensity is 0.0-1.0 (optional)."""
        ...

    @abstractmethod
    async def deactivate(self) -> None:
        """Deactivate actuator."""
        ...


class BehaviorExtension(ABC):
    """Base class for custom domain behavior plugins.

    Example:
        class CustomGrowthCalculator(BehaviorExtension):
            domain = "custom-growth"
            async def compute(self, **params):
                return params.get("height") * 1.1
    """

    domain: str

    @abstractmethod
    async def compute(self, **kwargs: Any) -> Any:
        """Compute domain-specific recommendation."""
        ...


class ExtensionRegistry:
    """Registry for managing custom extensions."""

    def __init__(self) -> None:
        self._sensors: dict[str, SensorExtension] = {}
        self._actuators: dict[str, ActuatorExtension] = {}
        self._behaviors: dict[str, BehaviorExtension] = {}

    def register_sensor(self, sensor: SensorExtension) -> None:
        """Register a sensor extension."""
        if not sensor.name:
            raise ValueError("Sensor must have a name")
        self._sensors[sensor.name] = sensor

    def register_actuator(self, actuator: ActuatorExtension) -> None:
        """Register an actuator extension."""
        if not actuator.name:
            raise ValueError("Actuator must have a name")
        self._actuators[actuator.name] = actuator

    def register_behavior(self, behavior: BehaviorExtension) -> None:
        """Register a behavior extension."""
        if not behavior.domain:
            raise ValueError("Behavior must have a domain")
        self._behaviors[behavior.domain] = behavior

    def get_sensor(self, name: str) -> SensorExtension | None:
        return self._sensors.get(name)

    def get_actuator(self, name: str) -> ActuatorExtension | None:
        return self._actuators.get(name)

    def get_behavior(self, domain: str) -> BehaviorExtension | None:
        return self._behaviors.get(domain)

    def list_sensors(self) -> list[str]:
        return list(self._sensors.keys())

    def list_actuators(self) -> list[str]:
        return list(self._actuators.keys())

    def list_behaviors(self) -> list[str]:
        return list(self._behaviors.keys())
