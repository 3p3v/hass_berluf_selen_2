"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from berluf_selen_2.recup.funcs import GWC
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

if TYPE_CHECKING:
    from .data import SelenConfigEntry
from .entity import SelenAsyncEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SelenConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        [
            SelenGWC(
                entry=entry,
                entity_description=SwitchEntityDescription(
                    key="berluf_selen_2",
                    name="Selen GWC switch",
                ),
                hass=hass,
            ),
        ]
    )


class SelenGWC(SelenAsyncEntry, SwitchEntity, GWC):
    """berluf_selen_2 heater cooler switch."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: SwitchEntityDescription,
        hass: HomeAssistant,
    ) -> None:
        """Initialize the sensor class."""
        SwitchEntity.__init__(self)
        SelenAsyncEntry.__init__(self, entry, "GWC")
        GWC.__init__(self, entry.runtime_data.get_device())
        self.entity_description = entity_description
        self._hass = hass

    @override
    def _usr_callback(self, val: bool) -> None:
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.get()

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.set(True)

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.set(False)
