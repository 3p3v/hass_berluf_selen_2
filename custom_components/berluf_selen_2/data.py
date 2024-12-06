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


type SelenConfigEntry = ConfigEntry[SelenData]


# @dataclass
class SelenData:
    """Data for the Berluf Selen 500 integration."""

    def __init__(
        self, intf: Device_async_intf, device: Recup_device, fan_conv: Fan_conv
    ) -> None:
        # Interface used for connecting/disconnecting
        self._intf = intf
        # Slave memory
        self._device = device
        # Task running that needs to be disabled while deleting integration
        self._task: asyncio.Task | None = None
        # Fan speed conversion
        self._fan_conv: Fan_conv = fan_conv

    def get_intf(self) -> Device_async_intf:
        return self._intf

    def get_device(self) -> Recup_device:
        return self._device

    def get_fan_conv(self) -> Fan_conv:
        return self._fan_conv
