from enum import Enum

class Modes(Enum):
    BASIC = 'basic'
    ADVANCED = 'advanced'

class OnOff(Enum):
    ON = 'on'
    OFF = 'off'

class DeleteNoDelete(Enum):
    DELETE = 'delete'
    NO_DELETE = 'no_delete'