from enum import Enum


class ObjectiveProgressOutStatus(str, Enum):
    ABANDONED = "abandoned"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
