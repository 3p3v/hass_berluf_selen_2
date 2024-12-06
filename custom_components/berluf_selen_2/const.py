"""Definitions for berluf_selen_500."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "berluf_selen_2"
DEV_NAME = "Recuperator"
DEV_MANUFACTURER = "Berluf"
DEV_MODEL = "Selen 2"

# Store definitions
LAST_SET = "last_set"
USER_MODE = "usr_mode"


def get_default_store_name(entry_id: str) -> str:
    """Get persistant storage name."""
    return entry_id + LAST_SET
