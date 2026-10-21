import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.getgroup("visual regression").addoption(
        "--update-visual-baselines",
        action="store_true",
        default=False,
        help="Explicitly create or replace approved visual regression baselines.",
    )


@pytest.fixture()
def browser_context_args(
    browser_context_args: dict[str, object],
) -> dict[str, object]:
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "device_scale_factor": 1,
        "color_scheme": "light",
        "reduced_motion": "reduce",
    }


@pytest.fixture()
def update_visual_baselines(request: pytest.FixtureRequest) -> bool:
    return bool(request.config.getoption("--update-visual-baselines"))
