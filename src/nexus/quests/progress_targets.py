from dataclasses import dataclass


@dataclass
class TargetProgressBase:
    target_uuid: str
    target_type: str
    count: int


@dataclass
class MineTargetProgress(TargetProgressBase):
    pass


@dataclass
class KillTargetProgress(TargetProgressBase):
    pass


@dataclass
class ScriptEventTargetProgress(TargetProgressBase):
    pass