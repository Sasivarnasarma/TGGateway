# -*- coding: utf-8 -*-

"""Python Telegram Gateway API wrapper.
For detailed API references, check the Official API Documentation
https://core.telegram.org/gateway/api

@author: Sasivarnasarma
@contact: sasivarnasarma@protonmail.com
@license MIT License, see LICENSE file

Copyright (C) 2024-2025
"""

__title__ = "TGGateway"
__author__ = "Sasivarnasarma"
__version__ = "2.0.0"
__all__ = (
    "__version__",
    "TGGateway",
    "AsyncTGGateway",
    "TGGatewayException",
    "ApiError",
    "ResponseNotOk",
    "DeliveryStatus",
    "VerificationStatus",
    "RequestStatus",
)

from ._api import TGGateway
from ._api_async import AsyncTGGateway
from .exceptions import TGGatewayException, ApiError, ResponseNotOk
from .types import DeliveryStatus, VerificationStatus, RequestStatus
