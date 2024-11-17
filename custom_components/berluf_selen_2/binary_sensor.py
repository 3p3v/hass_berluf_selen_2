"""Binary sensor platform for berluf_selen_2."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from berluf_selen_2_ctrl.recup.funcs import Bypass, Heater, Pump
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

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
    """Set up the binary_sensor platform."""
    async_add_entities(
        [
            SelenBypass(
                entry=entry,
                entity_description=BinarySensorEntityDescription(
                    key="berluf_selen_2",
                    name="Selen bypass",
                    device_class=BinarySensorDeviceClass.OPENING,
                ),
            ),
            SelenHeater(
                entry=entry,
                entity_description=BinarySensorEntityDescription(
                    key="berluf_selen_2", name="Selen heater", device_class=None
                ),
            ),
            SelenPump(
                entry=entry,
                entity_description=BinarySensorEntityDescription(
                    key="berluf_selen_2", name="Selen pump", device_class=None
                ),
            ),
        ]
    )


class SelenBypass(SelenAsyncEntry, BinarySensorEntity, Bypass):
    """berluf_selen_2 bypass indicator."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        BinarySensorEntity.__init__(self)
        SelenAsyncEntry.__init__(self, entry, "bypass")
        Bypass.__init__(self, entry.runtime_data.get_device())
        self.entity_description = entity_description

    @override
    def _usr_callback(self, val: bool) -> None:
        LOGGER.debug(f"Bypass: {self.get()}")
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return state of the recuperators bypass (True = ON)."""
        LOGGER.debug(f"Bypass reading: {self.get()}")
        return self.get()


class SelenHeater(SelenAsyncEntry, BinarySensorEntity, Heater):
    """berluf_selen_2 heater indicator."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        BinarySensorEntity.__init__(self)
        SelenAsyncEntry.__init__(self, entry, "heater")
        Heater.__init__(self, entry.runtime_data.get_device())
        self.entity_description = entity_description

    @override
    def _usr_callback(self, val: bool) -> None:
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return state of the recuperators bypass (True = ON)."""
        return self.get()


class SelenPump(SelenAsyncEntry, BinarySensorEntity, Pump):
    """berluf_selen_2 pump indicator."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        BinarySensorEntity.__init__(self)
        SelenAsyncEntry.__init__(self, entry, "pump")
        Pump.__init__(self, entry.runtime_data.get_device())
        self.entity_description = entity_description

    @override
    def _usr_callback(self, val: bool) -> None:
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return state of the recuperators bypass (True = ON)."""
        return self.get()
