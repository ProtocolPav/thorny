from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_progress_out import QuestProgressOut
from ...models.quest_progress_update import QuestProgressUpdate
from ...types import Response


def _get_kwargs(
    progress_id: int,
    *,
    body: QuestProgressUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/guilds/me/quests_router/progress/{progress_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, QuestProgressOut]]:
    if response.status_code == 200:
        response_200 = QuestProgressOut.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, QuestProgressOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    progress_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestProgressUpdate,
) -> Response[Union[HTTPValidationError, QuestProgressOut]]:
    """Partial Update Quest Progress

     Update Specific User's Quest

    Updates a user's quest.

    Args:
        progress_id (int):
        body (QuestProgressUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, QuestProgressOut]]
    """

    kwargs = _get_kwargs(
        progress_id=progress_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    progress_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestProgressUpdate,
) -> Optional[Union[HTTPValidationError, QuestProgressOut]]:
    """Partial Update Quest Progress

     Update Specific User's Quest

    Updates a user's quest.

    Args:
        progress_id (int):
        body (QuestProgressUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, QuestProgressOut]
    """

    return sync_detailed(
        progress_id=progress_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    progress_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestProgressUpdate,
) -> Response[Union[HTTPValidationError, QuestProgressOut]]:
    """Partial Update Quest Progress

     Update Specific User's Quest

    Updates a user's quest.

    Args:
        progress_id (int):
        body (QuestProgressUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, QuestProgressOut]]
    """

    kwargs = _get_kwargs(
        progress_id=progress_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    progress_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestProgressUpdate,
) -> Optional[Union[HTTPValidationError, QuestProgressOut]]:
    """Partial Update Quest Progress

     Update Specific User's Quest

    Updates a user's quest.

    Args:
        progress_id (int):
        body (QuestProgressUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, QuestProgressOut]
    """

    return (
        await asyncio_detailed(
            progress_id=progress_id,
            client=client,
            body=body,
        )
    ).parsed
