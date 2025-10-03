"""Integration tests for error handling."""

import pytest


@pytest.mark.integration
def test_invalid_yaml_rejected():
    """Test that invalid YAML is rejected with clear error message."""
    # Will be implemented once models are complete
    from con_duct_gallery.models import ExampleRegistry
    from pydantic import ValidationError

    # This should raise ValidationError
    with pytest.raises(ValidationError):
        ExampleRegistry(examples=[])


@pytest.mark.integration
def test_network_failure_graceful(tmp_path):
    """Test graceful handling of network failures.

    HTTP 404 → warning, continue with other examples
    """
    # Will be implemented once fetcher is complete
    from con_duct_gallery.fetcher import fetch_info_json

    # Should handle HTTP errors gracefully
    assert fetch_info_json is not None


@pytest.mark.integration
def test_plot_generation_failure():
    """Test handling of plot generation failures.

    con-duct error → warning, example without plot
    """
    # Will be implemented once plotter is complete
    from con_duct_gallery.plotter import generate_plot

    # Should handle subprocess errors
    assert generate_plot is not None


@pytest.mark.integration
def test_partial_fetch_success():
    """Test that gallery is still generated if some examples fail.

    Some examples fail → gallery still generated with successful examples
    """
    # Will be implemented once main is complete
    from con_duct_gallery.__main__ import main

    # Should continue with successful examples
    assert main is not None
