from enum import Enum


class QuestUpdateQuestTypeType0(str, Enum):
    MINOR = "minor"
    SIDE = "side"
    STORY = "story"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
