from enum import Enum


class StatusEnum(str, Enum):
    ABANDONED = "abandoned"
    COMPLETED = "completed"
    ONGOING = "ongoing"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
