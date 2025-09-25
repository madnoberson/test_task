__all__ = ("verify_api_key",)

from typing import Annotated

from fastapi import HTTPException, Depends, Query

from test_task.configs import ClientAccessConfig
from .stub import Stub


_ClientAccessConfig = Annotated[
    ClientAccessConfig,
    Depends(Stub(ClientAccessConfig)),
]


def verify_api_key(
    *,
    api_key: Annotated[str, Query()],
    client_access_config: _ClientAccessConfig,
) -> None:
    if api_key != client_access_config.api_key:
        raise HTTPException(401, "Invalid API key.")
    
