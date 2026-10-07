import logging

import pytest

from framework.diagnostics import (
    DIAGNOSTICS_LOGGER_NAME,
    format_diagnostic_error,
    format_failure_summary,
    format_runtime_summary,
    log_diagnostic_error,
)


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


def test_failure_summary_contains_available_diagnostic_context() -> None:
    summary = format_failure_summary(
        node_id="tests/test_example.py::test_example[chromium]",
        phase="call",
        page_url="https://example.com/inventory.html",
        screenshot_path="reports/screenshots/test_example.png",
    )

    assert summary == (
        "[failure] "
        "test=tests/test_example.py::test_example[chromium] | "
        "phase=call | "
        "url=https://example.com/inventory.html | "
        "screenshot=reports/screenshots/test_example.png"
    )


def test_failure_summary_omits_unavailable_optional_context() -> None:
    summary = format_failure_summary(
        node_id="tests/test_example.py::test_example",
        phase="setup",
    )

    assert summary == ("[failure] " "test=tests/test_example.py::test_example | " "phase=setup")


def test_diagnostic_error_contains_operation_and_failure_context() -> None:
    error = RuntimeError("screenshot failed")

    message = format_diagnostic_error(
        operation="screenshot",
        node_id="tests/test_example.py::test_example",
        phase="call",
        error=error,
    )

    assert message == (
        "[diagnostic-error] "
        "operation=screenshot | "
        "test=tests/test_example.py::test_example | "
        "phase=call | "
        "error=screenshot failed"
    )


def test_diagnostic_error_is_emitted_through_project_logger(
    caplog: pytest.LogCaptureFixture,
) -> None:
    error = RuntimeError("attachment failed")

    with caplog.at_level(logging.ERROR, logger=DIAGNOSTICS_LOGGER_NAME):
        message = log_diagnostic_error(
            operation="allure-attachment",
            node_id="tests/test_example.py::test_example",
            phase="call",
            error=error,
        )

    assert message in caplog.messages
