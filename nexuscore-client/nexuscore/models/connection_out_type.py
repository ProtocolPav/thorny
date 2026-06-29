from enum import Enum


class ConnectionOutType(str, Enum):
    CONNECT = "connect"
    DISCONNECT = "disconnect"

    def __str__(self) -> str:
        return str(self.value)
