"""Module for generating SVG plots from con/duct logs."""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def should_regenerate_plot(
    svg_path: Path,
    usage_json: Path,
    force: bool = False
) -> bool:
    """Check if plot needs regeneration.

    Args:
        svg_path: Path to SVG plot file
        usage_json: Path to usage JSON file
        force: If True, always regenerate

    Returns:
        True if plot should be regenerated
    """
    if force:
        return True

    if not svg_path.exists():
        return True

    # Check if usage JSON is newer than SVG (with 1 second tolerance for test timing)
    if usage_json.exists():
        svg_mtime = svg_path.stat().st_mtime
        usage_mtime = usage_json.stat().st_mtime
        # Only regenerate if usage is clearly newer (more than 1 second difference)
        if usage_mtime > svg_mtime + 1:
            return True

    return False


def generate_plot(
    usage_json: Path,
    output_svg: Path,
    plot_options: list[str] = None
) -> Path:
    """Generate SVG plot using con-duct plot command.

    Args:
        usage_json: Path to usage JSON file
        output_svg: Path for output SVG file
        plot_options: Additional options to pass to con-duct plot

    Returns:
        Path to generated SVG file

    Raises:
        FileNotFoundError: If con-duct command not found
        subprocess.CalledProcessError: If plot generation fails
    """
    if plot_options is None:
        plot_options = []

    # Ensure output directory exists
    output_svg.parent.mkdir(parents=True, exist_ok=True)

    # Build command
    cmd = ['con-duct', 'plot', '--output', str(output_svg)]
    cmd.extend(plot_options)
    cmd.append(str(usage_json))

    logger.debug(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        logger.debug(f"Plot generated: {output_svg}")
        return output_svg
    except FileNotFoundError:
        logger.error("con-duct command not found. Please install con-duct: pip install con-duct")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"Plot generation failed: {e.stderr}")
        raise
