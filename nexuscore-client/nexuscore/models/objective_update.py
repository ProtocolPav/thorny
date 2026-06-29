from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.objective_update_logic_type_0 import ObjectiveUpdateLogicType0
from ..models.objective_update_objective_type_type_0 import ObjectiveUpdateObjectiveTypeType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customizations import Customizations
    from ..models.kill_target_model import KillTargetModel
    from ..models.mine_target_model import MineTargetModel
    from ..models.reward_update import RewardUpdate
    from ..models.script_event_target_model import ScriptEventTargetModel


T = TypeVar("T", bound="ObjectiveUpdate")


@_attrs_define
class ObjectiveUpdate:
    """
    Attributes:
        objective_id (int | None | Unset):
        description (None | str | Unset):
        display (None | str | Unset):
        order_index (int | None | Unset):
        objective_type (None | ObjectiveUpdateObjectiveTypeType0 | Unset):
        logic (None | ObjectiveUpdateLogicType0 | Unset):
        target_count (int | None | Unset):
        targets (list[KillTargetModel | MineTargetModel | ScriptEventTargetModel] | None | Unset):
        customizations (Customizations | None | Unset):
        rewards (list[RewardUpdate] | None | Unset):
    """

    objective_id: int | None | Unset = UNSET
    description: None | str | Unset = UNSET
    display: None | str | Unset = UNSET
    order_index: int | None | Unset = UNSET
    objective_type: None | ObjectiveUpdateObjectiveTypeType0 | Unset = UNSET
    logic: None | ObjectiveUpdateLogicType0 | Unset = UNSET
    target_count: int | None | Unset = UNSET
    targets: list[KillTargetModel | MineTargetModel | ScriptEventTargetModel] | None | Unset = UNSET
    customizations: Customizations | None | Unset = UNSET
    rewards: list[RewardUpdate] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customizations import Customizations
        from ..models.kill_target_model import KillTargetModel
        from ..models.mine_target_model import MineTargetModel

        objective_id: int | None | Unset
        if isinstance(self.objective_id, Unset):
            objective_id = UNSET
        else:
            objective_id = self.objective_id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        display: None | str | Unset
        if isinstance(self.display, Unset):
            display = UNSET
        else:
            display = self.display

        order_index: int | None | Unset
        if isinstance(self.order_index, Unset):
            order_index = UNSET
        else:
            order_index = self.order_index

        objective_type: None | str | Unset
        if isinstance(self.objective_type, Unset):
            objective_type = UNSET
        elif isinstance(self.objective_type, ObjectiveUpdateObjectiveTypeType0):
            objective_type = self.objective_type.value
        else:
            objective_type = self.objective_type

        logic: None | str | Unset
        if isinstance(self.logic, Unset):
            logic = UNSET
        elif isinstance(self.logic, ObjectiveUpdateLogicType0):
            logic = self.logic.value
        else:
            logic = self.logic

        target_count: int | None | Unset
        if isinstance(self.target_count, Unset):
            target_count = UNSET
        else:
            target_count = self.target_count

        targets: list[dict[str, Any]] | None | Unset
        if isinstance(self.targets, Unset):
            targets = UNSET
        elif isinstance(self.targets, list):
            targets = []
            for targets_type_0_item_data in self.targets:
                targets_type_0_item: dict[str, Any]
                if isinstance(targets_type_0_item_data, MineTargetModel):
                    targets_type_0_item = targets_type_0_item_data.to_dict()
                elif isinstance(targets_type_0_item_data, KillTargetModel):
                    targets_type_0_item = targets_type_0_item_data.to_dict()
                else:
                    targets_type_0_item = targets_type_0_item_data.to_dict()

                targets.append(targets_type_0_item)

        else:
            targets = self.targets

        customizations: dict[str, Any] | None | Unset
        if isinstance(self.customizations, Unset):
            customizations = UNSET
        elif isinstance(self.customizations, Customizations):
            customizations = self.customizations.to_dict()
        else:
            customizations = self.customizations

        rewards: list[dict[str, Any]] | None | Unset
        if isinstance(self.rewards, Unset):
            rewards = UNSET
        elif isinstance(self.rewards, list):
            rewards = []
            for rewards_type_0_item_data in self.rewards:
                rewards_type_0_item = rewards_type_0_item_data.to_dict()
                rewards.append(rewards_type_0_item)

        else:
            rewards = self.rewards

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if objective_id is not UNSET:
            field_dict["objective_id"] = objective_id
        if description is not UNSET:
            field_dict["description"] = description
        if display is not UNSET:
            field_dict["display"] = display
        if order_index is not UNSET:
            field_dict["order_index"] = order_index
        if objective_type is not UNSET:
            field_dict["objective_type"] = objective_type
        if logic is not UNSET:
            field_dict["logic"] = logic
        if target_count is not UNSET:
            field_dict["target_count"] = target_count
        if targets is not UNSET:
            field_dict["targets"] = targets
        if customizations is not UNSET:
            field_dict["customizations"] = customizations
        if rewards is not UNSET:
            field_dict["rewards"] = rewards

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customizations import Customizations
        from ..models.kill_target_model import KillTargetModel
        from ..models.mine_target_model import MineTargetModel
        from ..models.reward_update import RewardUpdate
        from ..models.script_event_target_model import ScriptEventTargetModel

        d = dict(src_dict)

        def _parse_objective_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        objective_id = _parse_objective_id(d.pop("objective_id", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_display(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display = _parse_display(d.pop("display", UNSET))

        def _parse_order_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        order_index = _parse_order_index(d.pop("order_index", UNSET))

        def _parse_objective_type(data: object) -> None | ObjectiveUpdateObjectiveTypeType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                objective_type_type_0 = ObjectiveUpdateObjectiveTypeType0(data)

                return objective_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ObjectiveUpdateObjectiveTypeType0 | Unset, data)

        objective_type = _parse_objective_type(d.pop("objective_type", UNSET))

        def _parse_logic(data: object) -> None | ObjectiveUpdateLogicType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                logic_type_0 = ObjectiveUpdateLogicType0(data)

                return logic_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ObjectiveUpdateLogicType0 | Unset, data)

        logic = _parse_logic(d.pop("logic", UNSET))

        def _parse_target_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        target_count = _parse_target_count(d.pop("target_count", UNSET))

        def _parse_targets(
            data: object,
        ) -> list[KillTargetModel | MineTargetModel | ScriptEventTargetModel] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                targets_type_0 = []
                _targets_type_0 = data
                for targets_type_0_item_data in _targets_type_0:

                    def _parse_targets_type_0_item(
                        data: object,
                    ) -> KillTargetModel | MineTargetModel | ScriptEventTargetModel:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            targets_type_0_item_type_0 = MineTargetModel.from_dict(data)

                            return targets_type_0_item_type_0
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            targets_type_0_item_type_1 = KillTargetModel.from_dict(data)

                            return targets_type_0_item_type_1
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        targets_type_0_item_type_2 = ScriptEventTargetModel.from_dict(data)

                        return targets_type_0_item_type_2

                    targets_type_0_item = _parse_targets_type_0_item(targets_type_0_item_data)

                    targets_type_0.append(targets_type_0_item)

                return targets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KillTargetModel | MineTargetModel | ScriptEventTargetModel] | None | Unset, data)

        targets = _parse_targets(d.pop("targets", UNSET))

        def _parse_customizations(data: object) -> Customizations | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                customizations_type_0 = Customizations.from_dict(data)

                return customizations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Customizations | None | Unset, data)

        customizations = _parse_customizations(d.pop("customizations", UNSET))

        def _parse_rewards(data: object) -> list[RewardUpdate] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                rewards_type_0 = []
                _rewards_type_0 = data
                for rewards_type_0_item_data in _rewards_type_0:
                    rewards_type_0_item = RewardUpdate.from_dict(rewards_type_0_item_data)

                    rewards_type_0.append(rewards_type_0_item)

                return rewards_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RewardUpdate] | None | Unset, data)

        rewards = _parse_rewards(d.pop("rewards", UNSET))

        objective_update = cls(
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

        objective_update.additional_properties = d
        return objective_update

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
