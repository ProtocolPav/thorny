from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.objective_in_logic import ObjectiveInLogic
from ..models.objective_in_objective_type import ObjectiveInObjectiveType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customizations import Customizations
    from ..models.kill_target_model import KillTargetModel
    from ..models.mine_target_model import MineTargetModel
    from ..models.reward_in import RewardIn
    from ..models.script_event_target_model import ScriptEventTargetModel
    from ..models.visit_target_model import VisitTargetModel


T = TypeVar("T", bound="ObjectiveIn")


@_attrs_define
class ObjectiveIn:
    """
    Attributes:
        description (str): The description of the objective
        order_index (int): The order of the objective. Starts at 0.
        objective_type (ObjectiveInObjectiveType): The type of objective
        logic (ObjectiveInLogic): The logic to be applied to the objective targets
        targets (list[KillTargetModel | MineTargetModel | ScriptEventTargetModel | VisitTargetModel]): The targets of
            the objective. Target types must be equal to `objective_type`
        customizations (Customizations):
        rewards (list[RewardIn]):
        display (None | str | Unset):
        target_count (int | None | Unset):
    """

    description: str
    order_index: int
    objective_type: ObjectiveInObjectiveType
    logic: ObjectiveInLogic
    targets: list[KillTargetModel | MineTargetModel | ScriptEventTargetModel | VisitTargetModel]
    customizations: Customizations
    rewards: list[RewardIn]
    display: None | str | Unset = UNSET
    target_count: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.kill_target_model import KillTargetModel
        from ..models.mine_target_model import MineTargetModel
        from ..models.script_event_target_model import ScriptEventTargetModel

        description = self.description

        order_index = self.order_index

        objective_type = self.objective_type.value

        logic = self.logic.value

        targets = []
        for targets_item_data in self.targets:
            targets_item: dict[str, Any]
            if isinstance(targets_item_data, MineTargetModel):
                targets_item = targets_item_data.to_dict()
            elif isinstance(targets_item_data, KillTargetModel):
                targets_item = targets_item_data.to_dict()
            elif isinstance(targets_item_data, ScriptEventTargetModel):
                targets_item = targets_item_data.to_dict()
            else:
                targets_item = targets_item_data.to_dict()

            targets.append(targets_item)

        customizations = self.customizations.to_dict()

        rewards = []
        for rewards_item_data in self.rewards:
            rewards_item = rewards_item_data.to_dict()
            rewards.append(rewards_item)

        display: None | str | Unset
        if isinstance(self.display, Unset):
            display = UNSET
        else:
            display = self.display

        target_count: int | None | Unset
        if isinstance(self.target_count, Unset):
            target_count = UNSET
        else:
            target_count = self.target_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "order_index": order_index,
                "objective_type": objective_type,
                "logic": logic,
                "targets": targets,
                "customizations": customizations,
                "rewards": rewards,
            }
        )
        if display is not UNSET:
            field_dict["display"] = display
        if target_count is not UNSET:
            field_dict["target_count"] = target_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customizations import Customizations
        from ..models.kill_target_model import KillTargetModel
        from ..models.mine_target_model import MineTargetModel
        from ..models.reward_in import RewardIn
        from ..models.script_event_target_model import ScriptEventTargetModel
        from ..models.visit_target_model import VisitTargetModel

        d = dict(src_dict)
        description = d.pop("description")

        order_index = d.pop("order_index")

        objective_type = ObjectiveInObjectiveType(d.pop("objective_type"))

        logic = ObjectiveInLogic(d.pop("logic"))

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:

            def _parse_targets_item(
                data: object,
            ) -> KillTargetModel | MineTargetModel | ScriptEventTargetModel | VisitTargetModel:
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
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    targets_item_type_2 = ScriptEventTargetModel.from_dict(data)

                    return targets_item_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                targets_item_type_3 = VisitTargetModel.from_dict(data)

                return targets_item_type_3

            targets_item = _parse_targets_item(targets_item_data)

            targets.append(targets_item)

        customizations = Customizations.from_dict(d.pop("customizations"))

        rewards = []
        _rewards = d.pop("rewards")
        for rewards_item_data in _rewards:
            rewards_item = RewardIn.from_dict(rewards_item_data)

            rewards.append(rewards_item)

        def _parse_display(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display = _parse_display(d.pop("display", UNSET))

        def _parse_target_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        target_count = _parse_target_count(d.pop("target_count", UNSET))

        objective_in = cls(
            description=description,
            order_index=order_index,
            objective_type=objective_type,
            logic=logic,
            targets=targets,
            customizations=customizations,
            rewards=rewards,
            display=display,
            target_count=target_count,
        )

        objective_in.additional_properties = d
        return objective_in

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
