from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileUpdate")


@_attrs_define
class ProfileUpdate:
    """
    Attributes:
        slogan (str | Unset): The slogan of the profile
        aboutme (str | Unset): The aboutme of the profile
        lore (str | Unset): The lore of the profile
        character_name (str | Unset): The character name of the profile
        character_age (int | Unset): The character age of the profile
        character_race (str | Unset): The character race of the profile
        character_role (str | Unset): The character role of the profile
        character_origin (str | Unset): The character origin of the profile
        character_beliefs (str | Unset): The character beliefs of the profile
        agility (int | Unset): The character agility of the profile
        valor (int | Unset): The character valor of the profile
        strength (int | Unset): The character strength of the profile
        charisma (int | Unset): The character charisma of the profile
        creativity (int | Unset): The character creativity of the profile
        ingenuity (int | Unset): The character ingeniu of the profile
    """

    slogan: str | Unset = UNSET
    aboutme: str | Unset = UNSET
    lore: str | Unset = UNSET
    character_name: str | Unset = UNSET
    character_age: int | Unset = UNSET
    character_race: str | Unset = UNSET
    character_role: str | Unset = UNSET
    character_origin: str | Unset = UNSET
    character_beliefs: str | Unset = UNSET
    agility: int | Unset = UNSET
    valor: int | Unset = UNSET
    strength: int | Unset = UNSET
    charisma: int | Unset = UNSET
    creativity: int | Unset = UNSET
    ingenuity: int | Unset = UNSET
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
        field_dict.update({})
        if slogan is not UNSET:
            field_dict["slogan"] = slogan
        if aboutme is not UNSET:
            field_dict["aboutme"] = aboutme
        if lore is not UNSET:
            field_dict["lore"] = lore
        if character_name is not UNSET:
            field_dict["character_name"] = character_name
        if character_age is not UNSET:
            field_dict["character_age"] = character_age
        if character_race is not UNSET:
            field_dict["character_race"] = character_race
        if character_role is not UNSET:
            field_dict["character_role"] = character_role
        if character_origin is not UNSET:
            field_dict["character_origin"] = character_origin
        if character_beliefs is not UNSET:
            field_dict["character_beliefs"] = character_beliefs
        if agility is not UNSET:
            field_dict["agility"] = agility
        if valor is not UNSET:
            field_dict["valor"] = valor
        if strength is not UNSET:
            field_dict["strength"] = strength
        if charisma is not UNSET:
            field_dict["charisma"] = charisma
        if creativity is not UNSET:
            field_dict["creativity"] = creativity
        if ingenuity is not UNSET:
            field_dict["ingenuity"] = ingenuity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        slogan = d.pop("slogan", UNSET)

        aboutme = d.pop("aboutme", UNSET)

        lore = d.pop("lore", UNSET)

        character_name = d.pop("character_name", UNSET)

        character_age = d.pop("character_age", UNSET)

        character_race = d.pop("character_race", UNSET)

        character_role = d.pop("character_role", UNSET)

        character_origin = d.pop("character_origin", UNSET)

        character_beliefs = d.pop("character_beliefs", UNSET)

        agility = d.pop("agility", UNSET)

        valor = d.pop("valor", UNSET)

        strength = d.pop("strength", UNSET)

        charisma = d.pop("charisma", UNSET)

        creativity = d.pop("creativity", UNSET)

        ingenuity = d.pop("ingenuity", UNSET)

        profile_update = cls(
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

        profile_update.additional_properties = d
        return profile_update

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
