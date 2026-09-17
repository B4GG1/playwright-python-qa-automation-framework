import pytest

from config.settings import BASE_URL_ENV_VAR, DEFAULT_BASE_URL, load_settings


def test_default_base_url_is_used_when_environment_variable_is_not_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(BASE_URL_ENV_VAR, raising=False)

    settings = load_settings()

    assert settings.base_url == DEFAULT_BASE_URL


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
