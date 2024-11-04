from httpx import AsyncClient
from typing import Union

from .types import DeliveryStatus, RequestStatus, VerificationStatus
from .exceptions import ApiError, ResponseNotOk


class AsyncTGGateway:
    """
    Telegram Gateway Async API Client
    """

    __slots__ = ("_is_closed", "access_token", "session")

    def __init__(self, access_token: str):
        """
        Telegram Gateway API Client

        Parameters
        ----------
        access_token: str
            An Access token from Telegram Gateway account settings
            https://gateway.telegram.org/account/api
        """
        self._is_closed = False
        self.access_token = access_token
        self.session = AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.close()

    async def _convert_result(self, data: dict) -> RequestStatus:
        """
        Convert raw API response to RequestStatus object

        Parameters
        ----------
        data : dict
            Raw API response

        Returns
        -------
        RequestStatus
            A RequestStatus object containing the parsed data
        """
        ds_data = data.get("delivery_status")
        delivery_status = None
        if ds_data:
            delivery_status = DeliveryStatus(
                status=ds_data["status"], updated_at=ds_data["updated_at"]
            )

        vs_data = data.get("verification_status")
        verification_status = None
        if vs_data:
            verification_status = VerificationStatus(
                status=vs_data["status"],
                updated_at=vs_data["updated_at"],
                code_entered=vs_data.get("code_entered"),
            )

        request_status = None
        request_status = RequestStatus(
            request_id=data["request_id"],
            phone_number=data["phone_number"],
            request_cost=data["request_cost"],
            remaining_balance=data.get("remaining_balance"),
            delivery_status=delivery_status,
            verification_status=verification_status,
            payload=data.get("payload"),
        )

        return request_status

    async def _request(
        self, method: str, values: dict = None
    ) -> Union[RequestStatus, bool]:
        """
        Makes a request to the Telegram Gateway API

        Parameters
        ----------
        method: str
            The API method to call
        values: dict
            The values to send with the request

        Returns
        -------
        Union[RequestStatus, bool]
            The result of the request. Only if the method is 'revokeVerificationMessage' returns True. Otherwise returns a RequestStatus object

        Raises
        ------
        TGGatewayException
            Base class for all Telegram Gateway exceptions
        ApiError
            If the API returns an error
        ResponseNotOk
            If the HTTP response code is not 200
        """
        if self._is_closed:
            raise RuntimeError(
                "Once the client instance has been closed, no more requests can be made."
            )

        values = values.copy() if values is not None else {}
        values["access_token"] = self.access_token

        response = await self.session.post(
            f"https://gatewayapi.telegram.org/{method}", json=values
        )

        if response.status_code >= 400:
            raise ResponseNotOk(response)

        response = response.json()
        if response.get("ok"):
            if method == "revokeVerificationMessage":
                return True
            result = response.get("result", {})
            return await self._convert_result(result)
        else:
            error = response.get("error", "UNKNOWN_ERROR")
            raise ApiError(error)

    async def getAccessToken(self) -> str:
        """
        Get the current access token that is being used

        Returns
        -------
        str
            The current access token
        """
        return self.access_token

    async def sendVerificationMessage(
        self,
        phone_number: str,
        request_id: str = None,
        sender_username: str = None,
        code: str = None,
        code_length: int = None,
        callback_url: str = None,
        payload: str = None,
        ttl: int = None,
    ) -> RequestStatus:
        """
        **Use this method to send a verification message.**

        For more info check: https://core.telegram.org/gateway/api#sendverificationmessage

        Parameters
        ----------
        phone_number: str
            The phone number to which you want to send a verification message, in the E.164 format.
        request_id: str
            The unique identifier of a previous request from checkSendAbility.
            If provided, this request will be free of charge.
        sender_username: str
            Username of the Telegram channel from which the code will be sent.
            The specified channel, if any, must be verified and owned by the same account who owns the Gateway API token.
        code: str
            The verification code.
            Use this parameter if you want to set the verification code yourself.
            Only fully numeric strings between 4 and 8 characters in length are supported.
            If this parameter is set, code_length is ignored.
        code_length: int
            The length of the verification code if Telegram needs to generate it for you.
            Supported values are from 4 to 8.
            This is only relevant if you are not using the code parameter to set your own code.
            Use the checkVerificationStatus method with the code parameter to verify the code entered by the user.
        callback_url: str
            An HTTPS URL where you want to receive delivery reports related to the sent message, 0-256 bytes.
        payload: str
            Custom payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
        ttl: int
            Time-to-live (in seconds) before the message expires and is deleted.
            he message will not be deleted if it has already been read.
            If not specified, the message will not be deleted.
            Supported values are from 60 to 86400.

        Returns
        -------
        RequestStatus
            A RequestStatus object containing the result of the request
        """
        values = {
            "phone_number": phone_number,
            "request_id": request_id,
            "sender_username": sender_username,
            "code": code,
            "code_length": code_length,
            "callback_url": callback_url,
            "payload": payload,
            "ttl": ttl,
        }
        result = await self._request("sendVerificationMessage", values)
        return result

    async def checkSendAbility(self, phone_number: str) -> RequestStatus:
        """
        Use this method to optionally check the ability to send a verification message to the specified phone number.
        For more info check: https://core.telegram.org/gateway/api#checksendability

        Parameters
        ----------
        phone_number: str
            The phone number to which you want to send a verification message, in the E.164 format.

        Returns
        -------
        RequestStatus
            A RequestStatus object containing the result of the request
        """
        values = {"phone_number": phone_number}
        result = await self._request("checkSendAbility", values)
        return result

    async def checkVerificationStatus(
        self, request_id: str, code: str = None
    ) -> RequestStatus:
        """
        Use this method to check the status of a verification message that was sent previously.
        For more info check: https://core.telegram.org/gateway/api#checkverificationstatus

        Parameters
        ----------
        request_id: str
            The unique identifier of the verification request whose status you want to check.
        code: str
            The code entered by the user.
            If provided, the method checks if the code is valid for the relevant request.

        Returns
        -------
        RequestStatus
            A RequestStatus object containing the result of the request
        """
        values = {
            "request_id": request_id,
            "code": code,
        }
        result = await self._request("checkVerificationStatus", values)
        return result

    async def revokeVerificationMessage(
        self,
        request_id: str,
    ) -> bool:
        """
        Use this method to revoke a verification message that was sent previously.
        For more info check: https://core.telegram.org/gateway/api#revokeverificationmessage

        Parameters
        ----------
        request_id: str
            The unique identifier of the request whose verification message you want to revoke.

        Returns
        -------
        bool
            Returns True if the revocation request was received by server.
        """
        values = {"request_id": request_id}
        result = await self._request("revokeVerificationMessage", values)
        return result

    async def close(self):
        """
        Close the client instance.
        After calling this method, the client instance will no longer be usable and any attempts to make requests will raise an exception.
        """
        if not self._is_closed:
            self._is_closed = True
            self.access_token = None
            await self.session.close()
