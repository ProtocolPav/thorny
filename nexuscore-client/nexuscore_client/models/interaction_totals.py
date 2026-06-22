from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InteractionTotals")


@_attrs_define
class InteractionTotals:
    """
    Attributes:
        mine (int):
        kill (int):
        place (int):
        die (int):
        use (int):
    """

    mine: int
    kill: int
    place: int
    die: int
    use: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mine = self.mine

        kill = self.kill

        place = self.place

        die = self.die

        use = self.use

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mine": mine,
                "kill": kill,
                "place": place,
                "die": die,
                "use": use,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mine = d.pop("mine")

        kill = d.pop("kill")

        place = d.pop("place")

        die = d.pop("die")

        use = d.pop("use")

        interaction_totals = cls(
            mine=mine,
            kill=kill,
            place=place,
            die=die,
            use=use,
        )

        interaction_totals.additional_properties = d
        return interaction_totals

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
