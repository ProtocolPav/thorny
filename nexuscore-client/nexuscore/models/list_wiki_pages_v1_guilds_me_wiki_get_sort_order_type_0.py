from enum import Enum


class ListWikiPagesV1GuildsMeWikiGetSortOrderType0(str, Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
