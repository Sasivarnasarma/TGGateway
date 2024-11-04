from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class DeliveryStatus:
    status: Literal[
        "sent", "read", "revoked"
    ]  # The current status of the message.
    updated_at: (
        int  # Status last updated Timestamp as an integer (Unix timestamp)
    )


@dataclass
class VerificationStatus:
    status: Literal[
        "code_valid", "code_invalid", "code_max_attempts_exceeded", "expired"
    ]  # The current status of the verification process
    updated_at: (
        int  # Status last updated Timestamp as an integer (Unix timestamp)
    )
    code_entered: Optional[str]  # Optional. The code entered by the user


@dataclass
class RequestStatus:
    # This object represents the status of a verification message request.
    request_id: str  # Unique identifier for the verification request
    phone_number: str  # Phone number in E.164 format
    request_cost: float  # Total cost of the request
    remaining_balance: Optional[
        float
    ]  # Optional. Remaining balance in credits
    delivery_status: Optional[
        DeliveryStatus
    ]  # Optional. The current message delivery status
    verification_status: Optional[
        VerificationStatus
    ]  # Optional. The current status of the verification process
    payload: Optional[
        str
    ]  # Optional. Custom payload if it was provided in the request, 0-256 bytes
