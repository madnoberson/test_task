__all__ = ("ClientAccessConfig", "load_client_access_config")

from dataclasses import dataclass

from .env_var_getter import get_env_var


@dataclass
class ClientAccessConfig:
    api_key: str


def load_client_access_config() -> ClientAccessConfig:
    return ClientAccessConfig(api_key=get_env_var("API_KEY", default="123"))