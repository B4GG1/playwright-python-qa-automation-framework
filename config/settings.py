import os
from dataclasses import dataclass
from typing import Callable, TypeVar
from urllib.parse import urlsplit

DEFAULT_BASE_URL = "https://www.saucedemo.com"
DEFAULT_BROWSER = "chromium"
DEFAULT_HEADED = False
DEFAULT_TIMEOUT_MS = 30000
DEFAULT_EXPECT_TIMEOUT_MS = 5000

BASE_URL_ENV_VAR = "QA_BASE_URL"
BROWSER_ENV_VAR = "QA_BROWSER"
HEADED_ENV_VAR = "QA_HEADED"
TIMEOUT_MS_ENV_VAR = "QA_TIMEOUT_MS"
EXPECT_TIMEOUT_MS_ENV_VAR = "QA_EXPECT_TIMEOUT_MS"

SUPPORTED_BROWSERS = {"chromium", "firefox", "webkit"}

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


def _parse_browser(value: str) -> str:
    normalized_value = value.strip().lower()

    if normalized_value not in SUPPORTED_BROWSERS:
        supported_values = ", ".join(sorted(SUPPORTED_BROWSERS))
        raise ValueError(f"Browser must be one of: {supported_values}.")

    return normalized_value


def _parse_bool(value: str) -> bool:
    normalized_value = value.strip().lower()

    true_values = {"true", "1", "yes", "on"}
    false_values = {"false", "0", "no", "off"}

    if normalized_value in true_values:
        return True

    if normalized_value in false_values:
        return False

    raise ValueError("Boolean value must be one of: " "true, false, 1, 0, yes, no, on, off.")


def _parse_timeout_ms(value: str) -> int:
    normalized_value = value.strip()

    try:
        timeout_ms = int(normalized_value)
    except ValueError as exc:
        raise ValueError("Timeout must be an integer number of milliseconds.") from exc

    if timeout_ms < 0:
        raise ValueError("Timeout cannot be negative.")

    return timeout_ms


@dataclass(frozen=True, slots=True)
class Settings:
    base_url: str
    browser: str
    headed: bool
    timeout_ms: int
    expect_timeout_ms: int


def load_settings() -> Settings:
    return Settings(
        base_url=_read_env(
            BASE_URL_ENV_VAR,
            DEFAULT_BASE_URL,
            _parse_base_url,
        ),
        browser=_read_env(
            BROWSER_ENV_VAR,
            DEFAULT_BROWSER,
            _parse_browser,
        ),
        headed=_read_env(
            HEADED_ENV_VAR,
            DEFAULT_HEADED,
            _parse_bool,
        ),
        timeout_ms=_read_env(
            TIMEOUT_MS_ENV_VAR,
            DEFAULT_TIMEOUT_MS,
            _parse_timeout_ms,
        ),
        expect_timeout_ms=_read_env(
            EXPECT_TIMEOUT_MS_ENV_VAR,
            DEFAULT_EXPECT_TIMEOUT_MS,
            _parse_timeout_ms,
        ),
    )


settings = load_settings()
