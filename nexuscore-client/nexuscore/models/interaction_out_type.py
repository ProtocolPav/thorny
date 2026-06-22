from enum import Enum


class InteractionOutType(str, Enum):
    DIE = "die"
    KILL = "kill"
    MINE = "mine"
    PLACE = "place"
    SCRIPTEVENT = "scriptevent"
    USE = "use"

    def __str__(self) -> str:
        return str(self.value)
