from BusinessLogic.ModeEnum import Modes

class ConfigurationState:
    state: Modes = Modes.BASIC

    @staticmethod
    def setState(mode: Modes):
        ConfigurationState.state = mode

    @staticmethod
    def getState() -> Modes:
        return ConfigurationState.state