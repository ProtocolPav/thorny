from enum import Enum


class QuestInQuestType(str, Enum):
    MINOR = "minor"
    SIDE = "side"
    STORY = "story"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
