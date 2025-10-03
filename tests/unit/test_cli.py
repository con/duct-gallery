"""Contract tests for CLI argument parsing."""

import pytest
from pathlib import Path


def test_cli_defaults():
    """Test default argument values."""
    from con_duct_gallery.cli import parse_args

    args = parse_args(['generate'])
    assert args.config == Path('con-duct-gallery.yaml')
    assert args.output == Path('README.md')
    assert args.log_dir == Path('logs')
    assert args.image_dir == Path('images')
    assert args.force is False
    assert args.verbose is False
    assert args.dry_run is False


def test_cli_force_flag():
    """Test --force flag sets force=True."""
    from con_duct_gallery.cli import parse_args

    args = parse_args(['generate', '--force'])
    assert args.force is True


def test_cli_custom_paths():
    """Test custom path arguments."""
    from con_duct_gallery.cli import parse_args

    args = parse_args([
        'generate',
        '--config', 'custom.yaml',
        '--output', 'GALLERY.md',
        '--log-dir', 'cache/',
        '--image-dir', 'plots/'
    ])
    assert args.config == Path('custom.yaml')
    assert args.output == Path('GALLERY.md')
    assert args.log_dir == Path('cache/')
    assert args.image_dir == Path('plots/')


def test_cli_verbose_flag():
    """Test -v/--verbose enables verbose mode."""
    from con_duct_gallery.cli import parse_args

    args_short = parse_args(['generate', '-v'])
    assert args_short.verbose is True

    args_long = parse_args(['generate', '--verbose'])
    assert args_long.verbose is True


def test_cli_dry_run():
    """Test --dry-run sets dry_run=True."""
    from con_duct_gallery.cli import parse_args

    args = parse_args(['generate', '--dry-run'])
    assert args.dry_run is True


def test_cli_no_subcommand_shows_error():
    """Test that running without subcommand shows usage and exits with error."""
    from con_duct_gallery.cli import parse_args

    with pytest.raises(SystemExit) as exc_info:
        parse_args([])

    assert exc_info.value.code == 2  # argparse uses exit code 2 for errors


def test_cli_help_exits_cleanly():
    """Test that --help exits with code 0."""
    from con_duct_gallery.cli import parse_args

    with pytest.raises(SystemExit) as exc_info:
        parse_args(['--help'])

    assert exc_info.value.code == 0


def test_cli_generate_help_exits_cleanly():
    """Test that generate --help exits with code 0."""
    from con_duct_gallery.cli import parse_args

    with pytest.raises(SystemExit) as exc_info:
        parse_args(['generate', '--help'])

    assert exc_info.value.code == 0


def test_main_handles_missing_subcommand():
    """Test that main() handles missing subcommand gracefully."""
    from con_duct_gallery.__main__ import main
    import sys
    from unittest.mock import patch

    # Mock sys.argv to simulate no arguments
    with patch.object(sys, 'argv', ['con-duct-gallery']):
        exit_code = main()
        assert exit_code == 2  # argparse error code


def test_main_handles_help_flag():
    """Test that main() returns 0 for --help."""
    from con_duct_gallery.__main__ import main
    import sys
    from unittest.mock import patch

    with patch.object(sys, 'argv', ['con-duct-gallery', '--help']):
        exit_code = main()
        assert exit_code == 0
