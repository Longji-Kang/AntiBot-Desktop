from BusinessLogic.StateEnums import Modes, OnOff

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.LoggingComponent import LoggingComponentClass

class ConfigurationState:
    mode: Modes = Modes.BASIC
    state: OnOff = OnOff.ON

    subsystem = 'Config'
    @staticmethod
    def setMode(mode: Modes, logger: LoggingComponentClass):
        ConfigurationState.mode = mode
        logger.log(f'Changed mode to {mode.value}', ConfigurationState.subsystem)

    @staticmethod
    def getMode() -> Modes:
        return ConfigurationState.mode
    
    @staticmethod
    def setOnOff(state: OnOff, logger: LoggingComponentClass):
        ConfigurationState.state = state
        logger.log(f'Changed on/off state to {state.value}', ConfigurationState.subsystem)

    @staticmethod
    def getOnOff() -> OnOff:
        return ConfigurationState.state