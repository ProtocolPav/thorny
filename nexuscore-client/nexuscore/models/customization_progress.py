from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.death_customization_progress import DeathCustomizationProgress


T = TypeVar("T", bound="CustomizationProgress")


@_attrs_define
class CustomizationProgress:
    """
    Attributes:
        maximum_deaths (DeathCustomizationProgress | None | Unset): Death count tracking
    """

    maximum_deaths: DeathCustomizationProgress | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.death_customization_progress import DeathCustomizationProgress

        maximum_deaths: dict[str, Any] | None | Unset
        if isinstance(self.maximum_deaths, Unset):
            maximum_deaths = UNSET
        elif isinstance(self.maximum_deaths, DeathCustomizationProgress):
            maximum_deaths = self.maximum_deaths.to_dict()
        else:
            maximum_deaths = self.maximum_deaths

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if maximum_deaths is not UNSET:
            field_dict["maximum_deaths"] = maximum_deaths

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.death_customization_progress import DeathCustomizationProgress

        d = dict(src_dict)

        def _parse_maximum_deaths(data: object) -> DeathCustomizationProgress | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                maximum_deaths_type_0 = DeathCustomizationProgress.from_dict(data)

                return maximum_deaths_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeathCustomizationProgress | None | Unset, data)

        maximum_deaths = _parse_maximum_deaths(d.pop("maximum_deaths", UNSET))

        customization_progress = cls(
            maximum_deaths=maximum_deaths,
        )

        customization_progress.additional_properties = d
        return customization_progress

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
