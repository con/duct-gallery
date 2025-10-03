"""Main entry point for con-duct-gallery CLI."""

import logging
import sys
from pathlib import Path

from .cli import parse_args
from .models import ExampleRegistry
from .fetcher import fetch_log_files
from .plotter import generate_plot, should_regenerate_plot
from .generator import generate_gallery, slugify


def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 (success), 1 (config error), 2 (fetch error),
                  3 (plot error), 4 (file system error)
    """
    try:
        args = parse_args()
    except SystemExit as e:
        # argparse calls sys.exit() on error or --help
        return e.code if e.code is not None else 0

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Check for generate command
    if args.command != 'generate':
        logger.error("Please specify a command. Use 'generate' to create the gallery.")
        return 1

    try:
        # 1. Load and validate YAML configuration
        logger.info(f"Loading configuration from {args.config}")
        if not args.config.exists():
            logger.error(f"Configuration file not found: {args.config}")
            return 1

        try:
            registry = ExampleRegistry.from_yaml(args.config)
            logger.info(f"✓ Loaded {len(registry.examples)} examples")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return 1

        # Dry run mode
        if args.dry_run:
            logger.info(f"[DRY RUN] Would fetch logs for {len(registry.examples)} examples")
            logger.info(f"[DRY RUN] Would generate {len(registry.examples)} plots")
            logger.info(f"[DRY RUN] Would write {args.output}")
            return 0

        # 2. Process each example
        fetch_failures = 0
        plot_failures = 0
        example_log_paths = {}  # Store log paths for each example

        for example in registry.examples:
            try:
                # Fetch logs
                fetched_log = fetch_log_files(example, args.log_dir, args.force)

                # Store log paths for this example
                example_log_paths[example.title] = {
                    'info': fetched_log.info_json,
                    'usage': fetched_log.usage_json,
                    'stdout': fetched_log.stdout,
                    'stderr': fetched_log.stderr
                }

                # Generate plot if needed
                slug = slugify(example.title)
                svg_path = args.image_dir / f"{slug}.svg"

                if should_regenerate_plot(svg_path, fetched_log.usage_json, args.force):
                    try:
                        logger.info(f"Generating plot for '{example.title}'")
                        generate_plot(
                            fetched_log.usage_json,
                            svg_path,
                            example.plot_options
                        )
                        logger.info(f"  ✓ Plot saved: {svg_path}")
                    except Exception as e:
                        logger.warning(f"  ✗ Plot generation failed: {e}")
                        plot_failures += 1
                else:
                    logger.info(f"Using cached plot for '{example.title}'")

            except Exception as e:
                logger.warning(f"✗ Failed to fetch '{example.title}': {e}")
                fetch_failures += 1
                continue

        # Check if all examples failed
        if fetch_failures == len(registry.examples):
            logger.error("All examples failed to fetch")
            return 2

        # 3. Generate README.md
        logger.info("Generating markdown gallery")
        try:
            markdown = generate_gallery(registry, args.image_dir, example_log_paths)
        except Exception as e:
            logger.error(f"Failed to generate gallery: {e}")
            return 4

        # 4. Write output file
        try:
            args.output.write_text(markdown)
            logger.info(f"✓ Gallery written to {args.output}")

            # Summary
            successful = len(registry.examples) - fetch_failures
            num_tags = len(registry.get_all_tags())
            logger.info(f"✓ Generated gallery with {successful} examples, {num_tags} tags")

            if fetch_failures > 0:
                logger.warning(f"  {fetch_failures} examples failed to fetch")
            if plot_failures > 0:
                logger.warning(f"  {plot_failures} plots failed to generate")

        except Exception as e:
            logger.error(f"Failed to write output file: {e}")
            return 4

        return 0

    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
