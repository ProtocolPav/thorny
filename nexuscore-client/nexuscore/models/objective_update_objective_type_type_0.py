from enum import Enum


class ObjectiveUpdateObjectiveTypeType0(str, Enum):
    KILL = "kill"
    MINE = "mine"
    SCRIPTEVENT = "scriptevent"

    def __str__(self) -> str:
        return str(self.value)
