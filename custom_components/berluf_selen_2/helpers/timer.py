"""Home Assistant timer implementation for Berluf."""

import asyncio
from collections.abc import Callable
from typing import override

from berluf_selen_2_ctrl.modbus_impl.asyncio.timer import Asyncio_interval_timer
from berluf_selen_2_ctrl.modbus_slave.timer import Timer, Timer_factory
from homeassistant.core import HomeAssistant


class HomeAssistantTimer(Asyncio_interval_timer):
    """Timer starting tasks using HomeAssistant async API."""

    def __init__(
        self,
        timeout: int,
        callb: Callable[[], None],
        interval: int,
        hass: HomeAssistant,
    ):
        super().__init__(timeout, callb, interval)
        self._hass = hass

    @override
    def _run_job(self) -> asyncio.Task:
        return asyncio.create_task(self._job())


class HomeAssistantTimerFactory(Timer_factory):
    """Factory for constructing HomeAssistant timers."""

    def __init__(self, interval: int, hass: HomeAssistant) -> None:
        """Initialize a HomeAssistantTimerFactory factory."""
        super().__init__()
        self._hass = hass
        self._interval = interval

    @override
    def create_timer(self, timeout: int, callb: Callable[[], None]) -> Timer:
        return HomeAssistantTimer(timeout, callb, self._interval, self._hass)
