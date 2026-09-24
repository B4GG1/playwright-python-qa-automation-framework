import pytest

from config.settings import (
    BASE_URL_ENV_VAR,
    BROWSER_ENV_VAR,
    DEFAULT_BASE_URL,
    DEFAULT_BROWSER,
    DEFAULT_EXPECT_TIMEOUT_MS,
    DEFAULT_HEADED,
    DEFAULT_TIMEOUT_MS,
    EXPECT_TIMEOUT_MS_ENV_VAR,
    HEADED_ENV_VAR,
    TIMEOUT_MS_ENV_VAR,
    load_settings,
)


def test_default_runtime_configuration_is_used_when_environment_variables_are_not_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for env_var in (
        BASE_URL_ENV_VAR,
        BROWSER_ENV_VAR,
        HEADED_ENV_VAR,
        TIMEOUT_MS_ENV_VAR,
        EXPECT_TIMEOUT_MS_ENV_VAR,
    ):
        monkeypatch.delenv(env_var, raising=False)

    settings = load_settings()

    assert settings.base_url == DEFAULT_BASE_URL
    assert settings.browser == DEFAULT_BROWSER
    assert settings.headed is DEFAULT_HEADED
    assert settings.timeout_ms == DEFAULT_TIMEOUT_MS
    assert settings.expect_timeout_ms == DEFAULT_EXPECT_TIMEOUT_MS


@pytest.mark.parametrize(
    ("configured_base_url", "expected_base_url"),
    [
        ("https://example.com", "https://example.com"),
        ("https://example.com/", "https://example.com"),
        ("  https://example.com/  ", "https://example.com"),
        ("http://localhost:8000", "http://localhost:8000"),
    ],
)
def test_explicit_base_url_override_is_loaded_and_normalized(
    monkeypatch: pytest.MonkeyPatch,
    configured_base_url: str,
    expected_base_url: str,
) -> None:
    monkeypatch.setenv(BASE_URL_ENV_VAR, configured_base_url)

    settings = load_settings()

    assert settings.base_url == expected_base_url


@pytest.mark.parametrize(
    "invalid_base_url",
    [
        "",
        "   ",
        "example.com",
        "ftp://example.com",
        "https://",
        "https://example.com/path",
        "https://example.com?query=value",
        "https://example.com#fragment",
        "https://user:password@example.com",
        "https://example.com:invalid",
    ],
)
def test_invalid_explicit_base_url_raises_clear_configuration_error(
    monkeypatch: pytest.MonkeyPatch,
    invalid_base_url: str,
) -> None:
    monkeypatch.setenv(BASE_URL_ENV_VAR, invalid_base_url)

    with pytest.raises(
        ValueError,
        match=rf"Invalid value for environment variable {BASE_URL_ENV_VAR}",
    ):
        load_settings()


@pytest.mark.parametrize(
    ("configured_browser", "expected_browser"),
    [
        ("chromium", "chromium"),
        ("FIREFOX", "firefox"),
        ("  webkit  ", "webkit"),
    ],
)
def test_browser_override_is_loaded_and_normalized(
    monkeypatch: pytest.MonkeyPatch,
    configured_browser: str,
    expected_browser: str,
) -> None:
    monkeypatch.setenv(BROWSER_ENV_VAR, configured_browser)

    settings = load_settings()

    assert settings.browser == expected_browser


@pytest.mark.parametrize(
    "invalid_browser",
    [
        "",
        "chrome",
        "edge",
        "safari",
    ],
)
def test_invalid_browser_raises_clear_configuration_error(
    monkeypatch: pytest.MonkeyPatch,
    invalid_browser: str,
) -> None:
    monkeypatch.setenv(BROWSER_ENV_VAR, invalid_browser)

    with pytest.raises(
        ValueError,
        match=rf"Invalid value for environment variable {BROWSER_ENV_VAR}",
    ):
        load_settings()


@pytest.mark.parametrize(
    ("configured_headed", "expected_headed"),
    [
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("yes", True),
        ("on", True),
        ("false", False),
        ("FALSE", False),
        ("0", False),
        ("no", False),
        ("off", False),
    ],
)
def test_headed_override_is_parsed_predictably(
    monkeypatch: pytest.MonkeyPatch,
    configured_headed: str,
    expected_headed: bool,
) -> None:
    monkeypatch.setenv(HEADED_ENV_VAR, configured_headed)

    settings = load_settings()

    assert settings.headed is expected_headed


@pytest.mark.parametrize(
    "invalid_headed",
    [
        "",
        "enabled",
        "disabled",
        "2",
    ],
)
def test_invalid_headed_value_raises_clear_configuration_error(
    monkeypatch: pytest.MonkeyPatch,
    invalid_headed: str,
) -> None:
    monkeypatch.setenv(HEADED_ENV_VAR, invalid_headed)

    with pytest.raises(
        ValueError,
        match=rf"Invalid value for environment variable {HEADED_ENV_VAR}",
    ):
        load_settings()


@pytest.mark.parametrize(
    ("env_var", "setting_name"),
    [
        (TIMEOUT_MS_ENV_VAR, "timeout_ms"),
        (EXPECT_TIMEOUT_MS_ENV_VAR, "expect_timeout_ms"),
    ],
)
@pytest.mark.parametrize(
    ("configured_timeout", "expected_timeout"),
    [
        ("0", 0),
        ("1", 1),
        ("15000", 15000),
        (" 45000 ", 45000),
    ],
)
def test_timeout_override_is_parsed_as_non_negative_integer(
    monkeypatch: pytest.MonkeyPatch,
    env_var: str,
    setting_name: str,
    configured_timeout: str,
    expected_timeout: int,
) -> None:
    monkeypatch.setenv(env_var, configured_timeout)

    settings = load_settings()

    assert getattr(settings, setting_name) == expected_timeout


@pytest.mark.parametrize(
    "env_var",
    [
        TIMEOUT_MS_ENV_VAR,
        EXPECT_TIMEOUT_MS_ENV_VAR,
    ],
)
@pytest.mark.parametrize(
    "invalid_timeout",
    [
        "",
        "-1",
        "1.5",
        "invalid",
    ],
)
def test_invalid_timeout_raises_clear_configuration_error(
    monkeypatch: pytest.MonkeyPatch,
    env_var: str,
    invalid_timeout: str,
) -> None:
    monkeypatch.setenv(env_var, invalid_timeout)

    with pytest.raises(
        ValueError,
        match=rf"Invalid value for environment variable {env_var}",
    ):
        load_settings()
