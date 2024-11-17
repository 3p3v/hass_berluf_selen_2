"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from berluf_selen_2_ctrl.recup.funcs import Heater_cooler
from homeassistant.components.select import SelectEntity, SelectEntityDescription

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
    """Set up the select platform."""
    async_add_entities(
        [
            SelenHeaterCooler(
                entry=entry,
                entity_description=SelectEntityDescription(
                    key="berluf_selen_2",
                    name="Selen heater cooler switch",
                    options=Heater_cooler.Mode._member_names_,
                    icon="mdi:sun-snowflake-variant",
                ),
                hass=hass,
            ),
        ]
    )


class SelenHeaterCooler(SelectEntity, SelenEntry, Heater_cooler):
    """berluf_selen_2 heater cooler switch."""

    def __init__(
        self,
        entry: SelenConfigEntry,
        entity_description: SelectEntityDescription,
        hass: HomeAssistant,
    ) -> None:
        """Initialize the sensor class."""
        SelectEntity.__init__(self)
        SelenEntry.__init__(self, entry, "heater_cooler")
        Heater_cooler.__init__(self, entry.runtime_data.get_device())
        self.entity_description = entity_description

        self._hass = hass

    @override
    def _usr_callback(self, val: Heater_cooler.Mode) -> None:
        self.async_write_ha_state()

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        return self.get().name

    @override
    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self.set(Heater_cooler.Mode[option])
