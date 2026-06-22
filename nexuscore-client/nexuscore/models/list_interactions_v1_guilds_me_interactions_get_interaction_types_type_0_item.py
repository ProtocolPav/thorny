from enum import Enum


class ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item(str, Enum):
    DIE = "die"
    KILL = "kill"
    MINE = "mine"
    PLACE = "place"
    SCRIPTEVENT = "scriptevent"
    USE = "use"

    def __str__(self) -> str:
        return str(self.value)
