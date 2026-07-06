from enum import Enum


class ObjectiveOutObjectiveType(str, Enum):
    KILL = "kill"
    MINE = "mine"
    SCRIPTEVENT = "scriptevent"

    def __str__(self) -> str:
        return str(self.value)
