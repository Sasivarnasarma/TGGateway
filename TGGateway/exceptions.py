# -*- coding: utf-8 -*-
"""Python Telegram Gateway API wrapper.

Module for defining exceptions related to the Telegram Gateway API client.

This module contains custom exception classes that are raised in response to
errors encountered while interacting with the Telegram Gateway API.

Classes:
    - TGGatewayException: Base class for all exceptions raised by the API client.
    - ApiError: Raised when the API returns an error response.
    - ResponseNotOk: Raised when the HTTP response status code is not 200 (OK).
"""

from httpx import Response


class TGGatewayException(Exception):
    """Base class for all exceptions raised by the Telegram Gateway API client.

    This exception serves as the base class for all other exceptions
    related to errors encountered when using the Telegram Gateway API client.
    """


class ApiError(TGGatewayException):
    """Exception raised when the Telegram Gateway API returns an error.

    This exception is raised when the API returns an error response, typically
    with an 'error' field in the response body.
    """


class ResponseNotOk(TGGatewayException):
    """Exception raised when the HTTP response status code is not OK (i.e., not 200).

    Attributes:
        response (httpx.Response): The response object containing the status code and other details.

    This exception is raised when the HTTP response from the Telegram Gateway API
    has a status code that indicates an error (status code >= 400).
    """

    def __init__(self, response: Response):
        self.response = response
        super().__init__(
            f"The response is not OK. Status Code:- {response.status_code}"
        )
