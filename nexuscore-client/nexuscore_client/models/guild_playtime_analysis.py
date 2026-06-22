from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.daily_playtime import DailyPlaytime
    from ..models.monthly_playtime import MonthlyPlaytime
    from ..models.weekly_playtime import WeeklyPlaytime


T = TypeVar("T", bound="GuildPlaytimeAnalysis")


@_attrs_define
class GuildPlaytimeAnalysis:
    """
    Attributes:
        total_playtime (float): The total playtime of this guild in seconds
        total_unique_players (int): The total unique players that have played on this guild
        daily_playtime (list['DailyPlaytime']): Data about the last 7 days of playtime
        weekly_playtime (list['WeeklyPlaytime']): Data about the last 8 weeks of playtime
        monthly_playtime (list['MonthlyPlaytime']): Data about the last 12 months of playtime
        peak_playtime_periods (Union[Unset, None]):
        peak_active_periods (Union[Unset, None]):
        daily_playtime_distribution (Union[Unset, None]):
        anomalies (Union[Unset, None]):
        predictive_insights (Union[Unset, None]):
    """

    total_playtime: float
    total_unique_players: int
    daily_playtime: list["DailyPlaytime"]
    weekly_playtime: list["WeeklyPlaytime"]
    monthly_playtime: list["MonthlyPlaytime"]
    peak_playtime_periods: Union[Unset, None] = UNSET
    peak_active_periods: Union[Unset, None] = UNSET
    daily_playtime_distribution: Union[Unset, None] = UNSET
    anomalies: Union[Unset, None] = UNSET
    predictive_insights: Union[Unset, None] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_playtime = self.total_playtime

        total_unique_players = self.total_unique_players

        daily_playtime = []
        for daily_playtime_item_data in self.daily_playtime:
            daily_playtime_item = daily_playtime_item_data.to_dict()
            daily_playtime.append(daily_playtime_item)

        weekly_playtime = []
        for weekly_playtime_item_data in self.weekly_playtime:
            weekly_playtime_item = weekly_playtime_item_data.to_dict()
            weekly_playtime.append(weekly_playtime_item)

        monthly_playtime = []
        for monthly_playtime_item_data in self.monthly_playtime:
            monthly_playtime_item = monthly_playtime_item_data.to_dict()
            monthly_playtime.append(monthly_playtime_item)

        peak_playtime_periods = self.peak_playtime_periods

        peak_active_periods = self.peak_active_periods

        daily_playtime_distribution = self.daily_playtime_distribution

        anomalies = self.anomalies

        predictive_insights = self.predictive_insights

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_playtime": total_playtime,
                "total_unique_players": total_unique_players,
                "daily_playtime": daily_playtime,
                "weekly_playtime": weekly_playtime,
                "monthly_playtime": monthly_playtime,
            }
        )
        if peak_playtime_periods is not UNSET:
            field_dict["peak_playtime_periods"] = peak_playtime_periods
        if peak_active_periods is not UNSET:
            field_dict["peak_active_periods"] = peak_active_periods
        if daily_playtime_distribution is not UNSET:
            field_dict["daily_playtime_distribution"] = daily_playtime_distribution
        if anomalies is not UNSET:
            field_dict["anomalies"] = anomalies
        if predictive_insights is not UNSET:
            field_dict["predictive_insights"] = predictive_insights

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_playtime import DailyPlaytime
        from ..models.monthly_playtime import MonthlyPlaytime
        from ..models.weekly_playtime import WeeklyPlaytime

        d = dict(src_dict)
        total_playtime = d.pop("total_playtime")

        total_unique_players = d.pop("total_unique_players")

        daily_playtime = []
        _daily_playtime = d.pop("daily_playtime")
        for daily_playtime_item_data in _daily_playtime:
            daily_playtime_item = DailyPlaytime.from_dict(daily_playtime_item_data)

            daily_playtime.append(daily_playtime_item)

        weekly_playtime = []
        _weekly_playtime = d.pop("weekly_playtime")
        for weekly_playtime_item_data in _weekly_playtime:
            weekly_playtime_item = WeeklyPlaytime.from_dict(weekly_playtime_item_data)

            weekly_playtime.append(weekly_playtime_item)

        monthly_playtime = []
        _monthly_playtime = d.pop("monthly_playtime")
        for monthly_playtime_item_data in _monthly_playtime:
            monthly_playtime_item = MonthlyPlaytime.from_dict(monthly_playtime_item_data)

            monthly_playtime.append(monthly_playtime_item)

        peak_playtime_periods = d.pop("peak_playtime_periods", UNSET)

        peak_active_periods = d.pop("peak_active_periods", UNSET)

        daily_playtime_distribution = d.pop("daily_playtime_distribution", UNSET)

        anomalies = d.pop("anomalies", UNSET)

        predictive_insights = d.pop("predictive_insights", UNSET)

        guild_playtime_analysis = cls(
            total_playtime=total_playtime,
            total_unique_players=total_unique_players,
            daily_playtime=daily_playtime,
            weekly_playtime=weekly_playtime,
            monthly_playtime=monthly_playtime,
            peak_playtime_periods=peak_playtime_periods,
            peak_active_periods=peak_active_periods,
            daily_playtime_distribution=daily_playtime_distribution,
            anomalies=anomalies,
            predictive_insights=predictive_insights,
        )

        guild_playtime_analysis.additional_properties = d
        return guild_playtime_analysis

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
