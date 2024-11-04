from httpx import Response


class TGGatewayException(Exception):
    pass


class ApiError(TGGatewayException):
    pass


class ResponseNotOk(TGGatewayException):
    def __init__(self, response: Response):
        self.response = response
        super().__init__(
            f"The response is not OK. Status Code:- {response.status_code}"
        )
