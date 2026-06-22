"""pyfarm-sdk — Python SDK and extension framework.

Provides:
  PyFarmClient       — typed HTTP client for pyfarm-api
  ExtensionRegistry  — plugin system for sensors, actuators, behaviors
  SensorExtension    — base class for custom sensor integrations
  ActuatorExtension  — base class for custom actuator integrations
  BehaviorExtension  — base class for custom domain behavior plugins

Example:
  sdk = PyFarmClient(api_base="http://localhost:8000")
  grow_data = await sdk.get_grow(grow_id="grow-1")
  registry = ExtensionRegistry()
  registry.register_sensor(MyCustomSensor())
"""
from __future__ import annotations

from pyfarm.sdk.client import PyFarmClient
from pyfarm.sdk.extensions import (
    ActuatorExtension,
    BehaviorExtension,
    ExtensionRegistry,
    SensorExtension,
)

__all__ = [
    "PyFarmClient",
    "ExtensionRegistry",
    "SensorExtension",
    "ActuatorExtension",
    "BehaviorExtension",
]
__version__ = "0.1.0"
