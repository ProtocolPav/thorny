from enum import Enum


class Scope(str, Enum):
    ADMINCLIENTS = "admin:clients"
    ADMINGUILDS = "admin:guilds"
    EVENTSREAD = "events:read"
    EVENTSWRITE = "events:write"
    GUILDSREAD = "guilds:read"
    GUILDSWRITE = "guilds:write"
    GUILDS_MEMBERSREAD = "guilds.members:read"
    GUILDS_MEMBERSWRITE = "guilds.members:write"
    GUILDS_PINSREAD = "guilds.pins:read"
    GUILDS_PINSWRITE = "guilds.pins:write"
    GUILDS_PROJECTSREAD = "guilds.projects:read"
    GUILDS_PROJECTSWRITE = "guilds.projects:write"
    GUILDS_QUESTSREAD = "guilds.quests:read"
    GUILDS_QUESTSWRITE = "guilds.quests:write"
    GUILDS_WIKIREAD = "guilds.wiki:read"
    GUILDS_WIKIWRITE = "guilds.wiki:write"
    SERVERREAD = "server:read"

    def __str__(self) -> str:
        return str(self.value)
