from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.pin_out import PinOut
from ...models.pin_update import PinUpdate
from ...types import Response


def _get_kwargs(
    pin_id: int,
    *,
    body: PinUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/pins/{pin_id}".format(
            pin_id=quote(str(pin_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PinOut | None:
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
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | PinOut]:
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
    body: PinUpdate,
) -> Response[HTTPValidationError | PinOut]:
    """Partial Update Pin

     Update Pin

    Update the pin. Anything that you do not want to update can be left as `null`

    Args:
        pin_id (int):
        body (PinUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PinOut]
    """

    kwargs = _get_kwargs(
        pin_id=pin_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pin_id: int,
    *,
    client: AuthenticatedClient,
    body: PinUpdate,
) -> HTTPValidationError | PinOut | None:
    """Partial Update Pin

     Update Pin

    Update the pin. Anything that you do not want to update can be left as `null`

    Args:
        pin_id (int):
        body (PinUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PinOut
    """

    return sync_detailed(
        pin_id=pin_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    pin_id: int,
    *,
    client: AuthenticatedClient,
    body: PinUpdate,
) -> Response[HTTPValidationError | PinOut]:
    """Partial Update Pin

     Update Pin

    Update the pin. Anything that you do not want to update can be left as `null`

    Args:
        pin_id (int):
        body (PinUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PinOut]
    """

    kwargs = _get_kwargs(
        pin_id=pin_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pin_id: int,
    *,
    client: AuthenticatedClient,
    body: PinUpdate,
) -> HTTPValidationError | PinOut | None:
    """Partial Update Pin

     Update Pin

    Update the pin. Anything that you do not want to update can be left as `null`

    Args:
        pin_id (int):
        body (PinUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PinOut
    """

    return (
        await asyncio_detailed(
            pin_id=pin_id,
            client=client,
            body=body,
        )
    ).parsed
