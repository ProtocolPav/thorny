from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_out import UserOut
from ...types import Response


def _get_kwargs(
    thorny_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/guilds/me/users/{thorny_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserOut]]:
    if response.status_code == 200:
        response_200 = UserOut.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, UserOut]]:
    """Get User

     This returns the User object

    Args:
        thorny_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserOut]]
    """

    kwargs = _get_kwargs(
        thorny_id=thorny_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, UserOut]]:
    """Get User

     This returns the User object

    Args:
        thorny_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserOut]
    """

    return sync_detailed(
        thorny_id=thorny_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, UserOut]]:
    """Get User

     This returns the User object

    Args:
        thorny_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserOut]]
    """

    kwargs = _get_kwargs(
        thorny_id=thorny_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, UserOut]]:
    """Get User

     This returns the User object

    Args:
        thorny_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserOut]
    """

    return (
        await asyncio_detailed(
            thorny_id=thorny_id,
            client=client,
        )
    ).parsed
