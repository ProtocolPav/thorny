from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_out import QuestOut
from ...models.quest_update import QuestUpdate
from ...types import Response


def _get_kwargs(
    quest_id: int,
    *,
    body: QuestUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/guilds/me/quests/{quest_id}".format(
            quest_id=quote(str(quest_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | QuestOut | None:
    if response.status_code == 200:
        response_200 = QuestOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | QuestOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    quest_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestUpdate,
) -> Response[HTTPValidationError | QuestOut]:
    """Partial Update Quest

     Updates quest details and/or objectives. Objectives and rewards are additive-only:
    include an `objective_id`/`reward_id` to update an existing entry, or omit it to create a new one.
    Existing objectives and rewards not present in the payload are left untouched.

    Args:
        quest_id (int):
        body (QuestUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestOut]
    """

    kwargs = _get_kwargs(
        quest_id=quest_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    quest_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestUpdate,
) -> HTTPValidationError | QuestOut | None:
    """Partial Update Quest

     Updates quest details and/or objectives. Objectives and rewards are additive-only:
    include an `objective_id`/`reward_id` to update an existing entry, or omit it to create a new one.
    Existing objectives and rewards not present in the payload are left untouched.

    Args:
        quest_id (int):
        body (QuestUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestOut
    """

    return sync_detailed(
        quest_id=quest_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    quest_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestUpdate,
) -> Response[HTTPValidationError | QuestOut]:
    """Partial Update Quest

     Updates quest details and/or objectives. Objectives and rewards are additive-only:
    include an `objective_id`/`reward_id` to update an existing entry, or omit it to create a new one.
    Existing objectives and rewards not present in the payload are left untouched.

    Args:
        quest_id (int):
        body (QuestUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestOut]
    """

    kwargs = _get_kwargs(
        quest_id=quest_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    quest_id: int,
    *,
    client: AuthenticatedClient,
    body: QuestUpdate,
) -> HTTPValidationError | QuestOut | None:
    """Partial Update Quest

     Updates quest details and/or objectives. Objectives and rewards are additive-only:
    include an `objective_id`/`reward_id` to update an existing entry, or omit it to create a new one.
    Existing objectives and rewards not present in the payload are left untouched.

    Args:
        quest_id (int):
        body (QuestUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestOut
    """

    return (
        await asyncio_detailed(
            quest_id=quest_id,
            client=client,
            body=body,
        )
    ).parsed
