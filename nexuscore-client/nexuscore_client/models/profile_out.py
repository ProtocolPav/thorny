from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProfileOut")


@_attrs_define
class ProfileOut:
    """
    Attributes:
        slogan (str): The slogan of the profile
        aboutme (str): The aboutme of the profile
        lore (str): The lore of the profile
        character_name (str): The character name of the profile
        character_age (int): The character age of the profile
        character_race (str): The character race of the profile
        character_role (str): The character role of the profile
        character_origin (str): The character origin of the profile
        character_beliefs (str): The character beliefs of the profile
        agility (int): The character agility of the profile
        valor (int): The character valor of the profile
        strength (int): The character strength of the profile
        charisma (int): The character charisma of the profile
        creativity (int): The character creativity of the profile
        ingenuity (int): The character ingeniu of the profile
    """

    slogan: str
    aboutme: str
    lore: str
    character_name: str
    character_age: int
    character_race: str
    character_role: str
    character_origin: str
    character_beliefs: str
    agility: int
    valor: int
    strength: int
    charisma: int
    creativity: int
    ingenuity: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        slogan = self.slogan

        aboutme = self.aboutme

        lore = self.lore

        character_name = self.character_name

        character_age = self.character_age

        character_race = self.character_race

        character_role = self.character_role

        character_origin = self.character_origin

        character_beliefs = self.character_beliefs

        agility = self.agility

        valor = self.valor

        strength = self.strength

        charisma = self.charisma

        creativity = self.creativity

        ingenuity = self.ingenuity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "slogan": slogan,
                "aboutme": aboutme,
                "lore": lore,
                "character_name": character_name,
                "character_age": character_age,
                "character_race": character_race,
                "character_role": character_role,
                "character_origin": character_origin,
                "character_beliefs": character_beliefs,
                "agility": agility,
                "valor": valor,
                "strength": strength,
                "charisma": charisma,
                "creativity": creativity,
                "ingenuity": ingenuity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        slogan = d.pop("slogan")

        aboutme = d.pop("aboutme")

        lore = d.pop("lore")

        character_name = d.pop("character_name")

        character_age = d.pop("character_age")

        character_race = d.pop("character_race")

        character_role = d.pop("character_role")

        character_origin = d.pop("character_origin")

        character_beliefs = d.pop("character_beliefs")

        agility = d.pop("agility")

        valor = d.pop("valor")

        strength = d.pop("strength")

        charisma = d.pop("charisma")

        creativity = d.pop("creativity")

        ingenuity = d.pop("ingenuity")

        profile_out = cls(
            slogan=slogan,
            aboutme=aboutme,
            lore=lore,
            character_name=character_name,
            character_age=character_age,
            character_race=character_race,
            character_role=character_role,
            character_origin=character_origin,
            character_beliefs=character_beliefs,
            agility=agility,
            valor=valor,
            strength=strength,
            charisma=charisma,
            creativity=creativity,
            ingenuity=ingenuity,
        )

        profile_out.additional_properties = d
        return profile_out

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
