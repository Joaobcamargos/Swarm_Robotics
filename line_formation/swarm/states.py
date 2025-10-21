from enum import Enum, auto

class RobotStatus(Enum):
    GROUP = auto()
    LEADER = auto()
    IN_LINE = auto()
    FINISHED = auto()