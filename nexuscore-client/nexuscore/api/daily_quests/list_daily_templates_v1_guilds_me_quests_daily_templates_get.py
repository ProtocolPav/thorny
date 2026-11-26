from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daily_template_out import DailyTemplateOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    enabled: bool | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_enabled: bool | None | Unset
    if isinstance(enabled, Unset):
        json_enabled = UNSET
    else:
        json_enabled = enabled
    params["enabled"] = json_enabled

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/quests/daily/templates",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[DailyTemplateOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DailyTemplateOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | list[DailyTemplateOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    enabled: bool | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[DailyTemplateOut]]:
    """List Daily Templates

     List Daily Templates

    Returns the guild's pool of daily quest templates.

    Args:
        enabled (bool | None | Unset): Filter by enabled state

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[DailyTemplateOut]]
    """

    kwargs = _get_kwargs(
        enabled=enabled,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    enabled: bool | None | Unset = UNSET,
) -> HTTPValidationError | list[DailyTemplateOut] | None:
    """List Daily Templates

     List Daily Templates

    Returns the guild's pool of daily quest templates.

    Args:
        enabled (bool | None | Unset): Filter by enabled state

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[DailyTemplateOut]
    """

    return sync_detailed(
        client=client,
        enabled=enabled,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    enabled: bool | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[DailyTemplateOut]]:
    """List Daily Templates

     List Daily Templates

    Returns the guild's pool of daily quest templates.

    Args:
        enabled (bool | None | Unset): Filter by enabled state

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[DailyTemplateOut]]
    """

    kwargs = _get_kwargs(
        enabled=enabled,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    enabled: bool | None | Unset = UNSET,
) -> HTTPValidationError | list[DailyTemplateOut] | None:
    """List Daily Templates

     List Daily Templates

    Returns the guild's pool of daily quest templates.

    Args:
        enabled (bool | None | Unset): Filter by enabled state

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[DailyTemplateOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            enabled=enabled,
        )
    ).parsed
