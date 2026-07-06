from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.objective_out_logic import ObjectiveOutLogic
from ..models.objective_out_objective_type import ObjectiveOutObjectiveType

if TYPE_CHECKING:
    from ..models.customizations import Customizations
    from ..models.kill_target_model import KillTargetModel
    from ..models.mine_target_model import MineTargetModel
    from ..models.reward_out import RewardOut
    from ..models.script_event_target_model import ScriptEventTargetModel


T = TypeVar("T", bound="ObjectiveOut")


@_attrs_define
class ObjectiveOut:
    """
    Attributes:
        objective_id (int): The ID of the objective
        description (str): The description of the objective
        display (None | str):
        order_index (int): The order of the objective. Starts at 0.
        objective_type (ObjectiveOutObjectiveType): The type of objective: kill, mine or scriptevent
        logic (ObjectiveOutLogic): The logic to be applied to the objective targets
        target_count (int | None):
        targets (list[KillTargetModel | MineTargetModel | ScriptEventTargetModel]): The targets of the objective. Target
            types must be equal to `objective_type`
        customizations (Customizations):
        rewards (list[RewardOut]):
    """

    objective_id: int
    description: str
    display: None | str
    order_index: int
    objective_type: ObjectiveOutObjectiveType
    logic: ObjectiveOutLogic
    target_count: int | None
    targets: list[KillTargetModel | MineTargetModel | ScriptEventTargetModel]
    customizations: Customizations
    rewards: list[RewardOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.kill_target_model import KillTargetModel
        from ..models.mine_target_model import MineTargetModel

        objective_id = self.objective_id

        description = self.description

        display: None | str
        display = self.display

        order_index = self.order_index

        objective_type = self.objective_type.value

        logic = self.logic.value

        target_count: int | None
        target_count = self.target_count

        targets = []
        for targets_item_data in self.targets:
            targets_item: dict[str, Any]
            if isinstance(targets_item_data, MineTargetModel):
                targets_item = targets_item_data.to_dict()
            elif isinstance(targets_item_data, KillTargetModel):
                targets_item = targets_item_data.to_dict()
            else:
                targets_item = targets_item_data.to_dict()

            targets.append(targets_item)

        customizations = self.customizations.to_dict()

        rewards = []
        for rewards_item_data in self.rewards:
            rewards_item = rewards_item_data.to_dict()
            rewards.append(rewards_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "objective_id": objective_id,
                "description": description,
                "display": display,
                "order_index": order_index,
                "objective_type": objective_type,
                "logic": logic,
                "target_count": target_count,
                "targets": targets,
                "customizations": customizations,
                "rewards": rewards,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customizations import Customizations
        from ..models.kill_target_model import KillTargetModel
        from ..models.mine_target_model import MineTargetModel
        from ..models.reward_out import RewardOut
        from ..models.script_event_target_model import ScriptEventTargetModel

        d = dict(src_dict)
        objective_id = d.pop("objective_id")

        description = d.pop("description")

        def _parse_display(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display = _parse_display(d.pop("display"))

        order_index = d.pop("order_index")

        objective_type = ObjectiveOutObjectiveType(d.pop("objective_type"))

        logic = ObjectiveOutLogic(d.pop("logic"))

        def _parse_target_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        target_count = _parse_target_count(d.pop("target_count"))

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:

            def _parse_targets_item(data: object) -> KillTargetModel | MineTargetModel | ScriptEventTargetModel:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    targets_item_type_0 = MineTargetModel.from_dict(data)

                    return targets_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    targets_item_type_1 = KillTargetModel.from_dict(data)

                    return targets_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                targets_item_type_2 = ScriptEventTargetModel.from_dict(data)

                return targets_item_type_2

            targets_item = _parse_targets_item(targets_item_data)

            targets.append(targets_item)

        customizations = Customizations.from_dict(d.pop("customizations"))

        rewards = []
        _rewards = d.pop("rewards")
        for rewards_item_data in _rewards:
            rewards_item = RewardOut.from_dict(rewards_item_data)

            rewards.append(rewards_item)

        objective_out = cls(
            objective_id=objective_id,
            description=description,
            display=display,
            order_index=order_index,
            objective_type=objective_type,
            logic=logic,
            target_count=target_count,
            targets=targets,
            customizations=customizations,
            rewards=rewards,
        )

        objective_out.additional_properties = d
        return objective_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
