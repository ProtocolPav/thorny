from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.pin_out import PinOut
from ...types import Response


def _get_kwargs(
    pin_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/pins/{pin_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PinOut]]:
    if response.status_code == 200:
        response_200 = PinOut.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PinOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pin_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, PinOut]]:
    """Get Pin

     Returns the pin specified

    Args:
        pin_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PinOut]]
    """

    kwargs = _get_kwargs(
        pin_id=pin_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pin_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, PinOut]]:
    """Get Pin

     Returns the pin specified

    Args:
        pin_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PinOut]
    """

    return sync_detailed(
        pin_id=pin_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pin_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, PinOut]]:
    """Get Pin

     Returns the pin specified

    Args:
        pin_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PinOut]]
    """

    kwargs = _get_kwargs(
        pin_id=pin_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pin_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, PinOut]]:
    """Get Pin

     Returns the pin specified

    Args:
        pin_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PinOut]
    """

    return (
        await asyncio_detailed(
            pin_id=pin_id,
            client=client,
        )
    ).parsed
