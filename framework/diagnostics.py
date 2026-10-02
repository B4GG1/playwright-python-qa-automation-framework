from collections.abc import Sequence


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
