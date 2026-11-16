import os
from datetime import UTC, datetime
from typing import Callable

import allure
import pytest
from playwright.sync_api import BrowserContext, expect

from config.settings import settings
from framework.diagnostics import (
    format_failure_summary,
    format_runtime_summary,
    log_diagnostic_error,
)


def _cli_option_was_provided(config: pytest.Config, option: str) -> bool:
    invocation_params = config.invocation_params

    if invocation_params is None:
        return False

    option_with_value = f"{option}="

    return any(
        argument == option or argument.startswith(option_with_value)
        for argument in invocation_params.args
    )


def pytest_configure(config: pytest.Config) -> None:
    if not config.getoption("--browser"):
        config.option.browser = [settings.browser]

    if settings.headed and not config.getoption("--headed"):
        config.option.headed = True

    if not _cli_option_was_provided(config, "--tracing"):
        config.option.tracing = settings.trace_policy

    if not _cli_option_was_provided(config, "--video"):
        config.option.video = settings.video_policy

    expect.set_options(timeout=settings.expect_timeout_ms)


def pytest_report_header(config: pytest.Config) -> str | None:
    if hasattr(config, "workerinput"):
        return None

    return format_runtime_summary(
        base_url=settings.base_url,
        browser=config.getoption("--browser"),
        headed=config.getoption("--headed"),
        timeout_ms=settings.timeout_ms,
        expect_timeout_ms=settings.expect_timeout_ms,
        screenshot_policy=settings.screenshot_policy,
        trace_policy=config.getoption("--tracing"),
        video_policy=config.getoption("--video"),
    )


@pytest.fixture()
def context(
    new_context: Callable[..., BrowserContext],
) -> BrowserContext:
    browser_context = new_context()
    browser_context.set_default_timeout(settings.timeout_ms)
    browser_context.set_default_navigation_timeout(settings.timeout_ms)
    return browser_context


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    _ = call

    outcome = yield
    report = outcome.get_result()

    if not report.failed:
        return

    node_id = item.nodeid
    phase = report.when
    page = item.funcargs.get("page")

    page_url = None
    screenshot_path = None

    if page is not None:
        try:
            page_url = page.url
        except Exception as e:
            message = log_diagnostic_error(
                operation="page-url",
                node_id=node_id,
                phase=phase,
                error=e,
            )
            report.sections.append(("failure diagnostics", message))

    if phase == "call" and settings.screenshot_policy != "off" and page is not None:
        reports_dir = os.path.join("reports", "screenshots")
        os.makedirs(reports_dir, exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        test_name = item.name.replace("/", "_").replace("::", "_")

        file_path = os.path.join(
            reports_dir,
            f"{test_name}_{timestamp}.png",
        )

        try:
            page.screenshot(path=file_path, full_page=True)
        except Exception as e:
            message = log_diagnostic_error(
                operation="screenshot",
                node_id=node_id,
                phase=phase,
                error=e,
            )
            report.sections.append(("failure diagnostics", message))
        else:
            screenshot_path = file_path

            try:
                allure.attach.file(
                    file_path,
                    name="Failure screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                message = log_diagnostic_error(
                    operation="allure-attachment",
                    node_id=node_id,
                    phase=phase,
                    error=e,
                )
                report.sections.append(("failure diagnostics", message))

    summary = format_failure_summary(
        node_id=node_id,
        phase=phase,
        page_url=page_url,
        screenshot_path=screenshot_path,
    )

    report.sections.append(("failure diagnostics", summary))
