from dataclasses import dataclass
from typing import Optional


@dataclass
class MainhandCustomization:
    item: str

@dataclass
class LocationCustomization:
    coordinates: tuple[int, int, int]
    horizontal_radius: int
    vertical_radius: int

@dataclass
class TimerCustomization:
    seconds: int
    fail: bool

@dataclass
class MaximumDeathsCustomization:
    deaths: int
    fail: bool

@dataclass
class NaturalBlockCustomization:
    pass

@dataclass
class Customizations:
    mainhand: Optional[MainhandCustomization] = None
    location: Optional[LocationCustomization] = None
    timer: Optional[TimerCustomization] = None
    maximum_deaths: Optional[MaximumDeathsCustomization] = None
    natural_block: Optional[NaturalBlockCustomization] = None

    @classmethod
    def build(cls, data: dict):
        if not data:
            return cls()

        # Build Mainhand
        mainhand = None
        if data.get('mainhand'):
            mainhand = MainhandCustomization(**data['mainhand'])

        # Build Location
        location = None
        if data.get('location'):
            # Ensure coordinates are a tuple
            loc_data = data['location']
            if isinstance(loc_data.get('coordinates'), list):
                loc_data['coordinates'] = tuple(loc_data['coordinates'])
            location = LocationCustomization(**loc_data)

        # Build Timer
        timer = None
        if data.get('timer'):
            timer = TimerCustomization(**data['timer'])

        # Build Max Deaths
        max_deaths = None
        if data.get('maximum_deaths'):
            max_deaths = MaximumDeathsCustomization(**data['maximum_deaths'])

        # Build Natural Block
        natural_block = None
        if data.get('natural_block') is not None:
            # It might be an empty dict {} or None in JSON
            natural_block = NaturalBlockCustomization()

        return cls(
            mainhand=mainhand,
            location=location,
            timer=timer,
            maximum_deaths=max_deaths,
            natural_block=natural_block
        )