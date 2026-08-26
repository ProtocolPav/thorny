from enum import Enum


class ObjectiveOutObjectiveType(str, Enum):
    KILL = "kill"
    MINE = "mine"
    SCRIPTEVENT = "scriptevent"
    VISIT = "visit"

    def __str__(self) -> str:
        return str(self.value)
