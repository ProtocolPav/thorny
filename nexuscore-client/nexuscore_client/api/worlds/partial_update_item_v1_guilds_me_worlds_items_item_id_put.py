from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.item_model import ItemModel
from ...models.item_update_model import ItemUpdateModel
from ...types import Response


def _get_kwargs(
    item_id: str,
    *,
    body: ItemUpdateModel,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/guilds/me/worlds/items/{item_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ItemModel]]:
    if response.status_code == 200:
        response_200 = ItemModel.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ItemModel]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    item_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemUpdateModel,
) -> Response[Union[HTTPValidationError, ItemModel]]:
    """Partial Update Item

     Update Item

    This updates an item. All fields are optional, meaning you may
    set a field to `null` to not update it.

    Args:
        item_id (str):
        body (ItemUpdateModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ItemModel]]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemUpdateModel,
) -> Optional[Union[HTTPValidationError, ItemModel]]:
    """Partial Update Item

     Update Item

    This updates an item. All fields are optional, meaning you may
    set a field to `null` to not update it.

    Args:
        item_id (str):
        body (ItemUpdateModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ItemModel]
    """

    return sync_detailed(
        item_id=item_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    item_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemUpdateModel,
) -> Response[Union[HTTPValidationError, ItemModel]]:
    """Partial Update Item

     Update Item

    This updates an item. All fields are optional, meaning you may
    set a field to `null` to not update it.

    Args:
        item_id (str):
        body (ItemUpdateModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ItemModel]]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemUpdateModel,
) -> Optional[Union[HTTPValidationError, ItemModel]]:
    """Partial Update Item

     Update Item

    This updates an item. All fields are optional, meaning you may
    set a field to `null` to not update it.

    Args:
        item_id (str):
        body (ItemUpdateModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ItemModel]
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            body=body,
        )
    ).parsed
