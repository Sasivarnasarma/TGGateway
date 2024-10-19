
# TGGateway - Python Telegram Gateway API Wrapper

**TGGateway** is a Python library that provides both *synchronous* and asynchronous API clients for interacting with the [**Telegram Gateway API**](https://core.telegram.org/gateway).
This wrapper simplifies the process of sending verification messages, checking their status, and handling delivery reports.

## Features
- The one and only requirement is `httpx`.
-   Synchronous API client (`TGGateway`) using `httpx.Client`.
-   Asynchronous API client (`AsyncTGGateway`) using `httpx.AsyncClient`.
-   Handles API requests and responses, including:
    -   Sending verification messages
    -   Checking the status of sent messages
    -   Checking delivery status and revoking verification messages
-   Custom exception handling for API errors.

## Installation
You can install the package via `pip`:
```bash
python3 -m  pip  install  PyTGGateway
```

## Usage
 It is recommended to use `TGGateway` as a **context manager**. By doing this, you can make sure that connections are correctly cleaned up when leaving the `with` block. However, you also have the option to use `.close()` to explicitly close the connection.
 
 Get `access_token` from [**Telegram Gateway Account**](https://gateway.telegram.org/account/api).
 
**Sync Example**

 *As context manager*
```python
from TGGateway import TGGateway

def main():
    with TGGateway('access_token') as gateway:
        try:
            result = gateway.sendVerificationMessage(
                phone_number = '+1234567890',
                code = '0527'
            )
            print(result.request_id)
            print(result.request_cost)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
```

 *As .close()*
```python
from TGGateway import TGGateway

def main():
    try:
        gateway = TGGateway('access_token')
        result = gateway.sendVerificationMessage(
            phone_number = '+1234567890',
            code = '0527'
        )
        print(result.request_id)
        print(result.request_cost)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        gateway.close()

if __name__ == '__main__':
    main()
```

**Async Example**

 *As context manager*
```python
import asyncio
from TGGateway import AsyncTGGateway

async def main():
    async with AsyncTGGateway('access_token') as gateway:
        try:
            result = await gateway.sendVerificationMessage(
                phone_number = '+1234567890',
                code = '0527'
            )
            print(result.request_id)
            print(result.request_cost)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
```

 *As .close()*
```python
import asyncio
from TGGateway import AsyncTGGateway

async def main():
    try:
        gateway = AsyncTGGateway('access_token')
        result = await gateway.sendVerificationMessage(
            phone_number = '+1234567890',
            code = '0527'
        )
        print(result.request_id)
        print(result.request_cost)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await gateway.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## API Reference
 For detailed API references, check the [**Official API Documentation**](https://core.telegram.org/gateway/api).
### `TGGateway`

#### Methods:

-   `getAccessToken() -> str`  
    Get the current access token that is being used.

-   `sendVerificationMessage(phone_number: str, request_id: str, ...) -> RequestStatus`  
    Sends a verification message to a phone number.

-   `checkSendAbility(phone_number: str) -> RequestStatus`  
    Checks if a phone number can receive a verification message.

-   `checkVerificationStatus(request_id: str, code: str = None) -> RequestStatus`  
    Checks the status of the verification process.

-   `revokeVerificationMessage(request_id: str) -> bool`  
    Revokes a verification message.   

#### Exception:

-   `TGGatewayException`  
    Base class for all Telegram Gateway exceptions.

-   `ApiError`  
    Raised when the API returns an error.

-   `ResponseNotOk`  
    Raised when the response from the API is not successful (status code not 2xx).

### `AsyncTGGateway`

The asynchronous version of the `TGGateway` class supports the same methods as its synchronous counterpart, but all methods must be awaited.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request with your improvements.

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

### With ❤️ Made By @Sasivarnasarma
