"""Support for AquaLogic devices."""

from __future__ import annotations

from datetime import timedelta
import logging
import threading
import time

# Mod Begin
#from aqualogic.core import AquaLogic
from .core import AquaLogic
#Mod End
import voluptuous as vol

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
# Mod Begin    
    CONF_DEVICE,
# Mod End    
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "aqualogic"
UPDATE_TOPIC = f"{DOMAIN}_update"
CONF_UNIT = "unit"
RECONNECT_INTERVAL = timedelta(seconds=10)
CONF_USESCRIPT = "usescript"
CONF_P4P8 = "p4p8"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_HOST, default="localhost"): cv.string,
                vol.Optional(CONF_PORT, default="4328"): cv.port,
# Mod Begin                
                vol.Optional(CONF_DEVICE, default="socket"): cv.string,
                vol.Optional(CONF_USESCRIPT, default=True): cv.boolean,
                vol.Optional(CONF_P4P8, default="p4"): cv.string,
# Mod End                
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up AquaLogic platform."""
    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
# Mod Begin    
    device = config[DOMAIN][CONF_DEVICE]
    usescript = config[DOMAIN][CONF_USESCRIPT]
    p4p8 = config[DOMAIN][CONF_P4P8]
    processor = AquaLogicProcessor(hass, host, port, device, usescript, p4p8)
#    processor = AquaLogicProcessor(hass, host, port, device)
#    processor = AquaLogicProcessor(hass)    
# Mod End
    hass.data[DOMAIN] = processor
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, processor.start_listen)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, processor.shutdown)
    _LOGGER.debug("AquaLogicProcessor initialized")
    return True


class AquaLogicProcessor(threading.Thread):
    """AquaLogic event processor thread."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, device: str, usescript: bool, p4p8: str) -> None:
#    def __init__(self, hass: HomeAssistant, host: str, port: int, device: str) -> None:
        """Initialize the data object."""
        super().__init__(daemon=True)
        self._hass = hass
        self._host = host
        self._port = port
# Mod Begin        
        self._device = device
        self._usescript = usescript
        self._p4p8 = p4p8
# Mod End        
        self._shutdown = False
        self._panel = None

        
    def start_listen(self, event: Event) -> None:
        """Start event-processing thread."""
        _LOGGER.debug("Event processing thread started")
        self.start()

    def shutdown(self, event: Event) -> None:
        """Signal shutdown of processing event."""
        _LOGGER.debug("Event processing signaled exit")
        self._shutdown = True

    def data_changed(self, panel: AquaLogic) -> None:
        """Aqualogic data changed callback."""
        dispatcher_send(self._hass, UPDATE_TOPIC)

    def run(self) -> None:
        """Event thread."""
# Mod Begin
        panel = AquaLogic()
        self._panel = panel

        while True:
            if self._device == "socket":
                panel.connect(self._host, self._port)
            else:
                panel.connect_serial(self._host)
            panel.process(self.data_changed, self._usescript, self._p4p8)
#            panel.process(self.data_changed)
# Mod End
            if self._shutdown:
                return
            if self._device == "socket":
                _LOGGER.info("Connection to %s:%d lost", self._host, self._port)
            else:
                _LOGGER.info("Connection to %s lost", self._host)
            time.sleep(RECONNECT_INTERVAL.total_seconds())

    @property
    def panel(self) -> AquaLogic | None:
        """Retrieve the AquaLogic object."""
        return self._panel