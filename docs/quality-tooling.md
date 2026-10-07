# Quality Tooling

This document describes the code quality, validation, execution, runtime configuration, reporting, and diagnostic tooling used in the QA automation framework.

The goal of quality tooling is to keep the codebase readable, consistent, maintainable, observable, reproducible, and safe to extend as the framework grows.

The tooling described here supports:

* local development
* static code-quality validation
* selective test execution
* sequential and parallel Pytest execution
* centralized runtime configuration
* lightweight runtime diagnostics
* failed-test diagnostics
* reporting
* Pull Request validation
* CI quality gates
* stable portfolio promotion

The current implementation combines the Phase 4B CI execution strategy, Phase 4C parallel execution strategy, Phase 4D reporting strategy, Phase 4E runtime configuration strategy, and Phase 4F diagnostics and fixture-responsibility cleanup.

## Tooling Overview

The project currently uses:

* Ruff for linting and static checks
* Black for Python formatting
* isort for import sorting
* pre-commit for local quality validation
* Pytest as the automated test runner
* pytest-playwright for Playwright/Pytest integration
* pytest-xdist for worker-level parallel execution
* Playwright assertions for browser and UI validation
* centralized runtime configuration through `config/settings.py`
* lightweight diagnostic formatting through `framework/diagnostics.py`
* Pytest hooks for runtime and failed-test diagnostics
* pytest-html for lightweight HTML reporting
* allure-pytest for Allure result collection
* Allure CLI for Allure HTML generation
* configurable failure screenshots
* configurable Playwright trace generation
* configurable Playwright video generation
* GitHub Actions for CI execution
* GitHub Actions artifacts for temporary CI report and runtime-output retention

These tools support both local development and CI validation.

Phase 4F diagnostics use Python's standard `logging` module.

No additional logging dependency or persistent logging subsystem is introduced.

## Ruff

Ruff is used for fast Python linting and static code analysis.

Current responsibilities:

* detecting common Python issues
* enforcing selected linting rules
* validating import-related rules
* supporting consistent code quality across the project

Run Ruff locally:

```bash
ruff check .
```

Ruff configuration is stored in:

```text
pyproject.toml
```

Current Ruff configuration:

```toml
[tool.ruff]
line-length = 200
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I"]

[tool.ruff.lint.isort]
known-first-party = ["config", "framework", "pages", "test_data", "tests"]
```

The `config` and `framework` packages are treated as first-party project code.

Phase 4F does not require additional Ruff-specific rules.

## Black

Black is used as the primary Python formatter.

It enforces consistent formatting across Python project files.

Check formatting without modifying files:

```bash
black --check .
```

Format files locally:

```bash
black .
```

Black configuration is stored in:

```text
pyproject.toml
```

Current configuration:

```toml
[tool.black]
line-length = 100
target-version = ['py312']
```

## isort

isort is used to organize Python imports.

The project uses Black-compatible isort configuration.

Check import sorting:

```bash
isort . --check-only
```

Apply import sorting:

```bash
isort .
```

Configuration:

```text
pyproject.toml
```

Current configuration:

```toml
[tool.isort]
profile = "black"
line_length = 100
```

## pre-commit

pre-commit runs configured quality checks before a commit is created.

Current hooks include:

* Ruff
* Black
* isort

Install hooks:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

Current hook sources include:

* `astral-sh/ruff-pre-commit`
* `psf/black`
* `pycqa/isort`

The purpose of pre-commit is to catch formatting, linting, and import-order problems before changes are committed.

Phase 4F does not introduce another pre-commit tool.

## Pytest

Pytest is the main automated test runner.

Current responsibilities include:

* executing Playwright UI tests
* executing focused framework configuration tests
* supporting fixtures
* supporting parametrization
* supporting marker-based categorization
* supporting selective execution
* supporting sequential execution
* supporting pytest-xdist parallel execution
* integrating with pytest-playwright
* integrating with pytest-html
* integrating with allure-pytest
* providing framework hooks used by runtime diagnostics
* providing failed-test reports used by Phase 4F diagnostics
* producing results used by local and CI validation

Run the complete suite sequentially:

```bash
pytest -v
```

Run the complete suite in parallel:

```bash
pytest -n auto -v
```

Sequential execution remains supported.

Parallel execution is an additional validated execution mode rather than a replacement for the sequential baseline.

## Pytest Responsibility Boundary

Phase 4F separates framework-level Pytest integration from application scenario setup.

Framework-level integration remains in:

```text
conftest.py
```

Application scenario fixtures are located in:

```text
tests/conftest.py
```

The root `conftest.py` owns:

* runtime configuration integration
* effective runtime header
* Playwright BrowserContext timeout configuration
* failed-test diagnostic handling
* custom failure screenshot integration
* Allure failure screenshot integration

`tests/conftest.py` owns scenario-oriented fixtures such as:

```text
opened_login_page
standard_user
logged_in_inventory_page
inventory_page_with_one_product_in_cart
cart_page_with_one_product
checkout_step_one_page_with_one_product
checkout_step_two_page_with_one_product
checkout_last_step_page_with_one_product
```

This separation is a responsibility cleanup rather than a fixture-system redesign.

Phase 4F does not introduce:

* generic fixture factories
* dependency-injection infrastructure
* autouse redesign
* multi-layer fixture packages
* fixture scope redesign

Existing fixture names remain explicit and scenario-oriented.

## pytest-playwright

pytest-playwright provides the Pytest integration layer used by the framework for Playwright browser execution.

Current responsibilities include:

* browser lifecycle management
* browser selection
* `new_context`
* `context`
* `page`
* headed execution support
* native trace handling
* native video handling
* native runtime command-line options

The project does not manually start and own Playwright browser processes.

Phase 4E integrates project runtime configuration with the existing pytest-playwright model instead of replacing it.

Phase 4F preserves this ownership model.

The framework-level integration occurs primarily through:

```text
conftest.py
```

Current runtime integration includes:

* configured browser selection
* configured headed execution
* configured action timeout
* configured navigation timeout
* configured Playwright assertion timeout
* configured trace policy
* configured video policy
* preservation of explicit native pytest-playwright runtime options where applicable
* runtime diagnostic summary of effective values

Trace and video lifecycle remains owned by pytest-playwright.

Phase 4F does not introduce custom trace or video recording logic.

## pytest-xdist

pytest-xdist provides worker-level parallel execution.

Current implemented usage includes:

* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* local parallel validation
* parallel execution inside GitHub Actions browser-test jobs
* compatibility with pytest-html
* compatibility with Allure result collection
* compatibility with configurable failure screenshots
* compatibility with Phase 4E runtime configuration
* compatibility with Phase 4F runtime diagnostics
* compatibility with Phase 4F failed-test diagnostics
* compatibility with separated framework and scenario fixture responsibilities

Approved commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

`-n auto` allows pytest-xdist to determine the worker count according to the available environment.

The current test suite uses worker-safe execution based on test independence.

Validated areas include:

* Playwright fixture isolation
* browser-state independence
* Cart setup
* Checkout setup
* logout and re-login persistence
* E2E checkpoint independence
* parametrized scenario independence
* failure screenshot behavior
* report output behavior
* runtime configuration
* Phase 4F fixture responsibility separation
* runtime diagnostic header behavior
* failed-test diagnostic context

No sequential-only test, diagnostic, or reporting exceptions are required.

### Runtime Header Under pytest-xdist

The effective runtime summary is emitted through:

```text
pytest_report_header
```

The Phase 4F hook suppresses the header when execution occurs inside an xdist worker.

This prevents one runtime summary from being printed by each worker.

The controlling Pytest process therefore provides the execution-level runtime summary.

Failed-test diagnostics remain associated with the corresponding failed Pytest reports.

## Current Executable Markers

Current registered pytest markers are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Marker definitions are stored in:

```text
pytest.ini
```

The project uses:

```text
--strict-markers
```

Every executable marker used by automated tests must therefore be registered.

Detailed semantics are documented in:

```text
docs/testing-strategy.md
```

Runtime configuration, diagnostics, and reporting do not change marker semantics.

## Marker-Based Test Execution

Run Smoke sequentially:

```bash
pytest -m smoke -v
```

Run Smoke in parallel:

```bash
pytest -m smoke -n auto -v
```

Run Regression sequentially:

```bash
pytest -m regression -v
```

Run Regression in parallel:

```bash
pytest -m regression -n auto -v
```

Run UI:

```bash
pytest -m ui -v
```

Run Security:

```bash
pytest -m security -v
```

Run Sorting:

```bash
pytest -m sorting -v
```

Run Navigation:

```bash
pytest -m navigation -v
```

Run the primary E2E checkpoint suite:

```bash
pytest -m e2e -v
```

Markers describe different dimensions of test intent and may be combined.

Examples:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker execution may also be scoped to a module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

Parallel execution changes how collected tests are distributed between workers.

It does not change marker semantics.

Runtime configuration changes execution settings.

It does not change marker semantics.

Diagnostics add runtime and failure context.

They do not change marker semantics.

Reporting consumes execution results.

It also does not change marker semantics.

## Smoke And Regression

Smoke tests provide fast representative validation of critical behavior.

Regression tests provide broader or deeper validation across expanded applicable cases.

Smoke and Regression are not automatically assigned together.

Representative coverage should normally use Smoke.

Expanded or all-cases coverage should normally use Regression.

Both suites have dedicated GitHub Actions jobs.

Both dedicated jobs use pytest-xdist.

Both remain focused on pytest-html reporting.

Phase 4F diagnostics run through their normal Pytest execution path without requiring separate Smoke or Regression implementations.

## UI

The `ui` marker is used when visibility, presentation, state, or direct UI behavior is materially validated.

A Playwright test does not automatically require the `ui` marker.

UI does not currently have a dedicated CI job.

## Security

The `security` marker covers authentication access control and protected-route validation.

Current Security coverage includes unauthenticated access attempts to:

* Inventory
* Cart
* Product Details
* Checkout Information
* Checkout Overview
* Checkout Complete

Security does not currently have a dedicated CI job.

## Sorting

The `sorting` marker identifies product sorting behavior.

Current coverage includes:

* product name A to Z
* product name Z to A
* product price low to high
* product price high to low

Sorting does not currently have a dedicated CI job.

## Navigation

The `navigation` marker identifies meaningful page transitions.

The authentication Login → Inventory transition is intentionally excluded.

Navigation may be combined with Smoke or Regression depending on whether the scenario is representative or expanded.

Navigation does not currently have a dedicated CI job.

## End-to-End

The `e2e` marker identifies independent checkpoints that collectively form the primary purchase journey.

The E2E suite does not rely on:

* shared state between tests
* execution order
* one monolithic browser journey

Each checkpoint prepares its own state through scenario fixtures or test-local setup.

Run:

```bash
pytest -m e2e -v
```

E2E does not currently have a dedicated CI job.

Tests carrying UI, Security, Sorting, Navigation, or E2E markers still participate in complete full-suite CI execution.

Because the full-suite job uses pytest-xdist, those tests may execute on different workers.

Because the full-suite job also collects Allure results, those tests participate in the advanced full-suite report.

Phase 4F fixture separation preserves this independent-checkpoint model.

## Runtime Configuration

Phase 4E provides centralized environment-based runtime configuration through:

```text
config/settings.py
```

The configuration layer provides a controlled way to change execution behavior without editing functional tests or Page Objects.

Current supported environment variables are:

```text
QA_BASE_URL
QA_BROWSER
QA_HEADED
QA_TIMEOUT_MS
QA_EXPECT_TIMEOUT_MS
QA_SCREENSHOT_POLICY
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Current defaults are:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

The settings layer owns:

* default values
* environment-variable reading
* normalization
* validation
* immutable runtime settings consumed by the framework

Phase 4F does not add another runtime configuration layer or additional environment variables.

## Base URL Quality Boundary

`QA_BASE_URL` controls the application origin.

Default:

```text
https://www.saucedemo.com
```

Example:

```bash
QA_BASE_URL="http://localhost:8000" pytest -m smoke -v
```

The configuration validator requires the supplied value to:

* use `http` or `https`
* contain a valid host
* represent the application origin
* not contain credentials
* not contain query parameters
* not contain a fragment
* not contain whitespace
* contain a valid port if a port is provided

A trailing slash is normalized away.

The configured application origin is consumed through `BasePage`.

Page Objects keep their application-relative `ROUTE` definitions.

The effective value is also included in the Phase 4F runtime summary.

## Browser Runtime Quality Boundary

`QA_BROWSER` supports:

```text
chromium
firefox
webkit
```

Default:

```text
chromium
```

Values are normalized before validation.

The runtime configuration layer recognizes the three Playwright browser engines.

This does not mean that every execution environment installs or validates all three.

Current CI remains Chromium-only.

Explicit native pytest-playwright browser options remain supported.

When an explicit native browser selection is supplied, the project configuration does not silently replace it.

The effective Pytest browser selection is included in the Phase 4F runtime summary.

## Headed And Headless Runtime Configuration

`QA_HEADED` controls headed/headless execution.

Default:

```text
false
```

Accepted true values:

```text
true
1
yes
on
```

Accepted false values:

```text
false
0
no
off
```

Values are case-insensitive after normalization.

Headed local example:

```bash
QA_HEADED=true pytest -m smoke -v
```

The native pytest-playwright `--headed` option remains available.

Current CI explicitly uses:

```text
QA_HEADED=false
```

The effective headed/headless mode is included in the Phase 4F runtime summary.

## Timeout Runtime Configuration

### Action And Navigation Timeout

Configured through:

```text
QA_TIMEOUT_MS
```

Default:

```text
30000
```

The value is applied as:

* Playwright default action timeout
* Playwright default navigation timeout

Example:

```bash
QA_TIMEOUT_MS=45000 pytest -m regression -v
```

The effective value is included in the Phase 4F runtime summary.

### Assertion Timeout

Configured through:

```text
QA_EXPECT_TIMEOUT_MS
```

Default:

```text
5000
```

Example:

```bash
QA_EXPECT_TIMEOUT_MS=7000 pytest -m smoke -v
```

Timeout values:

* are expressed in milliseconds
* must be non-negative integers
* may use `0`, following Playwright timeout semantics

The effective assertion timeout is included in the Phase 4F runtime summary.

## Runtime Configuration Validation

Focused configuration behavior is validated through:

```text
tests/test_runtime_config.py
```

The focused configuration suite covers:

* approved defaults
* supported browser values
* browser normalization
* headed boolean parsing
* timeout parsing
* screenshot policy parsing
* trace policy parsing
* video policy parsing
* base URL normalization
* invalid-value handling

Run:

```bash
pytest tests/test_runtime_config.py
```

Invalid explicit configuration fails early.

The framework does not silently replace invalid explicit values with defaults.

Examples of invalid runtime input include:

* unsupported browser values
* unsupported artifact policy values
* invalid boolean values
* negative timeout values
* non-integer timeout values
* malformed application origins

The resulting configuration error identifies the affected environment variable.

## Combined Runtime Overrides

Supported values can be combined for one process.

Example:

```bash
QA_BASE_URL="https://www.saucedemo.com" \
QA_BROWSER="chromium" \
QA_HEADED="false" \
QA_TIMEOUT_MS="45000" \
QA_EXPECT_TIMEOUT_MS="7000" \
QA_SCREENSHOT_POLICY="only-on-failure" \
QA_TRACE_POLICY="retain-on-failure" \
QA_VIDEO_POLICY="off" \
pytest -m smoke -n auto -v
```

The override affects the current execution process.

No functional test or Page Object modification is required.

The effective resulting configuration is visible through the runtime summary.

## Runtime Diagnostic Tooling

Phase 4F introduces lightweight diagnostic support through:

```text
framework/diagnostics.py
```

and framework-level Pytest integration in:

```text
conftest.py
```

The diagnostics implementation uses:

```text
logging
```

from the Python standard library.

It does not introduce an additional third-party logging dependency.

### Runtime Summary Formatting

`framework/diagnostics.py` provides shared runtime summary formatting.

The runtime summary reports:

* application base URL
* effective browser
* headed/headless mode
* action/navigation timeout
* assertion timeout
* screenshot policy
* trace policy
* video policy

Representative format:

```text
[runtime] base_url=... | browser=... | mode=... | action_navigation_timeout_ms=... | assertion_timeout_ms=... | screenshot=... | trace=... | video=...
```

The summary is emitted through:

```text
pytest_report_header
```

The purpose is execution observability rather than persistent logging.

### Failed-Test Summary Formatting

Phase 4F provides failed-test summaries for failed Pytest reports.

Supported failure phases are:

```text
setup
call
teardown
```

Every summary identifies:

* Pytest node ID
* failure phase

When available, it additionally identifies:

* current page URL
* successfully created custom screenshot path

Representative format:

```text
[failure] test=<node-id> | phase=<phase> | url=<current-url> | screenshot=<path>
```

Optional fields are omitted when the corresponding evidence is unavailable.

### Diagnostic Error Formatting And Logging

The diagnostics module also formats errors produced while collecting diagnostic evidence.

Current diagnostic operations include:

```text
page-url
screenshot
allure-attachment
```

Representative format:

```text
[diagnostic-error] operation=<operation> | test=<node-id> | phase=<phase> | error=<error>
```

Diagnostic errors are:

* logged through the project diagnostics logger
* added to the failed Pytest report diagnostic sections

The logger name is:

```text
qa_automation.diagnostics
```

The project does not configure persistent log-file output for this logger.

## Playwright Assertions

Playwright assertions are used for browser and UI state validation.

Current assertion patterns include:

* URL validation
* element visibility
* hidden state
* form-field attributes
* authentication redirects
* Inventory visibility
* product card content
* Product Details content
* Cart state
* cart badge state
* Add to cart and Remove state
* checkout validation errors
* Checkout Overview content
* Checkout Complete content

Playwright assertions should be preferred for browser and UI state because they include built-in waiting behavior.

The default Playwright assertion timeout is configurable through:

```text
QA_EXPECT_TIMEOUT_MS
```

Current default:

```text
5000
```

Plain Python assertions remain appropriate for already extracted or calculated values such as:

* product names
* product prices
* sorted lists
* expected strings
* calculated checkout totals
* focused runtime configuration values

## pytest-html

pytest-html provides the lightweight HTML reporting layer.

It remains implemented for:

* local reporting where requested
* Smoke CI
* Regression CI
* full-suite CI

Current CI paths:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Smoke and Regression intentionally remain pytest-html-focused.

The full-suite job preserves pytest-html while also collecting Allure result data.

Allure does not replace pytest-html.

Phase 4F diagnostics operate alongside pytest-html rather than replacing it.

## Allure Pytest Integration

`allure-pytest` provides the Python-side integration between Pytest and Allure.

Its responsibility is to generate structured result data during test execution.

Current output:

```text
reports/allure-results/
```

Sequential collection:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Parallel collection:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Allure result collection supports:

* sequential execution
* pytest-xdist worker-level parallel execution

`--clean-alluredir` prevents stale result data from previous runs from being mixed into the current execution.

Phase 4F keeps Allure ownership separate from diagnostics.

## Allure CLI

The standalone Allure CLI converts result data into a browsable HTML report.

It is separate from the Python `allure-pytest` dependency.

Installing `allure-pytest` does not provide the standalone report generator.

Verify:

```bash
allure --version
```

Generate the report:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current generated output:

```text
reports/allure-report/
```

The Allure CLI is therefore required when local Allure HTML generation is needed.

In CI, the full-suite job prepares the required Java and Allure CLI environment.

## Failure Screenshot Policy

Browser-test failures use the existing custom screenshot mechanism in:

```text
conftest.py
```

The policy is controlled through:

```text
QA_SCREENSHOT_POLICY
```

Supported values:

```text
only-on-failure
off
```

Default:

```text
only-on-failure
```

With the default policy, screenshot capture occurs when:

* the Pytest report failed
* the failure phase is `call`
* a Playwright page is available

Current output:

```text
reports/screenshots/
```

Screenshot filenames contain:

* the test name
* a UTC timestamp

The screenshot is captured once.

After successful capture, the same PNG is attached to Allure as:

```text
Failure screenshot
```

when Allure result collection is active.

The successful screenshot path is also included in the Phase 4F failed-test summary.

The framework does not introduce a second project-level screenshot capture implementation.

If screenshot capture fails:

* the failure is reported through the Phase 4F diagnostic mechanism
* no screenshot path is added
* no Allure screenshot attachment is attempted because no screenshot file exists

If the Allure attachment fails after successful screenshot capture:

* the attachment failure is reported through the Phase 4F diagnostic mechanism
* the original PNG remains available under `reports/screenshots/`
* the screenshot path remains available in the failed-test summary

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom failure screenshot is not written and the corresponding Allure screenshot attachment is not created.

Setup-phase and teardown-phase failures receive Phase 4F failure diagnostics but do not trigger the custom project screenshot.

## Playwright Trace Policy

Trace policy is controlled through:

```text
QA_TRACE_POLICY
```

Supported values:

```text
off
retain-on-failure
on
```

Default:

```text
off
```

Example:

```bash
QA_TRACE_POLICY=retain-on-failure pytest -m regression -v
```

Trace generation uses pytest-playwright / Playwright runtime capabilities.

The project does not maintain custom trace recording logic.

Generated trace output uses pytest-playwright runtime artifact storage rooted under:

```text
test-results/
```

Representative output:

```text
trace.zip
```

Explicit native pytest-playwright trace options remain usable and take precedence when explicitly provided.

Current CI uses:

```text
QA_TRACE_POLICY=off
```

and therefore does not retain traces by default.

Phase 4F does not change trace ownership or automatically enable traces.

## Playwright Video Policy

Video policy is controlled through:

```text
QA_VIDEO_POLICY
```

Supported values:

```text
off
retain-on-failure
on
```

Default:

```text
off
```

Example:

```bash
QA_VIDEO_POLICY=on pytest tests/test_login_page.py -v
```

Video generation uses pytest-playwright / Playwright runtime capabilities.

The project does not maintain custom video recording logic.

Generated video output uses the pytest-playwright runtime artifact structure rooted under:

```text
test-results/
```

Representative output:

```text
video.webm
```

Explicit native pytest-playwright video options remain usable and take precedence when explicitly provided.

Current CI uses:

```text
QA_VIDEO_POLICY=off
```

and therefore does not retain video by default.

Phase 4F does not change video ownership or automatically enable video capture.

## Reporting And Diagnostic Compatibility

Current reporting and diagnostic behavior supports:

* sequential Pytest execution
* pytest-xdist worker-level execution
* one non-duplicated runtime header during xdist execution
* setup/call/teardown failure diagnostics
* pytest-html generation
* Allure result collection
* configurable failure screenshots
* failure screenshot attachment to Allure
* generated Allure HTML reports
* optional Playwright trace generation
* optional Playwright video generation
* centralized runtime configuration
* separated framework and scenario fixture responsibilities

No sequential-only diagnostic or reporting exception is required.

Reporting does not change test-isolation requirements.

Diagnostics do not change test-isolation requirements.

Runtime configuration does not change test-isolation requirements.

Tests must remain independent regardless of:

* execution mode
* reporting mode
* diagnostic context
* artifact policies

## Generated Runtime Output

Reports and persistent browser artifacts are generated runtime data rather than repository source content.

Current generated areas include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
test-results/
playwright-report/
```

These outputs are used for:

* local debugging
* failure analysis
* execution evidence
* report inspection
* CI artifact publishing where configured

They should not be committed to Git.

The repository ignore policy includes protection for:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
test-results/
playwright-report/
```

The implemented Allure output paths are nested inside:

```text
reports/
```

and are already covered by the `reports/*` rule.

The additional root-level Allure entries protect against alternate local Allure paths.

`test-results/` protects pytest-playwright-generated trace and video content.

Phase 4F runtime and failed-test summaries do not create another generated-output directory.

Persistent diagnostic log files are not implemented.

## Local Quality Workflow

Before pushing changes or opening a Pull Request where full validation is required, the standard sequential validation is:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

If formatting changes are needed:

```bash
black .
isort .
```

Then validate again:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Sequential execution remains the supported baseline for normal local validation.

## Parallel Validation

When worker safety, fixture isolation, execution behavior, or xdist-compatible diagnostics are part of the scope, use:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Parallel validation is not automatically required for every unrelated code or documentation task.

It should be used when the active scope can affect execution isolation or parallel behavior.

Phase 4F fixture separation and diagnostics were validated under pytest-xdist execution.

## Runtime Configuration Validation

When runtime configuration behavior is affected, validate the focused configuration module:

```bash
pytest tests/test_runtime_config.py
```

Representative environment-driven suite execution should additionally be used where required.

Example:

```bash
QA_BROWSER=chromium \
QA_HEADED=false \
QA_TIMEOUT_MS=20000 \
QA_EXPECT_TIMEOUT_MS=4000 \
pytest -m smoke -v
```

For changes affecting screenshot, trace, or video policies, controlled runtime artifact validation may additionally be required.

Temporary intentionally failing tests used only to validate artifact behavior should not be committed.

## Diagnostic Validation

When Phase 4F diagnostic behavior changes, controlled failure validation should verify the relevant failure context.

Expected diagnostic behavior includes:

* runtime summary visibility
* effective runtime values
* no duplicate runtime header from xdist workers
* failed-test node ID
* failure phase
* current URL when the Playwright page is available
* screenshot path after successful custom screenshot capture
* diagnostic error visibility if evidence collection itself fails

Screenshot-specific controlled failure validation should use a failed test-call when screenshot-path behavior must be verified.

Setup and teardown failures should be treated separately because the custom project screenshot is intentionally call-phase-only.

Temporary tests introduced solely to trigger controlled failure behavior should not be committed.

## Reporting Validation

When reporting behavior changes, validate result collection and report generation.

Example:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Then:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Expected outputs:

```text
reports/report.html
reports/allure-results/
reports/allure-report/
```

Failure screenshot behavior should additionally be validated when changes affect:

* `conftest.py`
* screenshot policy
* screenshot capture
* Allure screenshot attachments
* failed-test screenshot path diagnostics

Trace and video behavior should be validated when changes affect:

* trace policy
* video policy
* pytest-playwright runtime integration

## Scoped Local Validation

During implementation, relevant scoped validation may be run before the full suite.

### Login Changes

```bash
pytest -v tests/test_login_page.py
pytest -m security -v
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
```

### Inventory Changes

```bash
pytest -v tests/test_inventory_page.py
pytest -m sorting -v
pytest tests/test_inventory_page.py -m navigation -v
```

### Product Details Changes

```bash
pytest -v tests/test_product_details_page.py
pytest tests/test_product_details_page.py -m navigation -v
pytest tests/test_product_details_page.py -m regression -v
```

### Cart Changes

```bash
pytest -v tests/test_cart_page.py
pytest tests/test_cart_page.py -m navigation -v
pytest tests/test_cart_page.py -m regression -v
```

### Checkout Changes

```bash
pytest -v tests/test_checkout_page.py
pytest tests/test_checkout_page.py -m navigation -v
pytest tests/test_checkout_page.py -m regression -v
pytest tests/test_checkout_page.py -m e2e -v
```

### Runtime Configuration Changes

```bash
pytest tests/test_runtime_config.py
```

### Primary Purchase Journey Changes

```bash
pytest -m e2e -v
```

Scoped validation should normally be followed by complete-suite validation before merge unless an explicit scoped-validation exception is accepted.

## Full Workstream Validation

For checkpoint, stabilization, or portfolio-promotion work, page-level validation may include:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest -v
```

Quality checks:

```bash
ruff check .
black --check .
isort . --check-only
```

When parallel execution is relevant:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

When runtime configuration is relevant:

```bash
pytest tests/test_runtime_config.py
```

When reporting is relevant:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir

allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

When diagnostics are relevant, controlled failure validation should verify the applicable Phase 4F runtime and failed-test context.

Validation scope should remain aligned with the active task rather than automatically running every possible check after every documentation-only change.

## Phase 4F Validation Status

Phase 4F implementation was validated with:

```text
Smoke: 31 passed
Regression: 109 passed
Full sequential: 236 passed
Full pytest-xdist: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

Controlled failure validation also confirmed that after fixture responsibility separation the framework still provides:

* runtime header
* failure phase
* Pytest node ID
* current page URL
* screenshot diagnostic path

These results validate the implemented Phase 4F framework behavior rather than creating new permanent validation commands or test suites.

## CI Quality Checks

GitHub Actions validates the project according to configured workflow triggers.

The current pipeline combines:

* Phase 4B CI job structure
* Phase 4C parallel execution
* Phase 4D reporting
* Phase 4E runtime configuration
* Phase 4F diagnostics through the existing Pytest execution path

Current structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first.

After successful quality validation:

* Smoke
* Regression
* full-suite

become independently executable browser-test jobs.

GitHub Actions may schedule those jobs concurrently.

Inside each browser job, pytest-xdist distributes tests between workers.

These are separate concurrency layers.

Reporting, runtime configuration, and diagnostics are layered on top of those execution layers.

Phase 4F does not introduce another CI job or concurrency layer.

## Quality CI Job

The `quality` job executes:

```bash
ruff check .
black --check .
isort . --check-only
```

It additionally performs:

* repository checkout
* Python 3.12 setup
* dependency installation

The quality job does not:

* install Chromium
* execute browser tests
* use pytest-xdist
* generate browser-test reports
* require the Phase 4E browser runtime environment values

A failure in `quality` prevents all three browser jobs from starting.

## CI Runtime Defaults

Smoke, Regression, and full-suite explicitly use:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

These values intentionally match the approved local defaults.

Current CI therefore remains:

* Chromium-only
* headless
* pytest-xdist parallel
* failure screenshot enabled
* trace disabled by default
* video disabled by default
* Phase 4F runtime diagnostics enabled through normal Pytest execution

The current CI runtime configuration does not introduce:

* browser matrices
* Firefox CI installation
* WebKit CI installation
* workflow-dispatch runtime forms
* secrets for these non-secret values
* retries
* `continue-on-error`
* default trace retention
* default video retention
* diagnostic-specific environment variables

## Smoke CI Job

Smoke executes the approved marker suite through pytest-xdist.

Core command:

```bash
pytest -m smoke -n auto -v
```

The actual workflow additionally generates:

```text
reports/smoke-report.html
```

and uploads Smoke-specific artifacts.

Smoke remains pytest-html-focused.

It does not generate a dedicated Allure report.

The job uses the explicit Phase 4E CI runtime defaults.

Phase 4F runtime diagnostics operate through the same Pytest execution.

## Regression CI Job

Regression executes through pytest-xdist.

Core command:

```bash
pytest -m regression -n auto -v
```

The workflow additionally generates:

```text
reports/regression-report.html
```

and uploads Regression-specific artifacts.

Regression remains pytest-html-focused.

It does not generate a dedicated Allure report.

The job uses the explicit Phase 4E CI runtime defaults.

Phase 4F runtime diagnostics operate through the same Pytest execution.

## Full-Suite CI Job

The full-suite job executes the complete unfiltered suite through pytest-xdist.

Current command:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

This produces:

```text
reports/report.html
reports/allure-results/
```

The full-suite job remains:

* the complete CI regression gate
* the primary CI source for advanced Allure reporting

The workflow then attempts to generate:

```text
reports/allure-report/
```

from:

```text
reports/allure-results/
```

when usable result data exists.

The full-suite job uses the same Phase 4E defaults as Smoke and Regression.

Phase 4F does not change the full-suite topology or command structure.

## Allure CI Tooling

The full-suite job prepares:

* Java 17
* Allure CLI

Java is configured through:

```text
actions/setup-java@v4
```

using Temurin 17.

Allure CLI is installed with:

```bash
npm install -g allure-commandline
allure --version
```

These prerequisites are used only for Allure HTML generation.

They are not added to Smoke or Regression.

Phase 4F diagnostics do not require Java or the Allure CLI.

## Allure Generation After Test Failure

The Allure HTML generation step uses:

```yaml
if: always()
```

The step checks that:

```text
reports/allure-results/
```

exists and contains usable result data before calling the Allure CLI.

This allows report generation to be attempted after a failed full-suite test command.

A failed Pytest command still fails the full-suite job.

Reporting does not convert failed test execution into successful CI validation.

Diagnostics also do not change the failure result.

## CI Marker Coverage

Dedicated CI jobs currently exist for:

* Smoke
* Regression

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

These markers remain available for selective local validation.

Tests assigned to them still participate in the complete full-suite CI job.

## GitHub Actions Concurrency And pytest-xdist

The current execution model contains two distinct concurrency layers.

GitHub Actions job-level concurrency:

```text
quality
├── smoke
├── regression
└── full-suite
```

After `quality` succeeds, the browser jobs may run independently.

pytest-xdist worker-level parallelism:

```text
smoke / regression / full-suite
        ↓
pytest -n auto
        ↓
xdist workers
```

GitHub Actions controls independent workflow jobs.

pytest-xdist controls test distribution within each browser-test job.

These mechanisms should not be treated as equivalent.

Reporting does not add another concurrency layer.

Runtime configuration does not add another concurrency layer.

Diagnostics do not add another concurrency layer.

## CI Reports And Artifacts

Current browser-test jobs generate self-contained pytest-html reports.

### Smoke Artifacts

```text
smoke-pytest-html-report
smoke-test-artifacts
```

### Regression Artifacts

```text
regression-pytest-html-report
regression-test-artifacts
```

### Full-Suite Artifacts

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The broader full-suite runtime artifact publishes:

```text
reports/
```

Artifact upload steps use:

```yaml
if: always()
```

Available reporting and screenshot output can therefore be uploaded when an executing browser-test command fails.

If `quality` fails, browser jobs do not start and no browser-test artifacts are generated for that workflow run.

Current retention:

```text
7 days
```

Trace and video are disabled under the default CI runtime configuration and are therefore not added as dedicated retained CI artifacts.

Phase 4F does not introduce a persistent diagnostic artifact or log-file artifact.

Detailed behavior is documented in:

```text
docs/ci-cd-pipeline.md
```

## Quality Gates

The project uses several quality gates.

### Local Quality Gate

Where complete local validation is required:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

### Parallel Execution Gate

When the active scope affects test isolation, fixture ownership, worker-level execution, or parallel diagnostic behavior:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

### Runtime Configuration Gate

When runtime configuration behavior changes:

```bash
pytest tests/test_runtime_config.py
```

The relevant environment-driven execution should additionally be validated when required.

### Diagnostic Gate

When Phase 4F diagnostic behavior changes, controlled failure validation should confirm the affected diagnostic fields and failure phase.

Relevant checks may include:

* runtime header
* effective runtime values
* xdist header de-duplication
* node ID
* failure phase
* page URL
* screenshot path
* diagnostic-operation errors

Controlled failing tests created only for this validation should not remain committed.

### Reporting Gate

When reporting behavior changes:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir

allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Validation should confirm:

* pytest-html output is generated
* Allure result data is generated
* Allure HTML generation succeeds
* failure screenshots remain available when expected
* Allure attachments reuse the existing PNG
* failed-test screenshot path diagnostics remain correct when applicable
* generated output remains untracked

When trace or video behavior changes, the corresponding runtime policies and generated pytest-playwright output should additionally be validated.

### Pre-commit Quality Gate

```bash
pre-commit run --all-files
```

### Scoped Workstream Quality Gate

Run relevant modules and marker suites for the changed behavior.

Examples:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest tests/test_runtime_config.py
```

Scoped validation should normally be followed by full-suite validation before merge unless an explicit scoped exception is accepted.

### CI Quality Gate

Before merging a Pull Request:

* GitHub Actions must pass
* Ruff must pass
* Black must pass
* isort must pass
* required browser jobs must pass
* full-suite validation must pass
* expected pytest-html artifacts should be available
* expected full-suite Allure artifact should be available
* runtime artifacts should remain available for failure investigation when generated
* CI runtime defaults should remain aligned with `config/settings.py`
* diagnostics should remain consistent with `framework/diagnostics.py` and root `conftest.py`
* Chromium-only CI boundaries should remain intact unless explicitly changed by approved scope

The current dependency model is:

```text
quality
├── smoke
├── regression
└── full-suite
```

A failed quality job prevents browser execution.

Smoke, Regression, and full-suite do not depend on each other.

All three browser-test jobs use pytest-xdist.

### Portfolio Promotion Quality Gate

Before promoting `develop` to `main`:

* local validation should pass when required and practical
* CI on the promotion Pull Request should pass
* documentation should match implementation
* runtime configuration documentation should match `config/settings.py`, root `conftest.py`, Page Objects, and CI
* diagnostic documentation should match `framework/diagnostics.py` and root `conftest.py`
* fixture documentation should reflect the root `conftest.py` / `tests/conftest.py` responsibility boundary
* reporting documentation should match pytest-html, Allure, screenshot, trace, and video behavior
* planned functionality should not be presented as implemented
* generated reports, screenshots, traces, videos, caches, and virtual-environment files should not be tracked
* `main` should remain suitable as the stable portfolio version

## Runtime Configuration Scope Boundaries

The current runtime configuration implementation includes:

* environment-variable runtime settings
* base URL configuration
* browser selection
* headed/headless selection
* action/navigation timeout
* assertion timeout
* screenshot policy
* trace policy
* video policy
* validation and normalization
* pytest-playwright integration
* explicit CI defaults

It does not implement:

* named environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI
* Firefox CI installation
* WebKit CI installation
* device emulation
* mobile emulation
* browser channels
* slow-motion configuration
* retries

Phase 4F diagnostics and fixture cleanup are implemented and are not part of the remaining runtime-configuration scope.

These boundaries should remain explicit in project documentation.

## Reporting And Diagnostic Scope Boundaries

The current implemented reporting and diagnostic stack includes:

* effective runtime summary
* xdist runtime-header de-duplication
* failed-test node ID reporting
* setup/call/teardown failure-phase reporting
* current page URL diagnostics when available
* custom screenshot path diagnostics when available
* diagnostic error reporting
* lightweight project diagnostics logger
* pytest-html
* allure-pytest
* Allure CLI
* configurable failure screenshots
* Allure failure screenshot attachments
* configurable Playwright trace generation
* configurable Playwright video generation
* GitHub Actions artifacts

Current reporting and diagnostics do not implement:

* persistent project log files
* browser console capture
* network capture
* custom network tracing beyond Playwright trace
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* Allure history persistence
* trend-history storage
* report hosting
* GitHub Pages reporting
* retries
* cross-browser reporting
* default trace retention in CI
* default video retention in CI

Trace and video policies are implemented.

They are not future-only functionality.

They remain disabled by default.

Phase 4F runtime and failed-test diagnostics are implemented.

They should not be described as future-only functionality.

## Current Quality Status

The current quality tooling supports the implemented Playwright framework covering:

* Login
* Inventory
* Product Details
* Cart
* Checkout

Current capabilities include:

* Page Object Model
* shared authenticated behavior through `AppPage`
* reusable assertions
* reusable scenario-oriented fixtures
* separated framework-level and scenario fixture responsibilities
* centralized test data
* parametrization
* normalized marker categorization
* selective Smoke execution
* selective Regression execution
* selective UI execution
* selective Security execution
* selective Sorting execution
* selective Navigation execution
* independent E2E checkpoint execution
* sequential Pytest execution
* pytest-xdist worker-level execution
* parallel Smoke validation
* parallel Regression validation
* parallel full-suite validation
* centralized runtime configuration
* base URL configuration
* browser runtime selection
* headed/headless configuration
* Playwright timeout configuration
* assertion timeout configuration
* screenshot policy
* trace policy
* video policy
* fail-fast invalid configuration behavior
* focused runtime configuration tests
* lightweight runtime summary diagnostics
* effective runtime value visibility
* xdist runtime-header de-duplication
* failed-test node ID diagnostics
* setup/call/teardown failure-phase diagnostics
* current page URL diagnostics
* custom screenshot path diagnostics
* diagnostic-operation error reporting
* local quality validation
* dedicated CI quality validation
* dedicated parallel Smoke CI
* dedicated parallel Regression CI
* parallel complete full-suite CI
* explicit CI runtime defaults
* Chromium-only CI execution
* pytest-html report generation
* Allure result collection
* Allure HTML generation
* failure screenshots
* Allure screenshot attachments
* optional Playwright trace output
* optional Playwright video output
* job-specific CI artifacts
* dedicated full-suite Allure artifact
* generated runtime-output isolation

Current CI model:

```text
Phase 4E runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
quality
├── smoke
│   └── pytest-xdist workers
│       └── pytest-html
├── regression
│   └── pytest-xdist workers
│       └── pytest-html
└── full-suite
    └── pytest-xdist workers
        ├── pytest-html
        ├── Allure results
        ├── failure screenshots
        └── Allure HTML report
```

The quality job is the prerequisite gate.

Smoke and Regression have dedicated CI jobs.

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

The full-suite job remains the complete unfiltered regression gate and primary CI source for the Allure HTML report.

No sequential-only test, diagnostic, or reporting exceptions are required for the current implementation.

## Quality Goals

The quality tooling supports:

* consistent formatting
* readable code
* maintainable code
* automated local validation
* consistent imports
* reliable Pytest execution
* sequential and parallel execution
* selective marker-based validation
* worker-safe test independence
* centralized and validated runtime settings
* fail-fast configuration errors
* reproducible local and CI defaults
* lightweight runtime observability
* useful failed-test context
* explicit framework and scenario fixture responsibilities
* lightweight pytest-html reporting
* advanced Allure reporting
* configurable browser failure evidence
* optional Playwright diagnostics
* dedicated Smoke CI feedback
* dedicated Regression CI feedback
* complete full-suite protection
* reliable CI quality gates
* useful CI artifacts
* stable workstream integration
* professional Pull Request workflow
* test case traceability
* safe checkpoint validation
* stable portfolio promotion

## Current Phase Boundaries

### Phase 4B — CI Execution Strategy

Implemented capabilities include:

* separate code-quality validation
* dedicated Smoke CI
* dedicated Regression CI
* complete full-suite CI
* quality-gate dependencies
* job-specific pytest-html reports
* job-specific artifacts
* independent browser-job scheduling after `quality`

### Phase 4C — Parallel Execution

Implemented capabilities include:

* pytest-xdist worker-level parallel execution
* local parallel Smoke
* local parallel Regression
* local parallel full-suite
* sequential execution as a supported mode
* fixture and test-independence validation
* parametrized and E2E independence validation
* parallel Smoke CI
* parallel Regression CI
* parallel full-suite CI
* preserved Phase 4B topology
* preserved pytest-html behavior
* Chromium-only CI scope

GitHub Actions job concurrency and pytest-xdist worker parallelism remain separate mechanisms.

### Phase 4D — Reporting Upgrade

Implemented capabilities include:

* allure-pytest integration
* local Allure result collection
* local Allure HTML generation
* Allure CLI as the HTML-generation prerequisite
* existing failure screenshot reuse
* failure screenshot attachment to Allure
* sequential reporting compatibility
* pytest-xdist reporting compatibility
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* dedicated `full-suite-allure-report` artifact
* preservation of pytest-html
* preservation of existing browser-test artifacts
* generated reporting output excluded from repository source content

Phase 4D does not implement:

* Allure history persistence
* trend history
* hosted reports
* GitHub Pages reporting
* retries
* cross-browser reporting

### Phase 4E — Runtime Configuration

Implemented capabilities include:

* centralized `config/settings.py`
* environment-based runtime configuration
* `QA_BASE_URL`
* `QA_BROWSER`
* `QA_HEADED`
* `QA_TIMEOUT_MS`
* `QA_EXPECT_TIMEOUT_MS`
* `QA_SCREENSHOT_POLICY`
* `QA_TRACE_POLICY`
* `QA_VIDEO_POLICY`
* approved defaults
* normalization
* validation
* fail-fast invalid configuration behavior
* focused configuration tests
* runtime application URL composition through `BasePage`
* browser/runtime integration through root `conftest.py`
* action/navigation timeout integration
* assertion timeout integration
* configurable failure screenshot policy
* pytest-playwright trace integration
* pytest-playwright video integration
* preservation of explicit native runtime options where applicable
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* preservation of Chromium-only CI
* preservation of Phase 4B–4D execution and reporting structure

Phase 4E does not implement:

* environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI
* device emulation
* retries

### Phase 4F — Diagnostics And Fixture Cleanup

Implemented capabilities include:

* shared diagnostics implementation in `framework/diagnostics.py`
* runtime summary formatting
* failed-test summary formatting
* diagnostic error formatting
* project diagnostics logger
* effective runtime summary through `pytest_report_header`
* base URL visibility
* browser visibility
* headed/headless mode visibility
* action/navigation timeout visibility
* assertion timeout visibility
* screenshot policy visibility
* trace policy visibility
* video policy visibility
* runtime-header suppression on pytest-xdist workers
* failed-test Pytest node ID reporting
* setup/call/teardown failure-phase reporting
* current page URL reporting when a Playwright page is available
* custom screenshot path reporting after successful capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* framework-level Pytest responsibilities retained in root `conftest.py`
* application scenario fixtures separated into `tests/conftest.py`
* preservation of explicit scenario fixture names
* preservation of function-scoped fixture behavior
* preservation of pytest-playwright browser lifecycle
* preservation of pytest-playwright trace lifecycle
* preservation of pytest-playwright video lifecycle
* preservation of custom failure screenshot behavior
* preservation of Allure failure screenshot reuse
* sequential execution compatibility
* pytest-xdist execution compatibility
* Ruff validation
* Black validation
* isort validation

Phase 4F does not implement:

* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* new CI topology
* generic fixture factories
* dependency-injection infrastructure
* autouse redesign
* multi-layer fixture packages
* fixture scope redesign

## Future Improvements

Possible future quality-tooling improvements include:

* stricter Ruff rules where justified
* type checking with mypy
* test coverage reporting
* JUnit XML output
* refined pre-commit configuration
* persistent structured logging if justified by approved scope
* additional diagnostic evidence when justified
* Allure history and trend reporting
* hosted reporting
* additional CI execution improvements where justified

The following are already implemented and should not be described as future-only functionality:

* pytest-xdist parallel execution
* pytest-html reporting
* Allure reporting
* failure screenshot integration
* centralized runtime configuration
* base URL overrides
* browser runtime selection
* timeout configuration
* screenshot policy
* trace policy
* video policy
* explicit Phase 4E CI runtime defaults
* Phase 4F runtime diagnostics
* Phase 4F failed-test diagnostics
* diagnostic error reporting
* separation of framework-level hooks and application scenario fixtures

Future capabilities should not be described as implemented until their approved project scope has been completed and validated.