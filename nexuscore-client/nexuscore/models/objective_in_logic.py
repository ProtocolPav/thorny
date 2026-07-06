from enum import Enum


class ObjectiveInLogic(str, Enum):
    AND = "and"
    OR = "or"
    SEQUENTIAL = "sequential"

    def __str__(self) -> str:
        return str(self.value)
