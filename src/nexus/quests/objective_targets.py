from dataclasses import dataclass
from typing import Union

from nexuscore.models import (
    KillTargetModel,
    MineTargetModel,
    ScriptEventTargetModel,
    VisitTargetModel,
)


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


class MineTarget(MineTargetModel, TargetBase):
    def display_name(self):
        return self.format_minecraft_id(self.block)


class KillTarget(KillTargetModel, TargetBase):
    def display_name(self):
        return self.format_minecraft_id(self.entity)


class ScriptEventTarget(ScriptEventTargetModel, TargetBase):
    def display_name(self):
        return self.script_id


class VisitTarget(VisitTargetModel, TargetBase):
    def display_name(self):
        return self.helper_text


TargetType = Union[MineTarget, KillTarget, ScriptEventTarget, VisitTarget]