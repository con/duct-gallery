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
