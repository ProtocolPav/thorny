from enum import Enum


class ObjectiveUpdateLogicType0(str, Enum):
    AND = "and"
    OR = "or"
    SEQUENTIAL = "sequential"

    def __str__(self) -> str:
        return str(self.value)
