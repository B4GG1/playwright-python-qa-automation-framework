import pytest

from framework.diagnostics import format_runtime_summary


@pytest.mark.parametrize(
    ("headed", "expected_mode"),
    [
        (False, "headless"),
        (True, "headed"),
    ],
)
def test_runtime_summary_contains_effective_configuration(
    headed: bool,
    expected_mode: str,
) -> None:
    summary = format_runtime_summary(
        base_url="https://example.com",
        browser=["chromium"],
        headed=headed,
        timeout_ms=30000,
        expect_timeout_ms=5000,
        screenshot_policy="only-on-failure",
        trace_policy="off",
        video_policy="off",
    )

    assert summary == (
        "[runtime] "
        "base_url=https://example.com | "
        "browser=chromium | "
        f"mode={expected_mode} | "
        "action_navigation_timeout_ms=30000 | "
        "assertion_timeout_ms=5000 | "
        "screenshot=only-on-failure | "
        "trace=off | "
        "video=off"
    )


def test_runtime_summary_supports_multiple_native_browser_values() -> None:
    summary = format_runtime_summary(
        base_url="https://example.com",
        browser=["chromium", "firefox"],
        headed=False,
        timeout_ms=30000,
        expect_timeout_ms=5000,
        screenshot_policy="only-on-failure",
        trace_policy="off",
        video_policy="off",
    )

    assert "browser=chromium,firefox" in summary
