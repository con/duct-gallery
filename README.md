# con-duct-gallery

Automated markdown gallery generator for [con/duct](https://github.com/con/duct) usage examples.

## Overview

This project generates a beautiful, automatically-updated gallery of con/duct usage examples. Examples are configured in a YAML file, fetched from online sources (GitHub, DataLad), and rendered as markdown with embedded SVG plots.

## Features

- **Markdown-Native**: Pure markdown output, rendered by GitHub/GitLab
- **Automatic Updates**: Daily GitHub Actions workflow keeps gallery fresh
- **Incremental**: Caches logs and plots, only regenerates what changed
- **Tag-Based Navigation**: Browse examples by tags with anchor links
- **Reproducible**: All examples include source references

## Installation

### From Source

```bash
git clone https://github.com/con/con-duct-gallery.git
cd con-duct-gallery
pip install -e .
```

### Dependencies

- Python 3.11+
- [con-duct](https://github.com/con/duct): `pip install con-duct`

## Usage

### Quick Start

1. **Create configuration** (`con-duct-gallery.yaml`):

```yaml
examples:
  - title: "My Example"
    source_repo: "https://github.com/user/repo"
    info_file: "https://example.com/logs/output_info.json"
    tags:
      - tag1
      - tag2
    plot_options:
      - --style=seaborn
    description: "Description of this example"
```

2. **Generate gallery**:

```bash
con-duct-gallery generate
```

3. **View results**:

- `README.md`: Generated gallery (markdown)
- `images/`: SVG plot files
- `logs/`: Cached con/duct log files

### CLI Options

```bash
con-duct-gallery generate [OPTIONS]

Options:
  --config PATH        Configuration file (default: con-duct-gallery.yaml)
  --output PATH        Output markdown file (default: README.md)
  --log-dir PATH       Log cache directory (default: logs/)
  --image-dir PATH     Image output directory (default: images/)
  --force              Re-fetch and regenerate everything
  -v, --verbose        Enable detailed logging
  --dry-run            Show what would be done without executing
```

### Example: Force Regeneration

```bash
con-duct-gallery generate --force --verbose
```

## Configuration Schema

### Example Entry

```yaml
title: string                    # Required: unique name
source_repo: url                 # Required: GitHub/GitLab repo
info_file: url                   # Required: URL to *_info.json
tags:                            # Optional: list of tags
  - tag1
  - tag2
plot_options:                    # Optional: con-duct plot options
  - --option1
  - --option2
description: string              # Optional: markdown description
```

### Validation Rules

- **Title**: 1-100 characters, unique (case-insensitive)
- **Tags**: lowercase, alphanumeric + hyphens only
- **info_file**: Must end with `.json`

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=src/con_duct_gallery --cov-report=html

# Run specific test categories
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests only
```

### Project Structure

```
con-duct-gallery/
├── src/con_duct_gallery/    # Source code
│   ├── models.py             # Pydantic models
│   ├── fetcher.py            # Log file fetching
│   ├── plotter.py            # Plot generation
│   ├── generator.py          # Markdown generation
│   ├── cli.py                # CLI parsing
│   └── __main__.py           # Entry point
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── .github/workflows/        # GitHub Actions
├── con-duct-gallery.yaml     # Example configuration
└── pyproject.toml            # Project metadata
```

## Automation

### GitHub Actions

Two workflows are included:

1. **Daily Update** (`daily-update.yml`):
   - Runs daily at midnight UTC
   - Regenerates gallery
   - Commits changes if gallery updated

2. **PR Preview** (`pr-preview.yml`):
   - Triggered on PRs modifying config or code
   - Generates preview
   - Posts summary comment

### Manual Trigger

```bash
# Via GitHub UI: Actions → Daily Gallery Update → Run workflow
# Or via gh CLI:
gh workflow run daily-update.yml
```

## Contributing

1. Edit `con-duct-gallery.yaml` to add examples
2. Create pull request
3. PR preview workflow generates gallery preview
4. After merge, daily workflow keeps gallery updated

## License

[License information to be added]

## Credits

Built for the [con/duct](https://github.com/con/duct) project.
