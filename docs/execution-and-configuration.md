# Execution and Configuration

This guide explains how to set up and run the **completed Playwright Python QA Automation Framework portfolio project** and adjust its supported runtime settings. Commands are intended for a Linux or WSL2 shell and are executed from the repository root unless stated otherwise.

## Prerequisites

- **Local Playwright execution:** Python 3.12, Git, and a compatible Linux/WSL2 environment. Playwright browser binaries and system dependencies are installed during setup.
- **Selenium execution:** Google Chrome must also be installed. Selenium Manager resolves the compatible ChromeDriver automatically.
- **Docker execution:** Docker Engine or Docker Desktop with Linux containers and a working Docker daemon. A host Python environment is not required for this path.
- **Allure HTML reports (optional):** The standalone Allure CLI is needed to render local Allure results; installing Python dependencies alone does not install the CLI.

The framework tests the externally hosted [Sauce Demo](https://www.saucedemo.com) application. It does not start or host the application locally.

## Local Setup

Clone the `develop` branch:

```bash
git clone --branch develop https://github.com/B4GG1/playwright-python-qa-automation-framework.git
cd playwright-python-qa-automation-framework

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
playwright install --with-deps chromium firefox webkit
```

`requirements-lock.txt` provides pinned dependency versions; `requirements.txt` is the unpinned dependency declaration. Installing only Chromium is sufficient for the primary Playwright suite, but Firefox and WebKit are needed for the cross-browser Smoke runs below.

## Run Playwright Tests

The default `pytest.ini` collection root is `tests/`. With no overrides, Playwright uses headless Chromium against Sauce Demo.

| Purpose                           | Command                                         |
|-----------------------------------|-------------------------------------------------|
| Complete default test collection  | `pytest -v`                                     |
| Smoke                             | `pytest -m smoke -v`                            |
| Regression                        | `pytest -m regression -v`                       |
| Primary purchase-flow checkpoints | `pytest -m e2e -v`                              |
| Selected test module              | `pytest tests/test_cart_page.py -v`             |
| Parallel full suite               | `pytest -n auto -v`                             |
| Parallel Smoke                    | `pytest -m smoke -n auto -v`                    |
| Firefox Smoke                     | `QA_BROWSER=firefox pytest -m smoke -n auto -v` |
| WebKit Smoke                      | `QA_BROWSER=webkit pytest -m smoke -n auto -v`  |

Chromium is the primary full-suite browser. Firefox and WebKit execute the representative Smoke selection; these commands do not imply complete cross-browser Regression coverage. The default collection includes framework-focused tests under `tests/`, but not the separate Selenium or screenshot-checkpoint suites.

Pytest markers can also be combined, for example `pytest -m "smoke and ui" -v`. Marker intent and test selection principles are described in [Testing Strategy](testing-strategy.md).

## Run Selenium Tests

The Selenium showcase uses headless Google Chrome, independent WebDriver sessions, and its own test collection. It does **not** use `QA_BROWSER` or pytest-xdist.

```bash
# Eight purchase-journey E2E checkpoints
pytest selenium_tests -m "selenium and e2e" -v

# All Selenium tests, including the WebDriver lifecycle check
pytest selenium_tests -m selenium -v
```

A local Chrome installation is required. Selenium Manager handles ChromeDriver resolution; the repository does not pin a separate driver executable.

## Run Tests in Docker

The repository `Dockerfile` uses the pinned official Playwright Python image and installs project dependencies from `requirements-lock.txt`. Build the image after changing source files or locked dependencies:

```bash
docker build -t playwright-qa-framework:local .
```

Run the Playwright Smoke suite:

```bash
docker run --rm --init --ipc=host \
  playwright-qa-framework:local -m smoke -v
```

Test-selection arguments follow the image name because the container entrypoint invokes `python -m pytest`. Runtime settings can be passed with `-e`, for example:

```bash
docker run --rm --init --ipc=host \
  -e QA_BROWSER=firefox \
  playwright-qa-framework:local -m smoke -v
```

Container-generated files disappear when the container is removed unless the relevant output directories are mounted. To retain a local HTML report:

```bash
mkdir -p reports

docker run --rm --init --ipc=host \
  --user "$(id -u):$(id -g)" \
  -v "$PWD/reports:/app/reports" \
  playwright-qa-framework:local \
  -o cache_dir=/tmp/pytest_cache \
  -m smoke -v \
  --html=reports/docker-smoke.html --self-contained-html
```

Docker provides an additional Playwright execution environment; it does not run the separate Chrome-based Selenium showcase.

## Run Visual Regression Checks

Screenshot comparisons use **headless Chromium in the pinned Docker environment** with reviewed baselines. They are separate from the default functional test collection.

```bash
docker build -t playwright-qa-framework:visual .
mkdir -p reports/visual

docker run --rm --init --ipc=host \
  -v "$PWD/visual_baselines:/app/visual_baselines:ro" \
  -v "$PWD/reports/visual:/app/reports/visual" \
  -e QA_BASE_URL=https://www.saucedemo.com \
  -e QA_BROWSER=chromium \
  -e QA_HEADED=false \
  playwright-qa-framework:visual \
  visual_tests -m visual --browser chromium -v
```

The baseline mount is read-only during normal comparison. Only when intentionally refreshing reviewed baselines, use a **writable** mount and the explicit update flag:

```bash
docker run --rm --init --ipc=host \
  -v "$PWD/visual_baselines:/app/visual_baselines" \
  -v "$PWD/reports/visual:/app/reports/visual" \
  -e QA_BROWSER=chromium \
  -e QA_HEADED=false \
  playwright-qa-framework:visual \
  visual_tests -m visual --browser chromium --update-visual-baselines -v
```

Review the updated PNGs and their Git diff before committing them. Ordinary execution never approves new baselines. Firefox, WebKit, headed mode, and parallel visual checkpoint execution are outside the approved visual comparison setup.

## Runtime Configuration

Configuration is loaded from environment variables by `config/settings.py`. The following are the default values for local Playwright execution:

| Environment variable   | Default                     | Purpose / supported values                                          |
|------------------------|-----------------------------|---------------------------------------------------------------------|
| `QA_BASE_URL`          | `https://www.saucedemo.com` | Target application origin (`http` or `https`, no path/query)        |
| `QA_BROWSER`           | `chromium`                  | `chromium`, `firefox`, `webkit` (Playwright only)                   |
| `QA_HEADED`            | `false`                     | Headed (`true`) or headless (`false`) Playwright execution          |
| `QA_TIMEOUT_MS`        | `30000`                     | Non-negative action/navigation timeout in milliseconds              |
| `QA_EXPECT_TIMEOUT_MS` | `5000`                      | Non-negative assertion/expect timeout in milliseconds               |
| `QA_SCREENSHOT_POLICY` | `only-on-failure`           | `only-on-failure`, `off` for project Playwright failure screenshots |
| `QA_TRACE_POLICY`      | `off`                       | `off`, `retain-on-failure`, `on` for Playwright tracing             |
| `QA_VIDEO_POLICY`      | `off`                       | `off`, `retain-on-failure`, `on` for Playwright video capture       |

Values are validated at startup; unsupported values produce a configuration error. Boolean values also accept `1`/`0`, `yes`/`no`, and `on`/`off`. Timeout values are expressed in milliseconds.

For a temporary override in a Linux/WSL shell:

```bash
QA_BROWSER=chromium \
QA_HEADED=true \
QA_TRACE_POLICY=retain-on-failure \
pytest -m smoke -v
```

Native pytest-playwright options such as `--browser`, `--headed`, `--tracing`, and `--video` are also supported; explicitly supplied browser/tracing/video options take precedence over their corresponding project defaults. Settings control the Playwright execution path, except that Selenium also uses `QA_BASE_URL`, `QA_TIMEOUT_MS`, and `QA_EXPECT_TIMEOUT_MS` where applicable. Selenium always launches headless Chrome in the current implementation.

Visual regression enforces its own fixed rendering conditions and is not a general headed or cross-browser test run.

## Reports and Results

To generate a local pytest-html report and Allure result data:

```bash
mkdir -p reports
pytest -v \
  --html=reports/report.html --self-contained-html \
  --alluredir=reports/allure-results --clean-alluredir
```

The standalone Allure CLI can render that result directory with `allure generate reports/allure-results --clean -o reports/allure-report`. Test execution can also produce failure screenshots, traces, videos, and visual comparison evidence. Generated outputs are excluded from version control, while reviewed visual baselines are committed. Their ownership and locations are described in [Project Structure](project-structure.md); CI quality gates, uploaded artifacts, and report interpretation are covered in [CI, Quality, and Reporting](ci-quality-and-reporting.md).