import asyncio
import copy
from typing import override

from berluf_selen_2_ctrl.modbus_slave.func import Persistant_executor
from homeassistant.helpers.storage import Store

from .const import LOGGER


class HassModbusPersistant:
    """Implements saving modbus memory to persistant storage and loading from it."""

    def __init__(
        self, subkey: str, store: Store[dict[str, dict[int, list[int]]]]
    ) -> None:
        self._subkey = subkey
        self._store = store
        self._mem_await: dict[int, list[int]] | None = None
        self._saving = False

    async def load(self) -> dict[int, list[int]]:
        """Load saved persistant data."""
        data = await self._store.async_load()
        if data is not None:
            data_int = dict[int, list[int]]()
            for a, v in data[self._subkey].items():
                data_int[int(a)] = v

            return data_int
        raise RuntimeError("Error while retreiving saved data: No data found.")

    async def save(self, mem: dict[int, list[int]]) -> None:
        """Save modbus memory to persistant storage."""
        try:
            if not self._saving:
                self._saving = True
                LOGGER.debug(f"Saving memory: {mem}")
                await self._store.async_save({self._subkey: mem})
                while self._mem_await is not None:
                    # Save until there is nothing left
                    mem = copy.deepcopy(
                        self._mem_await
                    )  # Copy in case _mem_await is changed during write TODO(3p3v): check if nessesary
                    self._mem_await = None
                    await self._store.async_save({self._subkey: mem})
                self._saving = False
            else:
                self._mem_await = mem
        except Exception as ec:
            LOGGER.critical(f"Action needed. Cannot save user settings: {ec}")


class HassRecupPersistant(Persistant_executor):
    """Saving modbus memory to persistant storage by non-async method."""

    def __init__(self, impl: HassModbusPersistant) -> None:
        self._impl = impl
        self._task: asyncio.Task | None = None

    @override
    def save(self, mem: dict[int, list[int]]) -> None:
        LOGGER.debug(f"Preparing to save memory: {mem}")
        self._task = asyncio.ensure_future(self._impl.save(mem))
