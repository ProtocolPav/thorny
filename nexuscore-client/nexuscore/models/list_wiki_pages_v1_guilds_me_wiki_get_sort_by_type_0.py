from enum import Enum


class ListWikiPagesV1GuildsMeWikiGetSortByType0(str, Enum):
    CREATED_AT = "created_at"
    TITLE = "title"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
