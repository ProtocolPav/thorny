import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.session_out import SessionOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    active: Union[None, Unset, bool] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_active: Union[None, Unset, bool]
    if isinstance(active, Unset):
        json_active = UNSET
    else:
        json_active = active
    params["active"] = json_active

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
        "url": "/v1/guilds/me/sessions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["SessionOut"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SessionOut.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["SessionOut"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    active: Union[None, Unset, bool] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["SessionOut"]]]:
    """List Sessions

     Returns a list of all sessions for the guild.

    Args:
        active (Union[None, Unset, bool]): Filter by active sessions
        time_start (Union[None, Unset, datetime.datetime]): Start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): End time to filter by
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SessionOut']]]
    """

    kwargs = _get_kwargs(
        active=active,
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
    active: Union[None, Unset, bool] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["SessionOut"]]]:
    """List Sessions

     Returns a list of all sessions for the guild.

    Args:
        active (Union[None, Unset, bool]): Filter by active sessions
        time_start (Union[None, Unset, datetime.datetime]): Start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): End time to filter by
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SessionOut']]
    """

    return sync_detailed(
        client=client,
        active=active,
        time_start=time_start,
        time_end=time_end,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    active: Union[None, Unset, bool] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["SessionOut"]]]:
    """List Sessions

     Returns a list of all sessions for the guild.

    Args:
        active (Union[None, Unset, bool]): Filter by active sessions
        time_start (Union[None, Unset, datetime.datetime]): Start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): End time to filter by
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SessionOut']]]
    """

    kwargs = _get_kwargs(
        active=active,
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
    active: Union[None, Unset, bool] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["SessionOut"]]]:
    """List Sessions

     Returns a list of all sessions for the guild.

    Args:
        active (Union[None, Unset, bool]): Filter by active sessions
        time_start (Union[None, Unset, datetime.datetime]): Start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): End time to filter by
        page (Union[None, Unset, int]): The page number of the results. Defaults to 1 Default: 1.
        page_size (Union[None, Unset, int]): The number of results per page. Defaults to 100
            Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SessionOut']]
    """

    return (
        await asyncio_detailed(
            client=client,
            active=active,
            time_start=time_start,
            time_end=time_end,
            page=page,
            page_size=page_size,
        )
    ).parsed
