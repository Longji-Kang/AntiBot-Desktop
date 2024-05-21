from BusinessLogic.StateEnums import Modes, OnOff, DeleteNoDelete

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.LoggingComponent import LoggingComponentClass

class ConfigurationState:
    mode: Modes = Modes.BASIC
    state: OnOff = OnOff.ON
    delete: DeleteNoDelete = DeleteNoDelete.DELETE

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
    
    @staticmethod
    def setDelete(delete: DeleteNoDelete, logger: LoggingComponentClass):
        ConfigurationState.delete = delete
        logger.log(f'Changed action to {delete.value}', ConfigurationState.subsystem)

    @staticmethod
    def getDelete() -> DeleteNoDelete:
        return ConfigurationState.delete