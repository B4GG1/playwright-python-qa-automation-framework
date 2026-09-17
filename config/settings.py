import os
from dataclasses import dataclass
from typing import Callable, TypeVar
from urllib.parse import urlsplit

DEFAULT_BASE_URL = "https://www.saucedemo.com"
BASE_URL_ENV_VAR = "QA_BASE_URL"

T = TypeVar("T")


def _read_env(
    name: str,
    default: T,
    parser: Callable[[str], T],
) -> T:
    raw_value = os.environ.get(name)

    if raw_value is None:
        return default

    try:
        return parser(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid value for environment variable {name}: {raw_value!r}. {exc}"
        ) from exc


def _parse_base_url(value: str) -> str:
    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError("Base URL cannot be empty.")

    if any(character.isspace() for character in normalized_value):
        raise ValueError("Base URL cannot contain whitespace.")

    parsed_url = urlsplit(normalized_value)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Base URL must use the http or https scheme.")

    if not parsed_url.hostname:
        raise ValueError("Base URL must contain a valid host.")

    if parsed_url.username is not None or parsed_url.password is not None:
        raise ValueError("Base URL must not contain credentials.")

    try:
        _ = parsed_url.port
    except ValueError as exc:
        raise ValueError("Base URL contains an invalid port.") from exc

    if parsed_url.path not in {"", "/"}:
        raise ValueError("Base URL must contain only the application origin, without a path.")

    if parsed_url.query:
        raise ValueError("Base URL must not contain query parameters.")

    if parsed_url.fragment:
        raise ValueError("Base URL must not contain a fragment.")

    return normalized_value.rstrip("/")


@dataclass(frozen=True, slots=True)
class Settings:
    base_url: str


def load_settings() -> Settings:
    return Settings(
        base_url=_read_env(
            BASE_URL_ENV_VAR,
            DEFAULT_BASE_URL,
            _parse_base_url,
        )
    )


settings = load_settings()
