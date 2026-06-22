from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.damage_model import DamageModel
    from ..models.enchantment_model import EnchantmentModel
    from ..models.lore_model import LoreModel
    from ..models.name_model import NameModel
    from ..models.potion_model import PotionModel
    from ..models.random_enchantment_model import RandomEnchantmentModel


T = TypeVar("T", bound="RewardUpdate")


@_attrs_define
class RewardUpdate:
    """
    Attributes:
        reward_id (Union[None, Unset, int]):
        balance (Union[None, Unset, int]):
        item (Union[None, Unset, str]):
        count (Union[None, Unset, int]):
        display_name (Union[None, Unset, str]):
        item_metadata (Union[None, Unset, list[Union['DamageModel', 'EnchantmentModel', 'LoreModel', 'NameModel',
            'PotionModel', 'RandomEnchantmentModel']]]):
    """

    reward_id: Union[None, Unset, int] = UNSET
    balance: Union[None, Unset, int] = UNSET
    item: Union[None, Unset, str] = UNSET
    count: Union[None, Unset, int] = UNSET
    display_name: Union[None, Unset, str] = UNSET
    item_metadata: Union[
        None,
        Unset,
        list[
            Union["DamageModel", "EnchantmentModel", "LoreModel", "NameModel", "PotionModel", "RandomEnchantmentModel"]
        ],
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.enchantment_model import EnchantmentModel
        from ..models.lore_model import LoreModel
        from ..models.name_model import NameModel
        from ..models.potion_model import PotionModel
        from ..models.random_enchantment_model import RandomEnchantmentModel

        reward_id: Union[None, Unset, int]
        if isinstance(self.reward_id, Unset):
            reward_id = UNSET
        else:
            reward_id = self.reward_id

        balance: Union[None, Unset, int]
        if isinstance(self.balance, Unset):
            balance = UNSET
        else:
            balance = self.balance

        item: Union[None, Unset, str]
        if isinstance(self.item, Unset):
            item = UNSET
        else:
            item = self.item

        count: Union[None, Unset, int]
        if isinstance(self.count, Unset):
            count = UNSET
        else:
            count = self.count

        display_name: Union[None, Unset, str]
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        item_metadata: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.item_metadata, Unset):
            item_metadata = UNSET
        elif isinstance(self.item_metadata, list):
            item_metadata = []
            for item_metadata_type_0_item_data in self.item_metadata:
                item_metadata_type_0_item: dict[str, Any]
                if isinstance(item_metadata_type_0_item_data, EnchantmentModel):
                    item_metadata_type_0_item = item_metadata_type_0_item_data.to_dict()
                elif isinstance(item_metadata_type_0_item_data, RandomEnchantmentModel):
                    item_metadata_type_0_item = item_metadata_type_0_item_data.to_dict()
                elif isinstance(item_metadata_type_0_item_data, PotionModel):
                    item_metadata_type_0_item = item_metadata_type_0_item_data.to_dict()
                elif isinstance(item_metadata_type_0_item_data, NameModel):
                    item_metadata_type_0_item = item_metadata_type_0_item_data.to_dict()
                elif isinstance(item_metadata_type_0_item_data, LoreModel):
                    item_metadata_type_0_item = item_metadata_type_0_item_data.to_dict()
                else:
                    item_metadata_type_0_item = item_metadata_type_0_item_data.to_dict()

                item_metadata.append(item_metadata_type_0_item)

        else:
            item_metadata = self.item_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reward_id is not UNSET:
            field_dict["reward_id"] = reward_id
        if balance is not UNSET:
            field_dict["balance"] = balance
        if item is not UNSET:
            field_dict["item"] = item
        if count is not UNSET:
            field_dict["count"] = count
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if item_metadata is not UNSET:
            field_dict["item_metadata"] = item_metadata

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

        def _parse_reward_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        reward_id = _parse_reward_id(d.pop("reward_id", UNSET))

        def _parse_balance(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        balance = _parse_balance(d.pop("balance", UNSET))

        def _parse_item(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        item = _parse_item(d.pop("item", UNSET))

        def _parse_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        count = _parse_count(d.pop("count", UNSET))

        def _parse_display_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        display_name = _parse_display_name(d.pop("display_name", UNSET))

        def _parse_item_metadata(
            data: object,
        ) -> Union[
            None,
            Unset,
            list[
                Union[
                    "DamageModel", "EnchantmentModel", "LoreModel", "NameModel", "PotionModel", "RandomEnchantmentModel"
                ]
            ],
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                item_metadata_type_0 = []
                _item_metadata_type_0 = data
                for item_metadata_type_0_item_data in _item_metadata_type_0:

                    def _parse_item_metadata_type_0_item(
                        data: object,
                    ) -> Union[
                        "DamageModel",
                        "EnchantmentModel",
                        "LoreModel",
                        "NameModel",
                        "PotionModel",
                        "RandomEnchantmentModel",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            item_metadata_type_0_item_type_0 = EnchantmentModel.from_dict(data)

                            return item_metadata_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            item_metadata_type_0_item_type_1 = RandomEnchantmentModel.from_dict(data)

                            return item_metadata_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            item_metadata_type_0_item_type_2 = PotionModel.from_dict(data)

                            return item_metadata_type_0_item_type_2
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            item_metadata_type_0_item_type_3 = NameModel.from_dict(data)

                            return item_metadata_type_0_item_type_3
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            item_metadata_type_0_item_type_4 = LoreModel.from_dict(data)

                            return item_metadata_type_0_item_type_4
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        item_metadata_type_0_item_type_5 = DamageModel.from_dict(data)

                        return item_metadata_type_0_item_type_5

                    item_metadata_type_0_item = _parse_item_metadata_type_0_item(item_metadata_type_0_item_data)

                    item_metadata_type_0.append(item_metadata_type_0_item)

                return item_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list[
                        Union[
                            "DamageModel",
                            "EnchantmentModel",
                            "LoreModel",
                            "NameModel",
                            "PotionModel",
                            "RandomEnchantmentModel",
                        ]
                    ],
                ],
                data,
            )

        item_metadata = _parse_item_metadata(d.pop("item_metadata", UNSET))

        reward_update = cls(
            reward_id=reward_id,
            balance=balance,
            item=item,
            count=count,
            display_name=display_name,
            item_metadata=item_metadata,
        )

        reward_update.additional_properties = d
        return reward_update

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
