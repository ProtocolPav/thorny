from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.interaction_statistic import InteractionStatistic
    from ..models.interaction_totals import InteractionTotals


T = TypeVar("T", bound="InteractionSummary")


@_attrs_define
class InteractionSummary:
    """
    Attributes:
        blocks_mined (list[InteractionStatistic]):
        blocks_placed (list[InteractionStatistic]):
        kills (list[InteractionStatistic]):
        deaths (list[InteractionStatistic]):
        uses (list[InteractionStatistic]):
        totals (InteractionTotals):
    """

    blocks_mined: list[InteractionStatistic]
    blocks_placed: list[InteractionStatistic]
    kills: list[InteractionStatistic]
    deaths: list[InteractionStatistic]
    uses: list[InteractionStatistic]
    totals: InteractionTotals
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blocks_mined = []
        for componentsschemas_interaction_statistics_list_item_data in self.blocks_mined:
            componentsschemas_interaction_statistics_list_item = (
                componentsschemas_interaction_statistics_list_item_data.to_dict()
            )
            blocks_mined.append(componentsschemas_interaction_statistics_list_item)

        blocks_placed = []
        for componentsschemas_interaction_statistics_list_item_data in self.blocks_placed:
            componentsschemas_interaction_statistics_list_item = (
                componentsschemas_interaction_statistics_list_item_data.to_dict()
            )
            blocks_placed.append(componentsschemas_interaction_statistics_list_item)

        kills = []
        for componentsschemas_interaction_statistics_list_item_data in self.kills:
            componentsschemas_interaction_statistics_list_item = (
                componentsschemas_interaction_statistics_list_item_data.to_dict()
            )
            kills.append(componentsschemas_interaction_statistics_list_item)

        deaths = []
        for componentsschemas_interaction_statistics_list_item_data in self.deaths:
            componentsschemas_interaction_statistics_list_item = (
                componentsschemas_interaction_statistics_list_item_data.to_dict()
            )
            deaths.append(componentsschemas_interaction_statistics_list_item)

        uses = []
        for componentsschemas_interaction_statistics_list_item_data in self.uses:
            componentsschemas_interaction_statistics_list_item = (
                componentsschemas_interaction_statistics_list_item_data.to_dict()
            )
            uses.append(componentsschemas_interaction_statistics_list_item)

        totals = self.totals.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blocks_mined": blocks_mined,
                "blocks_placed": blocks_placed,
                "kills": kills,
                "deaths": deaths,
                "uses": uses,
                "totals": totals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.interaction_statistic import InteractionStatistic
        from ..models.interaction_totals import InteractionTotals

        d = dict(src_dict)
        blocks_mined = []
        _blocks_mined = d.pop("blocks_mined")
        for componentsschemas_interaction_statistics_list_item_data in _blocks_mined:
            componentsschemas_interaction_statistics_list_item = InteractionStatistic.from_dict(
                componentsschemas_interaction_statistics_list_item_data
            )

            blocks_mined.append(componentsschemas_interaction_statistics_list_item)

        blocks_placed = []
        _blocks_placed = d.pop("blocks_placed")
        for componentsschemas_interaction_statistics_list_item_data in _blocks_placed:
            componentsschemas_interaction_statistics_list_item = InteractionStatistic.from_dict(
                componentsschemas_interaction_statistics_list_item_data
            )

            blocks_placed.append(componentsschemas_interaction_statistics_list_item)

        kills = []
        _kills = d.pop("kills")
        for componentsschemas_interaction_statistics_list_item_data in _kills:
            componentsschemas_interaction_statistics_list_item = InteractionStatistic.from_dict(
                componentsschemas_interaction_statistics_list_item_data
            )

            kills.append(componentsschemas_interaction_statistics_list_item)

        deaths = []
        _deaths = d.pop("deaths")
        for componentsschemas_interaction_statistics_list_item_data in _deaths:
            componentsschemas_interaction_statistics_list_item = InteractionStatistic.from_dict(
                componentsschemas_interaction_statistics_list_item_data
            )

            deaths.append(componentsschemas_interaction_statistics_list_item)

        uses = []
        _uses = d.pop("uses")
        for componentsschemas_interaction_statistics_list_item_data in _uses:
            componentsschemas_interaction_statistics_list_item = InteractionStatistic.from_dict(
                componentsschemas_interaction_statistics_list_item_data
            )

            uses.append(componentsschemas_interaction_statistics_list_item)

        totals = InteractionTotals.from_dict(d.pop("totals"))

        interaction_summary = cls(
            blocks_mined=blocks_mined,
            blocks_placed=blocks_placed,
            kills=kills,
            deaths=deaths,
            uses=uses,
            totals=totals,
        )

        interaction_summary.additional_properties = d
        return interaction_summary

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
