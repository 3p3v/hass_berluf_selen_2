"""Config flow for berluf_selen_500."""

from __future__ import annotations

from enum import Enum

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_PORT
from homeassistant.helpers import selector

from .const import DOMAIN

# Conversion
CONV_TYPE = "Fans speed conversion"


class ConvType(Enum):
    """Fan speed conversion options."""

    OFF = 0
    LINEAR = 1


# Intefrace
INTF_TYPE = "Interface type"


class IntfType(Enum):
    """Types of interfaces (low-level connection with recuperator)."""

    SERIAL = 0


_data: dict[str, str] = {}


class SelenFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            # Check if fan speed conversion was set
            conv_type = user_input.get(CONV_TYPE)
            intf_type = user_input.get(INTF_TYPE)
            conf_port = user_input.get(CONF_PORT)
            if conv_type is not None and intf_type is not None:
                # Update data
                _data[CONV_TYPE] = conv_type
                _data[INTF_TYPE] = intf_type

                # Conversion and interface already set, get interface specyfic data
                match user_input[INTF_TYPE]:
                    case IntfType.SERIAL.name:
                        # Specify serial port
                        return self.async_show_form(
                            step_id="user",
                            data_schema=vol.Schema(
                                {
                                    vol.Required(
                                        CONF_PORT,
                                        default=(user_input or {}).get(
                                            CONF_PORT, vol.UNDEFINED
                                        ),
                                    ): selector.TextSelector(
                                        selector.TextSelectorConfig(
                                            type=selector.TextSelectorType.TEXT,
                                        ),
                                    ),
                                },
                            ),
                            errors=_errors,
                        )

                # Interface not recognised
                raise RuntimeError(f"Unknown interface type: {user_input[INTF_TYPE]}.")
            if conf_port is not None:
                # All data aquired
                _data[CONF_PORT] = conf_port
                return self.async_create_entry(
                    title=user_input[CONF_PORT],
                    data=_data,
                )

        # First select interface type
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONV_TYPE,
                    ): selector.SelectSelector(
                        config=selector.SelectSelectorConfig(
                            options=[ct.name for ct in ConvType]
                        )
                    ),
                    vol.Required(
                        INTF_TYPE,
                    ): selector.SelectSelector(
                        config=selector.SelectSelectorConfig(
                            options=[it.name for it in IntfType]
                        )
                    ),
                },
            ),
            errors=_errors,
        )
