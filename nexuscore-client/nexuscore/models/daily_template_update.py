from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.daily_template_update_logic_type_0 import DailyTemplateUpdateLogicType0
from ..models.daily_template_update_objective_type_type_0 import DailyTemplateUpdateObjectiveTypeType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customization_options import CustomizationOptions
    from ..models.kill_target_option import KillTargetOption
    from ..models.mine_target_option import MineTargetOption
    from ..models.random_count import RandomCount
    from ..models.reward_option import RewardOption
    from ..models.script_event_target_option import ScriptEventTargetOption
    from ..models.visit_target_option import VisitTargetOption


T = TypeVar("T", bound="DailyTemplateUpdate")


@_attrs_define
class DailyTemplateUpdate:
    """
    Attributes:
        name (None | str | Unset):
        enabled (bool | None | Unset):
        weight (int | None | Unset):
        created_by (int | None | Unset):
        title (None | str | Unset):
        description (None | str | Unset):
        objective_description (None | str | Unset):
        objective_display (None | str | Unset):
        objective_type (DailyTemplateUpdateObjectiveTypeType0 | None | Unset):
        logic (DailyTemplateUpdateLogicType0 | None | Unset):
        targets (list[KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption] | None |
            Unset):
        target_picks (None | RandomCount | Unset):
        target_count (None | RandomCount | Unset):
        customizations (CustomizationOptions | None | Unset):
        rewards (list[RewardOption] | None | Unset):
        reward_picks (int | None | Unset):
    """

    name: None | str | Unset = UNSET
    enabled: bool | None | Unset = UNSET
    weight: int | None | Unset = UNSET
    created_by: int | None | Unset = UNSET
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    objective_description: None | str | Unset = UNSET
    objective_display: None | str | Unset = UNSET
    objective_type: DailyTemplateUpdateObjectiveTypeType0 | None | Unset = UNSET
    logic: DailyTemplateUpdateLogicType0 | None | Unset = UNSET
    targets: list[KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption] | None | Unset = (
        UNSET
    )
    target_picks: None | RandomCount | Unset = UNSET
    target_count: None | RandomCount | Unset = UNSET
    customizations: CustomizationOptions | None | Unset = UNSET
    rewards: list[RewardOption] | None | Unset = UNSET
    reward_picks: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customization_options import CustomizationOptions
        from ..models.kill_target_option import KillTargetOption
        from ..models.mine_target_option import MineTargetOption
        from ..models.random_count import RandomCount
        from ..models.script_event_target_option import ScriptEventTargetOption

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        enabled: bool | None | Unset
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled

        weight: int | None | Unset
        if isinstance(self.weight, Unset):
            weight = UNSET
        else:
            weight = self.weight

        created_by: int | None | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        objective_description: None | str | Unset
        if isinstance(self.objective_description, Unset):
            objective_description = UNSET
        else:
            objective_description = self.objective_description

        objective_display: None | str | Unset
        if isinstance(self.objective_display, Unset):
            objective_display = UNSET
        else:
            objective_display = self.objective_display

        objective_type: None | str | Unset
        if isinstance(self.objective_type, Unset):
            objective_type = UNSET
        elif isinstance(self.objective_type, DailyTemplateUpdateObjectiveTypeType0):
            objective_type = self.objective_type.value
        else:
            objective_type = self.objective_type

        logic: None | str | Unset
        if isinstance(self.logic, Unset):
            logic = UNSET
        elif isinstance(self.logic, DailyTemplateUpdateLogicType0):
            logic = self.logic.value
        else:
            logic = self.logic

        targets: list[dict[str, Any]] | None | Unset
        if isinstance(self.targets, Unset):
            targets = UNSET
        elif isinstance(self.targets, list):
            targets = []
            for targets_type_0_item_data in self.targets:
                targets_type_0_item: dict[str, Any]
                if isinstance(targets_type_0_item_data, MineTargetOption):
                    targets_type_0_item = targets_type_0_item_data.to_dict()
                elif isinstance(targets_type_0_item_data, KillTargetOption):
                    targets_type_0_item = targets_type_0_item_data.to_dict()
                elif isinstance(targets_type_0_item_data, ScriptEventTargetOption):
                    targets_type_0_item = targets_type_0_item_data.to_dict()
                else:
                    targets_type_0_item = targets_type_0_item_data.to_dict()

                targets.append(targets_type_0_item)

        else:
            targets = self.targets

        target_picks: dict[str, Any] | None | Unset
        if isinstance(self.target_picks, Unset):
            target_picks = UNSET
        elif isinstance(self.target_picks, RandomCount):
            target_picks = self.target_picks.to_dict()
        else:
            target_picks = self.target_picks

        target_count: dict[str, Any] | None | Unset
        if isinstance(self.target_count, Unset):
            target_count = UNSET
        elif isinstance(self.target_count, RandomCount):
            target_count = self.target_count.to_dict()
        else:
            target_count = self.target_count

        customizations: dict[str, Any] | None | Unset
        if isinstance(self.customizations, Unset):
            customizations = UNSET
        elif isinstance(self.customizations, CustomizationOptions):
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

        reward_picks: int | None | Unset
        if isinstance(self.reward_picks, Unset):
            reward_picks = UNSET
        else:
            reward_picks = self.reward_picks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if weight is not UNSET:
            field_dict["weight"] = weight
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if objective_description is not UNSET:
            field_dict["objective_description"] = objective_description
        if objective_display is not UNSET:
            field_dict["objective_display"] = objective_display
        if objective_type is not UNSET:
            field_dict["objective_type"] = objective_type
        if logic is not UNSET:
            field_dict["logic"] = logic
        if targets is not UNSET:
            field_dict["targets"] = targets
        if target_picks is not UNSET:
            field_dict["target_picks"] = target_picks
        if target_count is not UNSET:
            field_dict["target_count"] = target_count
        if customizations is not UNSET:
            field_dict["customizations"] = customizations
        if rewards is not UNSET:
            field_dict["rewards"] = rewards
        if reward_picks is not UNSET:
            field_dict["reward_picks"] = reward_picks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customization_options import CustomizationOptions
        from ..models.kill_target_option import KillTargetOption
        from ..models.mine_target_option import MineTargetOption
        from ..models.random_count import RandomCount
        from ..models.reward_option import RewardOption
        from ..models.script_event_target_option import ScriptEventTargetOption
        from ..models.visit_target_option import VisitTargetOption

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))

        def _parse_weight(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        weight = _parse_weight(d.pop("weight", UNSET))

        def _parse_created_by(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_objective_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        objective_description = _parse_objective_description(d.pop("objective_description", UNSET))

        def _parse_objective_display(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        objective_display = _parse_objective_display(d.pop("objective_display", UNSET))

        def _parse_objective_type(data: object) -> DailyTemplateUpdateObjectiveTypeType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                objective_type_type_0 = DailyTemplateUpdateObjectiveTypeType0(data)

                return objective_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DailyTemplateUpdateObjectiveTypeType0 | None | Unset, data)

        objective_type = _parse_objective_type(d.pop("objective_type", UNSET))

        def _parse_logic(data: object) -> DailyTemplateUpdateLogicType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                logic_type_0 = DailyTemplateUpdateLogicType0(data)

                return logic_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DailyTemplateUpdateLogicType0 | None | Unset, data)

        logic = _parse_logic(d.pop("logic", UNSET))

        def _parse_targets(
            data: object,
        ) -> list[KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption] | None | Unset:
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
                    ) -> KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            targets_type_0_item_type_0 = MineTargetOption.from_dict(data)

                            return targets_type_0_item_type_0
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            targets_type_0_item_type_1 = KillTargetOption.from_dict(data)

                            return targets_type_0_item_type_1
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            targets_type_0_item_type_2 = ScriptEventTargetOption.from_dict(data)

                            return targets_type_0_item_type_2
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        targets_type_0_item_type_3 = VisitTargetOption.from_dict(data)

                        return targets_type_0_item_type_3

                    targets_type_0_item = _parse_targets_type_0_item(targets_type_0_item_data)

                    targets_type_0.append(targets_type_0_item)

                return targets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                list[KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption] | None | Unset,
                data,
            )

        targets = _parse_targets(d.pop("targets", UNSET))

        def _parse_target_picks(data: object) -> None | RandomCount | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_picks_type_0 = RandomCount.from_dict(data)

                return target_picks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RandomCount | Unset, data)

        target_picks = _parse_target_picks(d.pop("target_picks", UNSET))

        def _parse_target_count(data: object) -> None | RandomCount | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_count_type_0 = RandomCount.from_dict(data)

                return target_count_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RandomCount | Unset, data)

        target_count = _parse_target_count(d.pop("target_count", UNSET))

        def _parse_customizations(data: object) -> CustomizationOptions | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                customizations_type_0 = CustomizationOptions.from_dict(data)

                return customizations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CustomizationOptions | None | Unset, data)

        customizations = _parse_customizations(d.pop("customizations", UNSET))

        def _parse_rewards(data: object) -> list[RewardOption] | None | Unset:
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
                    rewards_type_0_item = RewardOption.from_dict(rewards_type_0_item_data)

                    rewards_type_0.append(rewards_type_0_item)

                return rewards_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RewardOption] | None | Unset, data)

        rewards = _parse_rewards(d.pop("rewards", UNSET))

        def _parse_reward_picks(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        reward_picks = _parse_reward_picks(d.pop("reward_picks", UNSET))

        daily_template_update = cls(
            name=name,
            enabled=enabled,
            weight=weight,
            created_by=created_by,
            title=title,
            description=description,
            objective_description=objective_description,
            objective_display=objective_display,
            objective_type=objective_type,
            logic=logic,
            targets=targets,
            target_picks=target_picks,
            target_count=target_count,
            customizations=customizations,
            rewards=rewards,
            reward_picks=reward_picks,
        )

        daily_template_update.additional_properties = d
        return daily_template_update

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
