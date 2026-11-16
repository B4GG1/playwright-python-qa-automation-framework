import logging
from collections.abc import Sequence

DIAGNOSTICS_LOGGER_NAME = "qa_automation.diagnostics"

logger = logging.getLogger(DIAGNOSTICS_LOGGER_NAME)


def format_runtime_summary(
    *,
    base_url: str,
    browser: str | Sequence[str],
    headed: bool,
    timeout_ms: int,
    expect_timeout_ms: int,
    screenshot_policy: str,
    trace_policy: str,
    video_policy: str,
) -> str:
    if isinstance(browser, str):
        browser_value = browser
    else:
        browser_value = ",".join(browser)

    mode = "headed" if headed else "headless"

    fields = (
        f"base_url={base_url}",
        f"browser={browser_value}",
        f"mode={mode}",
        f"action_navigation_timeout_ms={timeout_ms}",
        f"assertion_timeout_ms={expect_timeout_ms}",
        f"screenshot={screenshot_policy}",
        f"trace={trace_policy}",
        f"video={video_policy}",
    )

    return "[runtime] " + " | ".join(fields)


def format_failure_summary(
    *,
    node_id: str,
    phase: str,
    page_url: str | None = None,
    screenshot_path: str | None = None,
) -> str:
    fields = [
        f"test={node_id}",
        f"phase={phase}",
    ]

    if page_url is not None:
        fields.append(f"url={page_url}")

    if screenshot_path is not None:
        fields.append(f"screenshot={screenshot_path}")

    return "[failure] " + " | ".join(fields)


def format_diagnostic_error(
    *,
    operation: str,
    node_id: str,
    phase: str,
    error: Exception,
) -> str:
    return (
        "[diagnostic-error] "
        f"operation={operation} | "
        f"test={node_id} | "
        f"phase={phase} | "
        f"error={error}"
    )


def log_diagnostic_error(
    *,
    operation: str,
    node_id: str,
    phase: str,
    error: Exception,
) -> str:
    message = format_diagnostic_error(
        operation=operation,
        node_id=node_id,
        phase=phase,
        error=error,
    )

    logger.error(message)

    return message
