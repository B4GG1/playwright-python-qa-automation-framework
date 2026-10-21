from pathlib import Path

import pytest
from PIL import Image

from framework.visual_regression import compare_png_images

pytestmark = pytest.mark.visual


def _save_png(
    path: Path,
    *,
    size: tuple[int, int] = (4, 4),
    color: tuple[int, int, int, int] = (255, 255, 255, 255),
) -> None:
    Image.new("RGBA", size, color).save(path, format="PNG")


def test_identical_images_pass_without_creating_diff(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff" / "comparison.png"
    _save_png(baseline)
    _save_png(actual)

    compare_png_images(baseline, actual, diff)

    assert not diff.exists()


def test_mismatch_reports_pixel_count_bounds_and_paths(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff" / "comparison.png"
    _save_png(baseline)
    _save_png(actual)
    with Image.open(actual) as image:
        changed = image.copy()
    changed.putpixel((2, 1), (0, 0, 0, 255))
    changed.save(actual, format="PNG")

    with pytest.raises(AssertionError, match="Visual regression mismatch") as error:
        compare_png_images(baseline, actual, diff)

    message = str(error.value)
    assert "1/16 pixels differ (6.25%)" in message
    assert "(2, 1, 3, 2)" in message
    assert str(baseline) in message
    assert str(actual) in message
    assert str(diff) in message


def test_mismatch_creates_highlighted_diff_without_changing_baseline(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "visual" / "diff" / "comparison.png"
    _save_png(baseline)
    _save_png(actual)
    with Image.open(actual) as image:
        changed = image.copy()
    changed.putpixel((1, 2), (0, 0, 0, 255))
    changed.save(actual, format="PNG")

    with pytest.raises(AssertionError, match="Visual regression mismatch"):
        compare_png_images(baseline, actual, diff)

    assert diff.is_file()
    with Image.open(diff) as evidence:
        assert evidence.format == "PNG"
        assert evidence.getpixel((1, 2)) == (255, 0, 255)
        assert evidence.getpixel((0, 0)) == (255, 255, 255)
    with Image.open(baseline) as approved:
        assert approved.getpixel((1, 2)) == (255, 255, 255, 255)


def test_incompatible_dimensions_fail_without_diff(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    _save_png(baseline, size=(4, 4))
    _save_png(actual, size=(5, 4))

    with pytest.raises(AssertionError, match="image dimensions differ") as error:
        compare_png_images(baseline, actual, diff)

    assert "4x4" in str(error.value)
    assert "5x4" in str(error.value)
    assert not diff.exists()


def test_missing_baseline_fails_without_auto_approval(tmp_path: Path) -> None:
    baseline = tmp_path / "approved" / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    _save_png(actual)

    with pytest.raises(FileNotFoundError, match="baseline not found"):
        compare_png_images(baseline, actual, diff)

    assert not baseline.exists()
    assert not diff.exists()


def test_missing_actual_screenshot_fails_clearly(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    _save_png(baseline)

    with pytest.raises(FileNotFoundError, match="actual screenshot not found"):
        compare_png_images(baseline, actual, tmp_path / "diff.png")


def test_alpha_only_difference_is_detected(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    _save_png(baseline)
    _save_png(actual)
    with Image.open(actual) as image:
        changed = image.copy()
    changed.putpixel((0, 0), (255, 255, 255, 0))
    changed.save(actual, format="PNG")

    with pytest.raises(AssertionError, match="1/16 pixels differ"):
        compare_png_images(baseline, actual, diff)

    assert diff.is_file()


def test_diff_path_cannot_overwrite_approved_baseline(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    _save_png(baseline)
    _save_png(actual)

    with pytest.raises(ValueError, match="must not overwrite"):
        compare_png_images(baseline, actual, baseline)

    with Image.open(baseline) as approved:
        assert approved.getpixel((0, 0)) == (255, 255, 255, 255)
