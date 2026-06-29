from dataclasses import dataclass
from typing import Union


@dataclass
class TargetBase:
    target_uuid: str
    target_type: str
    count: int

    @staticmethod
    def format_minecraft_id(id_str: str) -> str:
        if ':' in id_str:
            return id_str.split(':')[1].replace('_', ' ').title()
        return id_str.replace('_', ' ').title()

    def display_name(self):
        pass


@dataclass
class MineTarget(TargetBase):
    block: str

    def display_name(self):
        return self.format_minecraft_id(self.block)


@dataclass
class KillTarget(TargetBase):
    entity: str

    def display_name(self):
        return self.format_minecraft_id(self.entity)


@dataclass
class ScriptEventTarget(TargetBase):
    script_id: str

    def display_name(self):
        return self.script_id


TargetType = Union[MineTarget, KillTarget, ScriptEventTarget]