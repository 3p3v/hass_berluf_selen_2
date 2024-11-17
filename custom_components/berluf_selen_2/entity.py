"""BlueprintEntity class."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DEV_MANUFACTURER, DEV_MODEL, DEV_NAME

if TYPE_CHECKING:
    from .data import SelenConfigEntry


class SelenEntry:
    """berluf_selen_500 entry."""

    # _attr_attribution = ATTRIBUTION
    _class_id = 0

    def __init__(self, entry: SelenConfigEntry, unique: str | None = None) -> None:
        """Initialize."""
        type(self)._class_id += 1
        if unique is None:
            self._attr_unique_id = entry.entry_id + str(type(self)._class_id)
        else:
            self._attr_unique_id = entry.entry_id + unique

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    entry.domain,
                    entry.entry_id,
                ),
            },
            name=DEV_NAME,
            manufacturer=DEV_MANUFACTURER,
            model=DEV_MODEL,
        )


class SelenAsyncEntry(SelenEntry):
    """berluf_selen_500 entry for async updating."""

    _events: list[asyncio.Event] = []

    def __init__(self, entry: SelenConfigEntry, unique: str | None = None) -> None:
        super().__init__(entry, unique)
        # Push state when callback is called
        self._attr_should_poll: bool = False
