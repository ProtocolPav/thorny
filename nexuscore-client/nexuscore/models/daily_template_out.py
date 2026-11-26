from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.daily_template_out_logic import DailyTemplateOutLogic
from ..models.daily_template_out_objective_type import DailyTemplateOutObjectiveType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customization_options import CustomizationOptions
    from ..models.kill_target_option import KillTargetOption
    from ..models.mine_target_option import MineTargetOption
    from ..models.random_count import RandomCount
    from ..models.reward_option import RewardOption
    from ..models.script_event_target_option import ScriptEventTargetOption
    from ..models.visit_target_option import VisitTargetOption


T = TypeVar("T", bound="DailyTemplateOut")


@_attrs_define
class DailyTemplateOut:
    """
    Attributes:
        name (str): Internal name of the template
        created_by (int): The Thorny ID that created this template. Generated quests are attributed to them.
        title (str): The generated quest title. Supports `{targets}` and `{count}` placeholders.
        description (str): The generated quest description. Supports `{targets}` and `{count}` placeholders.
        objective_description (str): The generated objective description. Supports `{targets}` and `{count}`
            placeholders.
        objective_type (DailyTemplateOutObjectiveType): The type of objective
        targets (list[KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption]): The possible
            targets. Target types must equal `objective_type`.
        template_id (int): The daily template ID
        guild_id (int): The guild this template belongs to
        created_at (datetime.datetime):
        enabled (bool | Unset): Whether this template can be chosen Default: True.
        weight (int | Unset): Relative chance of this template being chosen Default: 1.
        objective_display (None | str | Unset):
        logic (DailyTemplateOutLogic | Unset): The logic to be applied to the objective targets Default:
            DailyTemplateOutLogic.AND.
        target_picks (None | RandomCount | Unset):
        target_count (None | RandomCount | Unset):
        customizations (CustomizationOptions | Unset):
        rewards (list[RewardOption] | Unset): The possible rewards
        reward_picks (int | Unset): How many of the reward options are given Default: 1.
    """

    name: str
    created_by: int
    title: str
    description: str
    objective_description: str
    objective_type: DailyTemplateOutObjectiveType
    targets: list[KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption]
    template_id: int
    guild_id: int
    created_at: datetime.datetime
    enabled: bool | Unset = True
    weight: int | Unset = 1
    objective_display: None | str | Unset = UNSET
    logic: DailyTemplateOutLogic | Unset = DailyTemplateOutLogic.AND
    target_picks: None | RandomCount | Unset = UNSET
    target_count: None | RandomCount | Unset = UNSET
    customizations: CustomizationOptions | Unset = UNSET
    rewards: list[RewardOption] | Unset = UNSET
    reward_picks: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.kill_target_option import KillTargetOption
        from ..models.mine_target_option import MineTargetOption
        from ..models.random_count import RandomCount
        from ..models.script_event_target_option import ScriptEventTargetOption

        name = self.name

        created_by = self.created_by

        title = self.title

        description = self.description

        objective_description = self.objective_description

        objective_type = self.objective_type.value

        targets = []
        for targets_item_data in self.targets:
            targets_item: dict[str, Any]
            if isinstance(targets_item_data, MineTargetOption):
                targets_item = targets_item_data.to_dict()
            elif isinstance(targets_item_data, KillTargetOption):
                targets_item = targets_item_data.to_dict()
            elif isinstance(targets_item_data, ScriptEventTargetOption):
                targets_item = targets_item_data.to_dict()
            else:
                targets_item = targets_item_data.to_dict()

            targets.append(targets_item)

        template_id = self.template_id

        guild_id = self.guild_id

        created_at = self.created_at.isoformat()

        enabled = self.enabled

        weight = self.weight

        objective_display: None | str | Unset
        if isinstance(self.objective_display, Unset):
            objective_display = UNSET
        else:
            objective_display = self.objective_display

        logic: str | Unset = UNSET
        if not isinstance(self.logic, Unset):
            logic = self.logic.value

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

        customizations: dict[str, Any] | Unset = UNSET
        if not isinstance(self.customizations, Unset):
            customizations = self.customizations.to_dict()

        rewards: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rewards, Unset):
            rewards = []
            for rewards_item_data in self.rewards:
                rewards_item = rewards_item_data.to_dict()
                rewards.append(rewards_item)

        reward_picks = self.reward_picks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "created_by": created_by,
                "title": title,
                "description": description,
                "objective_description": objective_description,
                "objective_type": objective_type,
                "targets": targets,
                "template_id": template_id,
                "guild_id": guild_id,
                "created_at": created_at,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if weight is not UNSET:
            field_dict["weight"] = weight
        if objective_display is not UNSET:
            field_dict["objective_display"] = objective_display
        if logic is not UNSET:
            field_dict["logic"] = logic
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
        name = d.pop("name")

        created_by = d.pop("created_by")

        title = d.pop("title")

        description = d.pop("description")

        objective_description = d.pop("objective_description")

        objective_type = DailyTemplateOutObjectiveType(d.pop("objective_type"))

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:

            def _parse_targets_item(
                data: object,
            ) -> KillTargetOption | MineTargetOption | ScriptEventTargetOption | VisitTargetOption:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    targets_item_type_0 = MineTargetOption.from_dict(data)

                    return targets_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    targets_item_type_1 = KillTargetOption.from_dict(data)

                    return targets_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    targets_item_type_2 = ScriptEventTargetOption.from_dict(data)

                    return targets_item_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                targets_item_type_3 = VisitTargetOption.from_dict(data)

                return targets_item_type_3

            targets_item = _parse_targets_item(targets_item_data)

            targets.append(targets_item)

        template_id = d.pop("template_id")

        guild_id = d.pop("guild_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        enabled = d.pop("enabled", UNSET)

        weight = d.pop("weight", UNSET)

        def _parse_objective_display(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        objective_display = _parse_objective_display(d.pop("objective_display", UNSET))

        _logic = d.pop("logic", UNSET)
        logic: DailyTemplateOutLogic | Unset
        if isinstance(_logic, Unset):
            logic = UNSET
        else:
            logic = DailyTemplateOutLogic(_logic)

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

        _customizations = d.pop("customizations", UNSET)
        customizations: CustomizationOptions | Unset
        if isinstance(_customizations, Unset):
            customizations = UNSET
        else:
            customizations = CustomizationOptions.from_dict(_customizations)

        _rewards = d.pop("rewards", UNSET)
        rewards: list[RewardOption] | Unset = UNSET
        if _rewards is not UNSET:
            rewards = []
            for rewards_item_data in _rewards:
                rewards_item = RewardOption.from_dict(rewards_item_data)

                rewards.append(rewards_item)

        reward_picks = d.pop("reward_picks", UNSET)

        daily_template_out = cls(
            name=name,
            created_by=created_by,
            title=title,
            description=description,
            objective_description=objective_description,
            objective_type=objective_type,
            targets=targets,
            template_id=template_id,
            guild_id=guild_id,
            created_at=created_at,
            enabled=enabled,
            weight=weight,
            objective_display=objective_display,
            logic=logic,
            target_picks=target_picks,
            target_count=target_count,
            customizations=customizations,
            rewards=rewards,
            reward_picks=reward_picks,
        )

        daily_template_out.additional_properties = d
        return daily_template_out

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
