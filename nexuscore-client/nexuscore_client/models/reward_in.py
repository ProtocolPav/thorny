from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.damage_model import DamageModel
    from ..models.enchantment_model import EnchantmentModel
    from ..models.lore_model import LoreModel
    from ..models.name_model import NameModel
    from ..models.potion_model import PotionModel
    from ..models.random_enchantment_model import RandomEnchantmentModel


T = TypeVar("T", bound="RewardIn")


@_attrs_define
class RewardIn:
    """
    Attributes:
        balance (Union[None, int]):
        item (Union[None, str]):
        count (Union[None, int]):
        display_name (Union[None, str]):
        item_metadata (list[Union['DamageModel', 'EnchantmentModel', 'LoreModel', 'NameModel', 'PotionModel',
            'RandomEnchantmentModel']]): The metadata for the item reward, to add extra customization
    """

    balance: Union[None, int]
    item: Union[None, str]
    count: Union[None, int]
    display_name: Union[None, str]
    item_metadata: list[
        Union["DamageModel", "EnchantmentModel", "LoreModel", "NameModel", "PotionModel", "RandomEnchantmentModel"]
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.enchantment_model import EnchantmentModel
        from ..models.lore_model import LoreModel
        from ..models.name_model import NameModel
        from ..models.potion_model import PotionModel
        from ..models.random_enchantment_model import RandomEnchantmentModel

        balance: Union[None, int]
        balance = self.balance

        item: Union[None, str]
        item = self.item

        count: Union[None, int]
        count = self.count

        display_name: Union[None, str]
        display_name = self.display_name

        item_metadata = []
        for item_metadata_item_data in self.item_metadata:
            item_metadata_item: dict[str, Any]
            if isinstance(item_metadata_item_data, EnchantmentModel):
                item_metadata_item = item_metadata_item_data.to_dict()
            elif isinstance(item_metadata_item_data, RandomEnchantmentModel):
                item_metadata_item = item_metadata_item_data.to_dict()
            elif isinstance(item_metadata_item_data, PotionModel):
                item_metadata_item = item_metadata_item_data.to_dict()
            elif isinstance(item_metadata_item_data, NameModel):
                item_metadata_item = item_metadata_item_data.to_dict()
            elif isinstance(item_metadata_item_data, LoreModel):
                item_metadata_item = item_metadata_item_data.to_dict()
            else:
                item_metadata_item = item_metadata_item_data.to_dict()

            item_metadata.append(item_metadata_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "balance": balance,
                "item": item,
                "count": count,
                "display_name": display_name,
                "item_metadata": item_metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.damage_model import DamageModel
        from ..models.enchantment_model import EnchantmentModel
        from ..models.lore_model import LoreModel
        from ..models.name_model import NameModel
        from ..models.potion_model import PotionModel
        from ..models.random_enchantment_model import RandomEnchantmentModel

        d = dict(src_dict)

        def _parse_balance(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        balance = _parse_balance(d.pop("balance"))

        def _parse_item(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        item = _parse_item(d.pop("item"))

        def _parse_count(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        count = _parse_count(d.pop("count"))

        def _parse_display_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        display_name = _parse_display_name(d.pop("display_name"))

        item_metadata = []
        _item_metadata = d.pop("item_metadata")
        for item_metadata_item_data in _item_metadata:

            def _parse_item_metadata_item(
                data: object,
            ) -> Union[
                "DamageModel", "EnchantmentModel", "LoreModel", "NameModel", "PotionModel", "RandomEnchantmentModel"
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    item_metadata_item_type_0 = EnchantmentModel.from_dict(data)

                    return item_metadata_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    item_metadata_item_type_1 = RandomEnchantmentModel.from_dict(data)

                    return item_metadata_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    item_metadata_item_type_2 = PotionModel.from_dict(data)

                    return item_metadata_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    item_metadata_item_type_3 = NameModel.from_dict(data)

                    return item_metadata_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    item_metadata_item_type_4 = LoreModel.from_dict(data)

                    return item_metadata_item_type_4
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                item_metadata_item_type_5 = DamageModel.from_dict(data)

                return item_metadata_item_type_5

            item_metadata_item = _parse_item_metadata_item(item_metadata_item_data)

            item_metadata.append(item_metadata_item)

        reward_in = cls(
            balance=balance,
            item=item,
            count=count,
            display_name=display_name,
            item_metadata=item_metadata,
        )

        reward_in.additional_properties = d
        return reward_in

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
