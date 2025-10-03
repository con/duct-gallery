"""Unit tests for plotter module."""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock
import subprocess


def test_should_regenerate_plot(tmp_path):
    """Test plot regeneration logic."""
    from con_duct_gallery.plotter import should_regenerate_plot

    svg_path = tmp_path / "plot.svg"
    usage_json = tmp_path / "usage.json"

    # No SVG exists - should regenerate
    assert should_regenerate_plot(svg_path, usage_json, force=False) is True

    # Create files
    svg_path.write_text("<svg></svg>")
    usage_json.write_text("{}")

    # Both exist, not force - should not regenerate
    assert should_regenerate_plot(svg_path, usage_json, force=False) is False

    # Force flag - always regenerate
    assert should_regenerate_plot(svg_path, usage_json, force=True) is True


@patch('con_duct_gallery.plotter.subprocess.run')
def test_generate_plot(mock_run, tmp_path):
    """Test calling con-duct plot command."""
    from con_duct_gallery.plotter import generate_plot

    usage_json = tmp_path / "usage.json"
    usage_json.write_text("{}")
    output_svg = tmp_path / "output.svg"

    # Mock successful subprocess call
    mock_run.return_value = Mock(returncode=0)

    result = generate_plot(usage_json, output_svg)

    assert result == output_svg
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert "con-duct" in args
    assert "plot" in args
    assert str(output_svg) in args


@patch('con_duct_gallery.plotter.subprocess.run')
def test_plot_with_custom_options(mock_run, tmp_path):
    """Test passing custom plot options."""
    from con_duct_gallery.plotter import generate_plot

    usage_json = tmp_path / "usage.json"
    usage_json.write_text("{}")
    output_svg = tmp_path / "output.svg"

    mock_run.return_value = Mock(returncode=0)

    generate_plot(usage_json, output_svg, ["--style=seaborn", "--dpi=300"])

    args = mock_run.call_args[0][0]
    assert "--style=seaborn" in args
    assert "--dpi=300" in args


@patch('con_duct_gallery.plotter.subprocess.run')
def test_con_duct_not_found(mock_run, tmp_path):
    """Test handling con-duct command not found."""
    from con_duct_gallery.plotter import generate_plot

    usage_json = tmp_path / "usage.json"
    usage_json.write_text("{}")
    output_svg = tmp_path / "output.svg"

    # Mock FileNotFoundError
    mock_run.side_effect = FileNotFoundError()

    with pytest.raises(FileNotFoundError):
        generate_plot(usage_json, output_svg)
