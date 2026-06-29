from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.profile_out import ProfileOut
from ...models.profile_update import ProfileUpdate
from ...types import Response


def _get_kwargs(
    thorny_id: int,
    *,
    body: ProfileUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/guilds/me/users/{thorny_id}/profile".format(
            thorny_id=quote(str(thorny_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProfileOut | None:
    if response.status_code == 200:
        response_200 = ProfileOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProfileOut]:
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
    body: ProfileUpdate,
) -> Response[HTTPValidationError | ProfileOut]:
    """Partial Update Profile

     This updates a user's profile. Anything set to NULL will be ignored.

    Args:
        thorny_id (int):
        body (ProfileUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProfileOut]
    """

    kwargs = _get_kwargs(
        thorny_id=thorny_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    body: ProfileUpdate,
) -> HTTPValidationError | ProfileOut | None:
    """Partial Update Profile

     This updates a user's profile. Anything set to NULL will be ignored.

    Args:
        thorny_id (int):
        body (ProfileUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProfileOut
    """

    return sync_detailed(
        thorny_id=thorny_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    body: ProfileUpdate,
) -> Response[HTTPValidationError | ProfileOut]:
    """Partial Update Profile

     This updates a user's profile. Anything set to NULL will be ignored.

    Args:
        thorny_id (int):
        body (ProfileUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProfileOut]
    """

    kwargs = _get_kwargs(
        thorny_id=thorny_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    body: ProfileUpdate,
) -> HTTPValidationError | ProfileOut | None:
    """Partial Update Profile

     This updates a user's profile. Anything set to NULL will be ignored.

    Args:
        thorny_id (int):
        body (ProfileUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProfileOut
    """

    return (
        await asyncio_detailed(
            thorny_id=thorny_id,
            client=client,
            body=body,
        )
    ).parsed
