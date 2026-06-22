from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_get_token_auth_token_post import BodyGetTokenAuthTokenPost
from ...models.http_validation_error import HTTPValidationError
from ...models.token_response import TokenResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyGetTokenAuthTokenPost,
    authorization: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["Authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/token",
    }

    _body = body.to_dict()

    _kwargs["data"] = _body
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TokenResponse]]:
    if response.status_code == 200:
        response_200 = TokenResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TokenResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyGetTokenAuthTokenPost,
    authorization: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TokenResponse]]:
    """Get Token

    Args:
        authorization (Union[None, Unset, str]): Basic Auth credentials as `Basic
            base64(client_id:client_secret)`. Takes priority over body if both are provided.
        body (BodyGetTokenAuthTokenPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyGetTokenAuthTokenPost,
    authorization: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TokenResponse]]:
    """Get Token

    Args:
        authorization (Union[None, Unset, str]): Basic Auth credentials as `Basic
            base64(client_id:client_secret)`. Takes priority over body if both are provided.
        body (BodyGetTokenAuthTokenPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyGetTokenAuthTokenPost,
    authorization: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TokenResponse]]:
    """Get Token

    Args:
        authorization (Union[None, Unset, str]): Basic Auth credentials as `Basic
            base64(client_id:client_secret)`. Takes priority over body if both are provided.
        body (BodyGetTokenAuthTokenPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyGetTokenAuthTokenPost,
    authorization: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TokenResponse]]:
    """Get Token

    Args:
        authorization (Union[None, Unset, str]): Basic Auth credentials as `Basic
            base64(client_id:client_secret)`. Takes priority over body if both are provided.
        body (BodyGetTokenAuthTokenPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
