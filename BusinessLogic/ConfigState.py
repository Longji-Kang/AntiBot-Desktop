from BusinessLogic.ModeEnum import Modes

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.LoggingComponent import LoggingComponentClass

class ConfigurationState:
    state: Modes = Modes.BASIC
    subsystem = 'Config'
    @staticmethod
    def setState(mode: Modes, logger: LoggingComponentClass):
        ConfigurationState.state = mode
        logger.log(f'Changed mode to {mode.value}', ConfigurationState.subsystem)

    @staticmethod
    def getState() -> Modes:
        return ConfigurationState.state