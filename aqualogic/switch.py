"""Support for AquaLogic switches."""

from __future__ import annotations

from typing import Any

# Mod Begin
#from aqualogic.core import States
from .states import States
# Mod End

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_MONITORED_CONDITIONS
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN, UPDATE_TOPIC, AquaLogicProcessor

SWITCH_TYPES = {
    "lights": "Lights",
    "filter": "Filter",
    "filter_low_speed": "Filter Low Speed",
    "aux_1": "Aux 1",
    "aux_2": "Aux 2",
    "aux_3": "Aux 3",
    "aux_4": "Aux 4",
    "aux_5": "Aux 5",
    "aux_6": "Aux 6",
    "aux_7": "Aux 7",
# Mod Begin
    "pool": "Pool",
    "spa": "Spa",
    "aux_8": "Aux 8",
    "aux_9": "Aux 9",
    "aux_10": "Aux 10",
    "aux_11": "Aux 11",
    "aux_12": "Aux 12",
    "aux_13": "Aux 13",
    "aux_14": "Aux 14",
    "heater_1": "Heater 1",
    "valve_3": "Valve 3",
    "valve_4": "Valve 4",
    "heater_auto_mode": "Heater Auto Mode",
    "super_chlorinate": "Super Chlorinate",
    "service": "Service",
    "right": "Right",
    "left": "Left",
    "menu": "Menu",
    "minus": "Minus",
    "plus": "Plus",
# Mod End           
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SWITCH_TYPES)): vol.All(
            cv.ensure_list, [vol.In(SWITCH_TYPES)]
        )
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the switch platform."""
    processor: AquaLogicProcessor = hass.data[DOMAIN]

    async_add_entities(
        AquaLogicSwitch(processor, switch_type)
        for switch_type in config[CONF_MONITORED_CONDITIONS]
    )


class AquaLogicSwitch(SwitchEntity):
    """Switch implementation for the AquaLogic component."""

    _attr_should_poll = False

    def __init__(self, processor: AquaLogicProcessor, switch_type: str) -> None:
        """Initialize switch."""
        self._processor = processor
        self._state_name = {
            "lights": States.LIGHTS,
            "filter": States.FILTER,
            "filter_low_speed": States.FILTER_LOW_SPEED,
            "aux_1": States.AUX_1,
            "aux_2": States.AUX_2,
            "aux_3": States.AUX_3,
            "aux_4": States.AUX_4,
            "aux_5": States.AUX_5,
            "aux_6": States.AUX_6,
            "aux_7": States.AUX_7,
 # Mod Begin
            "pool": States.POOL,
            "spa": States.SPA,
            "aux_8": States.AUX_8,
            "aux_9": States.AUX_9,
            "aux_10": States.AUX_10,
            "aux_11": States.AUX_11,
            "aux_12": States.AUX_12,
            "aux_13": States.AUX_13,
            "aux_14": States.AUX_14,
            "heater_1": States.HEATER_1,
            "valve_3": States.VALVE_3,
            "valve_4": States.VALVE_4,
            "heater_auto_mode": States.HEATER_AUTO_MODE,
            "super_chlorinate": States.SUPER_CHLORINATE,
            "service": States.SERVICE,
# These should be buttons, but it was a quick add as switches
            "right": States.RIGHT,
            "left": States.LEFT,
            "menu": States.MENU,
            "minus": States.MINUS,
            "plus": States.PLUS,
# Mod End
        }[switch_type]
        self._attr_name = f"AquaLogic {SWITCH_TYPES[switch_type]}"
# Mod - Give switches a unique_id so they can be edited in HA UI - Begin
        self._attr_unique_id = f"Aqualogic_{switch_type}"
# Mod End

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        if (panel := self._processor.panel) is None:
            return False
        return panel.get_state(self._state_name)  # type: ignore[no-any-return]

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        if (panel := self._processor.panel) is None:
            return
        panel.set_state(self._state_name, True)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        if (panel := self._processor.panel) is None:
            return
        panel.set_state(self._state_name, False)

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        self.async_on_remove(
            async_dispatcher_connect(self.hass, UPDATE_TOPIC, self.async_write_ha_state)
        )