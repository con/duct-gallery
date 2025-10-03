"""Module for fetching con/duct log files from online sources."""

import json
import logging
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urljoin, urlparse

import requests

from .models import ExampleEntry

logger = logging.getLogger(__name__)


class FetchedLog(NamedTuple):
    """Represents downloaded con/duct log files for an example."""
    info_json: Path
    usage_json: Path
    stdout: Path
    stderr: Path


def fetch_info_json(url: str, dest: Path) -> dict:
    """Download and parse info JSON file.

    Args:
        url: URL to the info JSON file
        dest: Destination path to save the file

    Returns:
        Parsed JSON content as dictionary

    Raises:
        requests.HTTPError: If download fails
        json.JSONDecodeError: If file is not valid JSON
    """
    logger.debug(f"Fetching info JSON from {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Save to disk
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(response.text)

    # Parse and return
    return json.loads(response.text)


def parse_output_paths(info_json: dict, base_url: str) -> dict[str, str]:
    """Extract file URLs from output_paths field in info JSON.

    Args:
        info_json: Parsed info JSON dictionary
        base_url: Base URL to resolve relative paths

    Returns:
        Dictionary mapping file types to URLs:
        - 'usage': URL to usage JSON
        - 'stdout': URL to stdout file
        - 'stderr': URL to stderr file
        - 'info': URL to info JSON
    """
    output_paths = info_json.get('output_paths', {})

    # Get base directory from info file URL
    parsed = urlparse(base_url)
    base_dir = '/'.join(parsed.path.split('/')[:-1])
    base_scheme_host = f"{parsed.scheme}://{parsed.netloc}"

    file_urls = {}
    for key in ['usage', 'stdout', 'stderr', 'info']:
        if key in output_paths:
            rel_path = output_paths[key]
            # Construct full URL
            if rel_path.startswith('http'):
                file_urls[key] = rel_path
            else:
                # Relative path - use only filename since base_dir already points to the directory
                from pathlib import Path as PathLib
                filename = PathLib(rel_path).name
                full_path = f"{base_dir}/{filename}"
                file_urls[key] = f"{base_scheme_host}{full_path}"

    return file_urls


def fetch_log_files(
    example: ExampleEntry,
    log_dir: Path,
    force: bool = False
) -> FetchedLog:
    """Download all log files for an example.

    Args:
        example: Example entry to fetch logs for
        log_dir: Base directory for storing logs
        force: If True, re-fetch even if files exist

    Returns:
        FetchedLog with paths to all downloaded files

    Raises:
        requests.HTTPError: If any download fails
    """
    # Create subdirectory for this example
    example_dir = log_dir / example.slug
    example_dir.mkdir(parents=True, exist_ok=True)

    # Define file paths
    info_path = example_dir / "example_output_info.json"
    usage_path = example_dir / "example_output_usage.json"
    stdout_path = example_dir / "example_output_stdout"
    stderr_path = example_dir / "example_output_stderr"

    # Check if files exist and skip if not forcing
    if not force and all(p.exists() for p in [info_path, usage_path, stdout_path, stderr_path]):
        logger.info(f"Using cached logs for '{example.title}'")
        return FetchedLog(info_path, usage_path, stdout_path, stderr_path)

    logger.info(f"Fetching logs for '{example.title}'")

    # Fetch and parse info JSON
    info_json = fetch_info_json(str(example.info_file), info_path)

    # Parse output_paths to get other file URLs
    file_urls = parse_output_paths(info_json, str(example.info_file))

    # Fetch usage, stdout, stderr
    if 'usage' in file_urls:
        response = requests.get(file_urls['usage'], timeout=30)
        response.raise_for_status()
        usage_path.write_text(response.text)
        logger.debug(f"  ├─ Downloaded usage.json")

    if 'stdout' in file_urls:
        response = requests.get(file_urls['stdout'], timeout=30)
        response.raise_for_status()
        stdout_path.write_text(response.text)
        logger.debug(f"  ├─ Downloaded stdout")

    if 'stderr' in file_urls:
        response = requests.get(file_urls['stderr'], timeout=30)
        response.raise_for_status()
        stderr_path.write_text(response.text)
        logger.debug(f"  └─ Downloaded stderr")

    return FetchedLog(info_path, usage_path, stdout_path, stderr_path)
