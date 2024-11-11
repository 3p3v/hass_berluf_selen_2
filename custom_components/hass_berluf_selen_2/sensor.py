"""Sensor platform for integration_blueprint."""

from __future__ import annotations

import asyncio
import decimal
from typing import TYPE_CHECKING, Any

from berluf_selen_2.modbus_impl.asyncio.timer import Asyncio_timer_factory
from berluf_selen_2.modbus_slave.intf import Device_async_intf
from berluf_selen_2.recup.funcs import (
    Error,
    Thermometer_01,
    Thermometer_02,
    Thermometer_03,
    Thermometer_04,
    Thermometer_05,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import UnitOfTemperature

if TYPE_CHECKING:
    from .data import SelenConfigEntry
from .const import LOGGER
from .entity import SelenAsyncEntry

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SelenConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    timer = SelenError(
        entry=entry,
        entity_description=SensorEntityDescription(
            key="berluf_selen_2",
            name="Selen error indicator",
        ),
    )
    entry.runtime_data.set_timer(timer)
    conn_intf = SelenConnection(
        entry=entry,
        entity_description=SensorEntityDescription(
            key="berluf_selen_2",
            name="Selen connection status",
        ),
    )
    entry.runtime_data.set_task(asyncio.ensure_future(conn_intf.connect()))

    async_add_entities(
        [
            SelenThermometer(
                thermometer_class=c,
                thermometer_name=n,
                entry=entry,
                entity_description=SensorEntityDescription(
                    key="berluf_selen_2",
                    name=f"Selen temp. {n}",
                ),
            )
            for c, n in [
                (Thermometer_01, "01"),
                (Thermometer_02, "02"),
                (Thermometer_03, "03"),
                (Thermometer_04, "04"),
                (Thermometer_05, "05"),
            ]
        ]
        + [
            conn_intf,
            timer,
        ]
    )


class SelenThermometer(SelenAsyncEntry, SensorEntity):
    """berluf_selen_2 thermometer."""

    def __init__(
        self,
        thermometer_class: Any,
        thermometer_name: str,  # TODO(@3p3v): delete, do not set name at all
        entry: SelenConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry, thermometer_name)
        self._impl = thermometer_class(
            entry.runtime_data.get_device(), self._usr_callback
        )
        self.entity_description = entity_description
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self.no_error_detected()

    def _usr_callback(self, val: int) -> None:
        self.async_write_ha_state()

    @property
    def native_value(self) -> decimal.Decimal | None:
        """Return the native value of the sensor."""
        temp = self._impl.get()
        if temp == int("11111111", 2):
            self.error_detected()
            return None

        self.no_error_detected()
        return decimal.Decimal(temp)

    def no_error_detected(self) -> None:
        """Set no error icon.."""
        self._attr_icon = "mdi:thermometer"

    def error_detected(self) -> None:
        """Set error icon.."""
        self._attr_icon = "mdi:alert"


class BaseErrorEntity(SensorEntity):
    """Base class for error entities."""

    def __init__(self) -> None:
        """Initialize base error entity class."""
        SensorEntity().__init__()
        self.no_error_detected()

    def no_error_detected(self) -> None:
        """Set no error icon.."""
        self._attr_icon = "mdi:alert-circle-check"

    def error_detected(self) -> None:
        """Set error icon.."""
        self._attr_icon = "mdi:alert-circle"


class SelenError(SelenAsyncEntry, BaseErrorEntity):
    """berluf_selen_2 error indicator."""

    _STATE_OK = "OK"

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        SelenAsyncEntry.__init__(self, entry, "error")
        BaseErrorEntity.__init__(self)
        self.entity_description = entity_description

        self._impl = Error(
            entry.runtime_data.get_device(), Asyncio_timer_factory(), self._callb
        )
        self._ec: str = self._STATE_OK

    def _callb(self, ecs: list[Error.Error]) -> None:
        # Save errors
        if len(ecs) == 0:
            self.no_error_detected()
            self._ec = self._STATE_OK
        else:
            self.error_detected()
            self._ec = ecs[0].name
            for e in ecs[1:]:
                self._ec += f", {e.name}"

        # Try fixing recuperator
        self._impl.reset()

        self.async_write_ha_state()

    def cancel(self) -> None:
        """Cancel timer (call when object needs to be deleted)."""
        self._impl.cancel()

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self._ec


class SelenConnection(SelenAsyncEntry, BaseErrorEntity):
    """berluf_selen_2 connection status."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        SelenAsyncEntry.__init__(self, entry, "connection")
        BaseErrorEntity.__init__(self)
        self.entity_description = entity_description

        self._intf = entry.runtime_data.get_intf()

    async def connect(self) -> None:
        """Connect to the intefrace, reconnect on error, until shutdown."""
        if self._intf.get_state() in (
            Device_async_intf.State.CONNECTING,
            Device_async_intf.State.CONNECTED,
        ):
            LOGGER.error("Called connect twice.")
            return

        while True:
            LOGGER.debug("Connecting to specyfied interface...")
            state = await self._intf.connect()
            LOGGER.debug(f"Connection state {state}")

            if state == Device_async_intf.State.CONNECTED:
                LOGGER.info("Connected.")
                self.no_error_detected()
                self.async_write_ha_state()
                state = await self._intf.wait_state_change()

            if state == Device_async_intf.State.DISCONNECTED:
                self.async_write_ha_state()
                LOGGER.info("Disconnected gently.")
                return

            self.error_detected()
            self.async_write_ha_state()
            LOGGER.error(f"Disconnected from interface, reason: {state}")
            await asyncio.sleep(5)

    async def disconnect(self) -> None:
        """Disconnect from the interface."""
        await self._intf.disconnect()
        self.error_detected()

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self._intf.get_state().name
