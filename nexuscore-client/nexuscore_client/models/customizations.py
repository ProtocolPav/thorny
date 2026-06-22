from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_customization import LocationCustomization
    from ..models.mainhand_customization import MainhandCustomization
    from ..models.maximum_deaths_customization import MaximumDeathsCustomization
    from ..models.natural_block_customization import NaturalBlockCustomization
    from ..models.timer_customization import TimerCustomization


T = TypeVar("T", bound="Customizations")


@_attrs_define
class Customizations:
    """
    Attributes:
        mainhand (Union['MainhandCustomization', None, Unset]): Mainhand Customization
        location (Union['LocationCustomization', None, Unset]): Location Customization
        timer (Union['TimerCustomization', None, Unset]): Timer Customization
        maximum_deaths (Union['MaximumDeathsCustomization', None, Unset]): Maximum Deaths Customization
        natural_block (Union['NaturalBlockCustomization', None, Unset]): Natural Block Customization
    """

    mainhand: Union["MainhandCustomization", None, Unset] = UNSET
    location: Union["LocationCustomization", None, Unset] = UNSET
    timer: Union["TimerCustomization", None, Unset] = UNSET
    maximum_deaths: Union["MaximumDeathsCustomization", None, Unset] = UNSET
    natural_block: Union["NaturalBlockCustomization", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.location_customization import LocationCustomization
        from ..models.mainhand_customization import MainhandCustomization
        from ..models.maximum_deaths_customization import MaximumDeathsCustomization
        from ..models.natural_block_customization import NaturalBlockCustomization
        from ..models.timer_customization import TimerCustomization

        mainhand: Union[None, Unset, dict[str, Any]]
        if isinstance(self.mainhand, Unset):
            mainhand = UNSET
        elif isinstance(self.mainhand, MainhandCustomization):
            mainhand = self.mainhand.to_dict()
        else:
            mainhand = self.mainhand

        location: Union[None, Unset, dict[str, Any]]
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, LocationCustomization):
            location = self.location.to_dict()
        else:
            location = self.location

        timer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.timer, Unset):
            timer = UNSET
        elif isinstance(self.timer, TimerCustomization):
            timer = self.timer.to_dict()
        else:
            timer = self.timer

        maximum_deaths: Union[None, Unset, dict[str, Any]]
        if isinstance(self.maximum_deaths, Unset):
            maximum_deaths = UNSET
        elif isinstance(self.maximum_deaths, MaximumDeathsCustomization):
            maximum_deaths = self.maximum_deaths.to_dict()
        else:
            maximum_deaths = self.maximum_deaths

        natural_block: Union[None, Unset, dict[str, Any]]
        if isinstance(self.natural_block, Unset):
            natural_block = UNSET
        elif isinstance(self.natural_block, NaturalBlockCustomization):
            natural_block = self.natural_block.to_dict()
        else:
            natural_block = self.natural_block

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mainhand is not UNSET:
            field_dict["mainhand"] = mainhand
        if location is not UNSET:
            field_dict["location"] = location
        if timer is not UNSET:
            field_dict["timer"] = timer
        if maximum_deaths is not UNSET:
            field_dict["maximum_deaths"] = maximum_deaths
        if natural_block is not UNSET:
            field_dict["natural_block"] = natural_block

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location_customization import LocationCustomization
        from ..models.mainhand_customization import MainhandCustomization
        from ..models.maximum_deaths_customization import MaximumDeathsCustomization
        from ..models.natural_block_customization import NaturalBlockCustomization
        from ..models.timer_customization import TimerCustomization

        d = dict(src_dict)

        def _parse_mainhand(data: object) -> Union["MainhandCustomization", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mainhand_type_0 = MainhandCustomization.from_dict(data)

                return mainhand_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MainhandCustomization", None, Unset], data)

        mainhand = _parse_mainhand(d.pop("mainhand", UNSET))

        def _parse_location(data: object) -> Union["LocationCustomization", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = LocationCustomization.from_dict(data)

                return location_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LocationCustomization", None, Unset], data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_timer(data: object) -> Union["TimerCustomization", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                timer_type_0 = TimerCustomization.from_dict(data)

                return timer_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TimerCustomization", None, Unset], data)

        timer = _parse_timer(d.pop("timer", UNSET))

        def _parse_maximum_deaths(data: object) -> Union["MaximumDeathsCustomization", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                maximum_deaths_type_0 = MaximumDeathsCustomization.from_dict(data)

                return maximum_deaths_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MaximumDeathsCustomization", None, Unset], data)

        maximum_deaths = _parse_maximum_deaths(d.pop("maximum_deaths", UNSET))

        def _parse_natural_block(data: object) -> Union["NaturalBlockCustomization", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                natural_block_type_0 = NaturalBlockCustomization.from_dict(data)

                return natural_block_type_0
            except:  # noqa: E722
                pass
            return cast(Union["NaturalBlockCustomization", None, Unset], data)

        natural_block = _parse_natural_block(d.pop("natural_block", UNSET))

        customizations = cls(
            mainhand=mainhand,
            location=location,
            timer=timer,
            maximum_deaths=maximum_deaths,
            natural_block=natural_block,
        )

        customizations.additional_properties = d
        return customizations

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
