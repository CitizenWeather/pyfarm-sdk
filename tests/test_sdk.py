"""Smoke tests for pyfarm-sdk."""
from __future__ import annotations

import pytest

from pyfarm.sdk import (
    ActuatorExtension,
    BehaviorExtension,
    ExtensionRegistry,
    PyFarmClient,
    SensorExtension,
)


# ---------------------------------------------------------------------------
# PyFarmClient
# ---------------------------------------------------------------------------

def test_pyfarm_client_initialization():
    client = PyFarmClient(api_base="http://localhost:8000")
    assert client.api_base == "http://localhost:8000"
    assert client.timeout == 30.0


def test_pyfarm_client_with_auth():
    client = PyFarmClient(api_base="http://api.farm", auth_token="secret")
    assert client.auth_token == "secret"


async def test_pyfarm_client_close():
    client = PyFarmClient()
    await client.close()


# ---------------------------------------------------------------------------
# SensorExtension
# ---------------------------------------------------------------------------

class MockSensor(SensorExtension):
    name = "mock-sensor"

    async def read(self) -> float:
        return 23.5


async def test_sensor_extension():
    sensor = MockSensor()
    value = await sensor.read()
    assert value == 23.5
    errors = await sensor.validate()
    assert errors == []


# ---------------------------------------------------------------------------
# ActuatorExtension
# ---------------------------------------------------------------------------

class MockActuator(ActuatorExtension):
    name = "mock-actuator"
    state: bool = False

    async def activate(self, intensity: float | None = None) -> None:
        self.state = True

    async def deactivate(self) -> None:
        self.state = False


async def test_actuator_extension():
    actuator = MockActuator()
    assert not actuator.state
    await actuator.activate()
    assert actuator.state
    await actuator.deactivate()
    assert not actuator.state


# ---------------------------------------------------------------------------
# BehaviorExtension
# ---------------------------------------------------------------------------

class MockBehavior(BehaviorExtension):
    domain = "mock-domain"

    async def compute(self, **kwargs) -> float:
        return kwargs.get("value", 0.0) * 2.0


async def test_behavior_extension():
    behavior = MockBehavior()
    result = await behavior.compute(value=10.0)
    assert result == 20.0


# ---------------------------------------------------------------------------
# ExtensionRegistry
# ---------------------------------------------------------------------------

async def test_extension_registry_register_sensor():
    registry = ExtensionRegistry()
    sensor = MockSensor()
    registry.register_sensor(sensor)
    assert registry.get_sensor("mock-sensor") is sensor


async def test_extension_registry_register_actuator():
    registry = ExtensionRegistry()
    actuator = MockActuator()
    registry.register_actuator(actuator)
    assert registry.get_actuator("mock-actuator") is actuator


async def test_extension_registry_register_behavior():
    registry = ExtensionRegistry()
    behavior = MockBehavior()
    registry.register_behavior(behavior)
    assert registry.get_behavior("mock-domain") is behavior


async def test_extension_registry_list():
    registry = ExtensionRegistry()
    registry.register_sensor(MockSensor())
    registry.register_actuator(MockActuator())
    registry.register_behavior(MockBehavior())
    assert "mock-sensor" in registry.list_sensors()
    assert "mock-actuator" in registry.list_actuators()
    assert "mock-domain" in registry.list_behaviors()


async def test_extension_registry_sensor_requires_name():
    registry = ExtensionRegistry()

    class BadSensor(SensorExtension):
        name = ""

        async def read(self) -> float:
            return 0.0

    with pytest.raises(ValueError, match="must have a name"):
        registry.register_sensor(BadSensor())
