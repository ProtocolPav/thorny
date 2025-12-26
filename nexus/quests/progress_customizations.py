from dataclasses import dataclass
from typing import Optional


@dataclass
class DeathCustomizationProgress:
    deaths: int = 0

    @classmethod
    def build(cls, data: dict):
        return cls(deaths=data.get('deaths', 0))


@dataclass
class CustomizationProgress:
    maximum_deaths: Optional[DeathCustomizationProgress] = None

    @classmethod
    def build(cls, data: dict):
        if not data:
            return cls()

        max_deaths = None
        if data.get('maximum_deaths'):
            max_deaths = DeathCustomizationProgress.build(data['maximum_deaths'])

        return cls(maximum_deaths=max_deaths)