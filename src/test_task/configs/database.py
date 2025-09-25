__all__ = ("PostgresConfig", "load_postgres_config")

from dataclasses import dataclass

from .env_var_getter import get_env_var


@dataclass
class PostgresConfig:
    username: str
    password: str
    host: str
    port: int
    database: str


def load_postgres_config() -> PostgresConfig:
    return PostgresConfig(
        username=get_env_var("POSTGRES_USERNAME", default="postgres"),
        password=get_env_var("POSTGRES_PASSWORD", default="1234"),
        host=get_env_var("POSTGRES_HOST", default="localhost"),
        port=get_env_var("POSTGRES_PORT", default=5432, value_factory=int),
        database=get_env_var("POSTGRES_DATABASE", default="test_task"),
    )