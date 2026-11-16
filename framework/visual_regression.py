from pathlib import Path

from PIL import Image, ImageChops


def compare_png_images(
    baseline_path: str | Path,
    actual_path: str | Path,
    diff_path: str | Path,
    *,
    max_different_pixels: int = 0,
) -> None:
    baseline_path = Path(baseline_path)
    actual_path = Path(actual_path)
    diff_path = Path(diff_path)

    if max_different_pixels < 0:
        raise ValueError("max_different_pixels must be greater than or equal to 0")

    if not baseline_path.is_file():
        raise FileNotFoundError(f"Visual regression baseline not found: {baseline_path}")
    if not actual_path.is_file():
        raise FileNotFoundError(f"Visual regression actual screenshot not found: {actual_path}")
    if diff_path.resolve() in {baseline_path.resolve(), actual_path.resolve()}:
        raise ValueError(
            "The visual diff path must not overwrite the baseline or actual screenshot"
        )

    try:
        with Image.open(baseline_path) as baseline_file, Image.open(actual_path) as actual_file:
            if baseline_file.format != "PNG" or actual_file.format != "PNG":
                raise ValueError(
                    "Visual regression expects PNG files: "
                    f"baseline={baseline_path}, actual={actual_path}"
                )

            if baseline_file.size != actual_file.size:
                raise AssertionError(
                    "Visual regression image dimensions differ: "
                    f"baseline={baseline_path} ({baseline_file.width}x{baseline_file.height}), "
                    f"actual={actual_path} ({actual_file.width}x{actual_file.height})"
                )

            baseline = baseline_file.convert("RGBA")
            actual = actual_file.convert("RGBA")
    except OSError as exc:
        raise ValueError(
            f"Unable to read comparison PNGs: baseline={baseline_path}, actual={actual_path}: {exc}"
        ) from exc

    channels = ImageChops.difference(baseline, actual).split()
    mask = channels[0]
    for channel in channels[1:]:
        mask = ImageChops.lighter(mask, channel)

    bounds = mask.getbbox()
    if bounds is None:
        return

    binary_mask = mask.point(lambda value: 255 if value else 0)
    different_pixels = binary_mask.histogram()[255]

    if different_pixels <= max_different_pixels:
        return

    total_pixels = baseline.width * baseline.height

    diff = actual.convert("RGB")
    diff.paste((255, 0, 255), mask=binary_mask)
    diff_path.parent.mkdir(parents=True, exist_ok=True)
    diff.save(diff_path, format="PNG")

    raise AssertionError(
        "Visual regression mismatch: "
        f"{different_pixels}/{total_pixels} pixels differ "
        f"({100 * different_pixels / total_pixels:.2f}%). "
        f"Allowed pixel difference: {max_different_pixels}. "
        f"Changed bounds (left, top, right, bottom): {bounds}. "
        f"Baseline: {baseline_path}; Actual: {actual_path}; Diff: {diff_path}"
    )
