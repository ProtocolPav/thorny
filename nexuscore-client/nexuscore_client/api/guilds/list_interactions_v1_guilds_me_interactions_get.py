import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.interaction_out import InteractionOut
from ...models.list_interactions_v1_guilds_me_interactions_get_interaction_types_type_0_item import (
    ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    coordinates: Union[None, Unset, list[int]] = UNSET,
    coordinates_end: Union[None, Unset, list[int]] = UNSET,
    thorny_ids: Union[None, Unset, list[int]] = UNSET,
    interaction_types: Union[
        None, Unset, list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]
    ] = UNSET,
    references: Union[None, Unset, list[str]] = UNSET,
    dimensions: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_coordinates: Union[None, Unset, list[int]]
    if isinstance(coordinates, Unset):
        json_coordinates = UNSET
    elif isinstance(coordinates, list):
        json_coordinates = coordinates

    else:
        json_coordinates = coordinates
    params["coordinates"] = json_coordinates

    json_coordinates_end: Union[None, Unset, list[int]]
    if isinstance(coordinates_end, Unset):
        json_coordinates_end = UNSET
    elif isinstance(coordinates_end, list):
        json_coordinates_end = coordinates_end

    else:
        json_coordinates_end = coordinates_end
    params["coordinates_end"] = json_coordinates_end

    json_thorny_ids: Union[None, Unset, list[int]]
    if isinstance(thorny_ids, Unset):
        json_thorny_ids = UNSET
    elif isinstance(thorny_ids, list):
        json_thorny_ids = thorny_ids

    else:
        json_thorny_ids = thorny_ids
    params["thorny_ids"] = json_thorny_ids

    json_interaction_types: Union[None, Unset, list[str]]
    if isinstance(interaction_types, Unset):
        json_interaction_types = UNSET
    elif isinstance(interaction_types, list):
        json_interaction_types = []
        for interaction_types_type_0_item_data in interaction_types:
            interaction_types_type_0_item = interaction_types_type_0_item_data.value
            json_interaction_types.append(interaction_types_type_0_item)

    else:
        json_interaction_types = interaction_types
    params["interaction_types"] = json_interaction_types

    json_references: Union[None, Unset, list[str]]
    if isinstance(references, Unset):
        json_references = UNSET
    elif isinstance(references, list):
        json_references = references

    else:
        json_references = references
    params["references"] = json_references

    json_dimensions: Union[None, Unset, list[str]]
    if isinstance(dimensions, Unset):
        json_dimensions = UNSET
    elif isinstance(dimensions, list):
        json_dimensions = dimensions

    else:
        json_dimensions = dimensions
    params["dimensions"] = json_dimensions

    json_time_start: Union[None, Unset, str]
    if isinstance(time_start, Unset):
        json_time_start = UNSET
    elif isinstance(time_start, datetime.datetime):
        json_time_start = time_start.isoformat()
    else:
        json_time_start = time_start
    params["time_start"] = json_time_start

    json_time_end: Union[None, Unset, str]
    if isinstance(time_end, Unset):
        json_time_end = UNSET
    elif isinstance(time_end, datetime.datetime):
        json_time_end = time_end.isoformat()
    else:
        json_time_end = time_end
    params["time_end"] = json_time_end

    json_page: Union[None, Unset, int]
    if isinstance(page, Unset):
        json_page = UNSET
    else:
        json_page = page
    params["page"] = json_page

    json_page_size: Union[None, Unset, int]
    if isinstance(page_size, Unset):
        json_page_size = UNSET
    else:
        json_page_size = page_size
    params["page_size"] = json_page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/interactions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["InteractionOut"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = InteractionOut.from_dict(response_200_item_data)

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, list["InteractionOut"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    coordinates: Union[None, Unset, list[int]] = UNSET,
    coordinates_end: Union[None, Unset, list[int]] = UNSET,
    thorny_ids: Union[None, Unset, list[int]] = UNSET,
    interaction_types: Union[
        None, Unset, list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]
    ] = UNSET,
    references: Union[None, Unset, list[str]] = UNSET,
    dimensions: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["InteractionOut"]]]:
    """List Interactions

     Filter interactions by various criteria.

    Args:
        coordinates (Union[None, Unset, list[int]]): The coordinates where it happened
        coordinates_end (Union[None, Unset, list[int]]): Optional End coordinates
        thorny_ids (Union[None, Unset, list[int]]): The thorny IDs to filter by
        interaction_types (Union[None, Unset,
            list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]]): The
            interaction types to filter by
        references (Union[None, Unset, list[str]]): The references to filter by
        dimensions (Union[None, Unset, list[str]]): The dimensions to filter by
        time_start (Union[None, Unset, datetime.datetime]): The start time of the interaction
            events
        time_end (Union[None, Unset, datetime.datetime]): The end time of the interaction events
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['InteractionOut']]]
    """

    kwargs = _get_kwargs(
        coordinates=coordinates,
        coordinates_end=coordinates_end,
        thorny_ids=thorny_ids,
        interaction_types=interaction_types,
        references=references,
        dimensions=dimensions,
        time_start=time_start,
        time_end=time_end,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    coordinates: Union[None, Unset, list[int]] = UNSET,
    coordinates_end: Union[None, Unset, list[int]] = UNSET,
    thorny_ids: Union[None, Unset, list[int]] = UNSET,
    interaction_types: Union[
        None, Unset, list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]
    ] = UNSET,
    references: Union[None, Unset, list[str]] = UNSET,
    dimensions: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["InteractionOut"]]]:
    """List Interactions

     Filter interactions by various criteria.

    Args:
        coordinates (Union[None, Unset, list[int]]): The coordinates where it happened
        coordinates_end (Union[None, Unset, list[int]]): Optional End coordinates
        thorny_ids (Union[None, Unset, list[int]]): The thorny IDs to filter by
        interaction_types (Union[None, Unset,
            list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]]): The
            interaction types to filter by
        references (Union[None, Unset, list[str]]): The references to filter by
        dimensions (Union[None, Unset, list[str]]): The dimensions to filter by
        time_start (Union[None, Unset, datetime.datetime]): The start time of the interaction
            events
        time_end (Union[None, Unset, datetime.datetime]): The end time of the interaction events
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['InteractionOut']]
    """

    return sync_detailed(
        client=client,
        coordinates=coordinates,
        coordinates_end=coordinates_end,
        thorny_ids=thorny_ids,
        interaction_types=interaction_types,
        references=references,
        dimensions=dimensions,
        time_start=time_start,
        time_end=time_end,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    coordinates: Union[None, Unset, list[int]] = UNSET,
    coordinates_end: Union[None, Unset, list[int]] = UNSET,
    thorny_ids: Union[None, Unset, list[int]] = UNSET,
    interaction_types: Union[
        None, Unset, list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]
    ] = UNSET,
    references: Union[None, Unset, list[str]] = UNSET,
    dimensions: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["InteractionOut"]]]:
    """List Interactions

     Filter interactions by various criteria.

    Args:
        coordinates (Union[None, Unset, list[int]]): The coordinates where it happened
        coordinates_end (Union[None, Unset, list[int]]): Optional End coordinates
        thorny_ids (Union[None, Unset, list[int]]): The thorny IDs to filter by
        interaction_types (Union[None, Unset,
            list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]]): The
            interaction types to filter by
        references (Union[None, Unset, list[str]]): The references to filter by
        dimensions (Union[None, Unset, list[str]]): The dimensions to filter by
        time_start (Union[None, Unset, datetime.datetime]): The start time of the interaction
            events
        time_end (Union[None, Unset, datetime.datetime]): The end time of the interaction events
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['InteractionOut']]]
    """

    kwargs = _get_kwargs(
        coordinates=coordinates,
        coordinates_end=coordinates_end,
        thorny_ids=thorny_ids,
        interaction_types=interaction_types,
        references=references,
        dimensions=dimensions,
        time_start=time_start,
        time_end=time_end,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    coordinates: Union[None, Unset, list[int]] = UNSET,
    coordinates_end: Union[None, Unset, list[int]] = UNSET,
    thorny_ids: Union[None, Unset, list[int]] = UNSET,
    interaction_types: Union[
        None, Unset, list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]
    ] = UNSET,
    references: Union[None, Unset, list[str]] = UNSET,
    dimensions: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["InteractionOut"]]]:
    """List Interactions

     Filter interactions by various criteria.

    Args:
        coordinates (Union[None, Unset, list[int]]): The coordinates where it happened
        coordinates_end (Union[None, Unset, list[int]]): Optional End coordinates
        thorny_ids (Union[None, Unset, list[int]]): The thorny IDs to filter by
        interaction_types (Union[None, Unset,
            list[ListInteractionsV1GuildsMeInteractionsGetInteractionTypesType0Item]]): The
            interaction types to filter by
        references (Union[None, Unset, list[str]]): The references to filter by
        dimensions (Union[None, Unset, list[str]]): The dimensions to filter by
        time_start (Union[None, Unset, datetime.datetime]): The start time of the interaction
            events
        time_end (Union[None, Unset, datetime.datetime]): The end time of the interaction events
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['InteractionOut']]
    """

    return (
        await asyncio_detailed(
            client=client,
            coordinates=coordinates,
            coordinates_end=coordinates_end,
            thorny_ids=thorny_ids,
            interaction_types=interaction_types,
            references=references,
            dimensions=dimensions,
            time_start=time_start,
            time_end=time_end,
            page=page,
            page_size=page_size,
        )
    ).parsed
