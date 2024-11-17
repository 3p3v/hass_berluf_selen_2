"""Custom types for berluf_selen_500"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

# Underlying recuperator implementation
from berluf_selen_2_ctrl.modbus_slave.intf import Device_async_intf
from berluf_selen_2_ctrl.recup.device import Recup_device
from berluf_selen_2_ctrl.recup.funcs import Fan_conv

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


type SelenConfigEntry = ConfigEntry[SelenData]


# @dataclass
class SelenData:
    """Data for the Berluf Selen 500 integration."""

    def __init__(
        self,
        intf: Device_async_intf,
        device: Recup_device,
        fan_conv: Fan_conv,
        hass: HomeAssistant,
    ) -> None:
        # Interface used for connecting/disconnecting
        self._intf = intf
        # Slave memory
        self._device = device
        # Timer that needs to be disabled while deleting integration; TODO set type
        self._timer = None
        # Task running that needs to be disabled while deleting integration
        self._task: asyncio.Task | None = None
        # Fan speed conversion
        self._fan_conv: Fan_conv = fan_conv

        self._hass = hass

    def get_intf(self) -> Device_async_intf:
        return self._intf

    def get_device(self) -> Recup_device:
        return self._device

    def set_timer(self, timer) -> None:
        if self._timer is None:
            self._timer = timer
        else:
            raise RuntimeError("Timer has already been set.")

    def get_timer(self):
        if self._timer is not None:
            return self._timer
        raise RuntimeError("Timer hasn't been set yet.")

    def set_task(self, task: asyncio.Task):
        if self._task is None:
            self._task = task
        else:
            raise RuntimeError("Task has already been set.")

    def get_task(self):
        if self._task is not None:
            return self._task
        raise RuntimeError("Task hasn't been set yet.")

    def get_fan_conv(self):
        return self._fan_conv

    def get_hass(self) -> HomeAssistant:
        return self._hass
