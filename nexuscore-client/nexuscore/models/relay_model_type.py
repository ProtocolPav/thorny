from enum import Enum


class RelayModelType(str, Enum):
    CRASH = "crash"
    JOIN = "join"
    LEAVE = "leave"
    MESSAGE = "message"
    OTHER = "other"
    START = "start"
    STOP = "stop"

    def __str__(self) -> str:
        return str(self.value)
