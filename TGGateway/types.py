# -*- coding: utf-8 -*-
"""
Module for representing the status of a verification message request.

This module defines data classes for tracking the status of various components in a message
verification system, including the message delivery status, verification process status, and
the overall request status.

Classes:
    - DeliveryStatus: Represents the status of a message delivery.
    - VerificationStatus: Represents the status of the verification process.
    - RequestStatus: Represents the status of a verification message request, including
      delivery and verification statuses.

@author: Sasivarnasarma
@contact: sasivarnasarma@protonmail.com
@license MIT License, see LICENSE file

Copyright (C) 2024-2025
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class DeliveryStatus:
    """Represents the status of a message delivery.

    Attributes:
        status (Literal): The current status of the message.
                           It can be one of "sent", "delivered", "read", "expired", or "revoked".
        updated_at (int): The Unix timestamp when the status was last updated.
    """

    status: Literal[
        "sent", "delivered", "read", "expired", "revoked"
    ]  # The current status of the message.
    updated_at: int  # Status last updated Timestamp as an integer (Unix timestamp)


@dataclass
class VerificationStatus:
    """Represents the status of the verification process.

    Attributes:
        status (Literal): The current status of the verification process.
                           It can be one of "code_valid", "code_invalid",
                           "code_max_attempts_exceeded", or "expired".
        updated_at (int): The Unix timestamp when the status was last updated.
        code_entered (Optional[str]): The code entered by the user during verification, if provided.
    """

    status: Literal[
        "code_valid", "code_invalid", "code_max_attempts_exceeded", "expired"
    ]  # The current status of the verification process.
    updated_at: int  # Status last updated Timestamp as an integer (Unix timestamp)
    code_entered: Optional[str]  # Optional. The code entered by the user


@dataclass
class RequestStatus:
    """Represents the status of a verification message request.

    Attributes:
        request_id (str): A unique identifier for the verification request.
        phone_number (str): The phone number in E.164 format.
        request_cost (float): The total cost of the verification request.
        is_refunded (Optional[bool]): If True, the request fee was refunded.
        remaining_balance (Optional[float]): The remaining balance in credits after the request.
        delivery_status (Optional[DeliveryStatus]): The current status of the message delivery.
        verification_status (Optional[VerificationStatus]): The current status of
            the verification process.
        payload (Optional[str]): Custom payload if it was provided in the request (0-256 bytes).
    """

    request_id: str  # Unique id for the verification request
    phone_number: str  # Phone number in E.164 format
    request_cost: float  # Total cost of the request
    is_refunded: Optional[bool]  # Optional. If True, the request fee was refunded.
    remaining_balance: Optional[float]  # Optional. Remaining balance in credits
    delivery_status: Optional[
        DeliveryStatus
    ]  # Optional. The current message delivery status
    verification_status: Optional[
        VerificationStatus
    ]  # Optional. The current status of the verification process
    payload: Optional[
        str
    ]  # Optional. Custom payload if it was provided in the request, 0-256 bytes
