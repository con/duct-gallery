"""CLI argument parsing for con-duct-gallery."""

import argparse
from pathlib import Path


def parse_args(args: list[str] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: List of arguments (if None, uses sys.argv)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog='con-duct-gallery',
        description='Generate markdown gallery of con/duct examples'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate subcommand
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate the gallery README.md and plot images'
    )

    generate_parser.add_argument(
        '--config',
        type=Path,
        default=Path('con-duct-gallery.yaml'),
        help='Path to YAML configuration file (default: con-duct-gallery.yaml)'
    )

    generate_parser.add_argument(
        '--output',
        type=Path,
        default=Path('README.md'),
        help='Path for generated markdown file (default: README.md)'
    )

    generate_parser.add_argument(
        '--log-dir',
        type=Path,
        default=Path('logs'),
        help='Directory for cached log files (default: logs/)'
    )

    generate_parser.add_argument(
        '--image-dir',
        type=Path,
        default=Path('images'),
        help='Directory for generated SVG plots (default: images/)'
    )

    generate_parser.add_argument(
        '--force',
        action='store_true',
        help='Re-fetch logs and regenerate plots even if cached'
    )

    generate_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable detailed logging'
    )

    generate_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without executing'
    )

    return parser.parse_args(args)
