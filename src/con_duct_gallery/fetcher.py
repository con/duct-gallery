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


def fetch_info_json(url_or_path: str, dest: Path, repo_root: Path = None) -> dict:
    """Download and parse info JSON file or read from local path.

    Args:
        url_or_path: URL to the info JSON file or local file path
        dest: Destination path to save the file
        repo_root: Repository root path for resolving local paths (defaults to cwd)

    Returns:
        Parsed JSON content as dictionary

    Raises:
        requests.HTTPError: If download fails
        json.JSONDecodeError: If file is not valid JSON
        FileNotFoundError: If local file does not exist
    """
    # Check if it's a local path or URL
    if url_or_path.startswith('http'):
        # Remote URL - download it
        logger.debug(f"Fetching info JSON from {url_or_path}")
        response = requests.get(url_or_path, timeout=30)
        response.raise_for_status()

        # Save to disk
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(response.text)

        # Parse and return
        return json.loads(response.text)
    else:
        # Local file path
        if repo_root is None:
            repo_root = Path.cwd()

        source_path = repo_root / url_or_path
        logger.debug(f"Reading info JSON from local path {source_path}")

        if not source_path.exists():
            raise FileNotFoundError(f"Local info file not found: {source_path}")

        # Read and parse
        content = source_path.read_text()

        # Save to destination
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)

        return json.loads(content)


def parse_output_paths(info_json: dict, base_url_or_path: str, repo_root: Path = None) -> dict[str, str]:
    """Extract file URLs/paths from output_paths field in info JSON.

    Args:
        info_json: Parsed info JSON dictionary
        base_url_or_path: Base URL or local file path to resolve relative paths
        repo_root: Repository root path for local files (defaults to cwd)

    Returns:
        Dictionary mapping file types to URLs or local paths:
        - 'usage': URL/path to usage JSON
        - 'stdout': URL/path to stdout file
        - 'stderr': URL/path to stderr file
        - 'info': URL/path to info JSON
    """
    output_paths = info_json.get('output_paths', {})

    # Check if base is a local path or URL
    if base_url_or_path.startswith('http'):
        # Remote URL case
        parsed = urlparse(base_url_or_path)
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
    else:
        # Local path case
        if repo_root is None:
            repo_root = Path.cwd()

        base_path = repo_root / base_url_or_path
        base_dir = base_path.parent

        file_urls = {}
        for key in ['usage', 'stdout', 'stderr', 'info']:
            if key in output_paths:
                rel_path = output_paths[key]
                # Resolve relative to the directory containing the info file
                if Path(rel_path).is_absolute():
                    file_urls[key] = rel_path
                else:
                    # Relative path - resolve from base directory
                    file_urls[key] = str(base_dir / Path(rel_path).name)

    return file_urls


def fetch_log_files(
    example: ExampleEntry,
    log_dir: Path,
    force: bool = False,
    repo_root: Path = None
) -> FetchedLog:
    """Download all log files for an example or copy from local paths.

    Args:
        example: Example entry to fetch logs for
        log_dir: Base directory for storing logs
        force: If True, re-fetch even if files exist
        repo_root: Repository root path for local files (defaults to cwd)

    Returns:
        FetchedLog with paths to all downloaded files

    Raises:
        requests.HTTPError: If any download fails
        FileNotFoundError: If local file does not exist
    """
    if repo_root is None:
        repo_root = Path.cwd()

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

    # Fetch and parse info JSON (handles both remote and local)
    info_json = fetch_info_json(str(example.info_file), info_path, repo_root)

    # Parse output_paths to get other file URLs/paths
    file_paths = parse_output_paths(info_json, str(example.info_file), repo_root)

    # Check if we're working with local or remote files
    is_local = example.is_local

    # Fetch/copy usage, stdout, stderr
    if 'usage' in file_paths:
        if is_local:
            source = Path(file_paths['usage'])
            if not source.exists():
                raise FileNotFoundError(f"Local usage file not found: {source}")
            usage_path.write_text(source.read_text())
            logger.debug(f"  ├─ Copied usage.json from local")
        else:
            response = requests.get(file_paths['usage'], timeout=30)
            response.raise_for_status()
            usage_path.write_text(response.text)
            logger.debug(f"  ├─ Downloaded usage.json")

    if 'stdout' in file_paths:
        if is_local:
            source = Path(file_paths['stdout'])
            if not source.exists():
                raise FileNotFoundError(f"Local stdout file not found: {source}")
            stdout_path.write_text(source.read_text())
            logger.debug(f"  ├─ Copied stdout from local")
        else:
            response = requests.get(file_paths['stdout'], timeout=30)
            response.raise_for_status()
            stdout_path.write_text(response.text)
            logger.debug(f"  ├─ Downloaded stdout")

    if 'stderr' in file_paths:
        if is_local:
            source = Path(file_paths['stderr'])
            if not source.exists():
                raise FileNotFoundError(f"Local stderr file not found: {source}")
            stderr_path.write_text(source.read_text())
            logger.debug(f"  └─ Copied stderr from local")
        else:
            response = requests.get(file_paths['stderr'], timeout=30)
            response.raise_for_status()
            stderr_path.write_text(response.text)
            logger.debug(f"  └─ Downloaded stderr")

    return FetchedLog(info_path, usage_path, stdout_path, stderr_path)
