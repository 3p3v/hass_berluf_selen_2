"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from berluf_selen_2.recup.funcs import Exhaust_fan, Fan_conv, Supply_fan
from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import PERCENTAGE

if TYPE_CHECKING:
    from .data import SelenConfigEntry
from .entity import SelenEntry

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SelenConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    async_add_entities(
        [
            SelenExhaustFan(
                entry=entry,
                entity_description=NumberEntityDescription(
                    key="berluf_selen_2",
                    name="Selen exhaust fan",
                    icon="mdi:fan",
                ),
                hass=hass,
                conv=entry.runtime_data.get_fan_conv(),
            ),
            SelenSupplyFan(
                entry=entry,
                entity_description=NumberEntityDescription(
                    key="berluf_selen_2",
                    name="Selen supply fan",
                    icon="mdi:fan",
                ),
                hass=hass,
                conv=entry.runtime_data.get_fan_conv(),
            ),
        ]
    )


class BaseFanEntity(NumberEntity):
    """Class implementing Home Assistant entity update."""

    def __init__(self, hass: HomeAssistant) -> None:
        NumberEntity.__init__(self)
        self._hass = hass

    def call_update_service(self) -> None:
        """Update entity."""
        self.async_write_ha_state()


class SelenSupplyFan(BaseFanEntity, SelenEntry, Supply_fan):
    """berluf_selen_2 fan."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: NumberEntityDescription,
        hass: HomeAssistant,
        conv: Fan_conv,
    ) -> None:
        """Initialize the sensor class."""
        BaseFanEntity.__init__(self, hass)
        SelenEntry.__init__(self, entry, "supply_fan")
        Supply_fan.__init__(self, entry.runtime_data.get_device(), conv)
        self.entity_description = entity_description

        self._attr_native_value: float = float(self.get())
        self._attr_native_max_value: float = 100.0
        self._attr_native_min_value: float = 0.0
        self._attr_native_step: float = 1.0
        self._attr_native_unit_of_measurement = PERCENTAGE

    @override
    def _usr_callback(self, val: int) -> None:
        self._attr_native_value = float(val)
        self.call_update_service()

    @override
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.set(int(value))
        self._attr_native_value = value


class SelenExhaustFan(BaseFanEntity, SelenEntry, Exhaust_fan):
    """berluf_selen_2 fan."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: NumberEntityDescription,
        hass: HomeAssistant,
        conv: Fan_conv,
    ) -> None:
        """Initialize the sensor class."""
        BaseFanEntity.__init__(self, hass)
        SelenEntry.__init__(self, entry, "exhaust_fan")
        Exhaust_fan.__init__(self, entry.runtime_data.get_device(), conv)
        self.entity_description = entity_description

        self._attr_native_value: float = float(self.get())
        self._attr_native_max_value: float = float(self.get_max())
        self._attr_native_min_value: float = float(self.get_min())
        self._attr_native_step: float = 1.0
        self._attr_native_unit_of_measurement = PERCENTAGE

    @override
    def _usr_callback(self, val: int, val_min: int, val_max: int) -> None:
        self._attr_native_value = float(val)
        self._attr_native_max_value = float(val_max)
        self._attr_native_min_value = float(val_min)
        self.call_update_service()

    @override
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.set(int(value))
        self._attr_native_value = value
