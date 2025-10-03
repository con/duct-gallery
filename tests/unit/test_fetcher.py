"""Unit tests for fetcher module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json


def test_parse_output_paths():
    """Test parsing output_paths from info JSON."""
    from con_duct_gallery.fetcher import parse_output_paths

    info_json = {
        "output_paths": {
            "usage": "demo/example_output_usage.json",
            "stdout": "demo/example_output_stdout",
            "stderr": "demo/example_output_stderr",
            "info": "demo/example_output_info.json"
        }
    }

    base_url = "https://raw.githubusercontent.com/con/duct/abc123/demo/example_output_info.json"

    file_urls = parse_output_paths(info_json, base_url)

    assert "usage" in file_urls
    assert "example_output_usage.json" in file_urls["usage"]
    assert file_urls["usage"].startswith("https://")


@patch('con_duct_gallery.fetcher.requests.get')
def test_fetch_info_json(mock_get, tmp_path):
    """Test downloading and parsing info JSON."""
    from con_duct_gallery.fetcher import fetch_info_json

    # Mock response
    mock_response = Mock()
    mock_response.text = '{"output_paths": {}}'
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    dest = tmp_path / "info.json"
    result = fetch_info_json("https://example.com/info.json", dest)

    assert result == {"output_paths": {}}
    assert dest.exists()
    mock_get.assert_called_once()


def test_fetch_with_cache(tmp_path):
    """Test that cached files are reused."""
    from con_duct_gallery.fetcher import fetch_log_files
    from con_duct_gallery.models import ExampleEntry

    # Create fake cached files
    example_dir = tmp_path / "test-example"
    example_dir.mkdir()
    (example_dir / "example_output_info.json").write_text("{}")
    (example_dir / "example_output_usage.json").write_text("{}")
    (example_dir / "example_output_stdout").write_text("")
    (example_dir / "example_output_stderr").write_text("")

    example = ExampleEntry(
        title="Test Example",
        source_repo="https://github.com/test/repo",
        info_file="https://example.com/info.json"
    )

    # Should use cache (no network calls)
    with patch('con_duct_gallery.fetcher.fetch_info_json') as mock_fetch:
        result = fetch_log_files(example, tmp_path, force=False)
        mock_fetch.assert_not_called()  # Cache used
        assert result.info_json.exists()
