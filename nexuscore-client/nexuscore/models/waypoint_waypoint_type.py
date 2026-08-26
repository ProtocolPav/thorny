from enum import Enum


class WaypointWaypointType(str, Enum):
    QUESTION = "question"
    STAR = "star"

    def __str__(self) -> str:
        return str(self.value)
