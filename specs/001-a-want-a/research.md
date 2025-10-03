# Research: con/duct Examples Gallery

**Phase**: 0 - Outline & Research
**Date**: 2025-10-03

## Overview
This document consolidates research findings for technical decisions in the con/duct examples gallery implementation.

## 1. Python Project Structure (Modern, 2024+)

**Decision**: Use `pyproject.toml` with `src/` layout and setuptools backend

**Rationale**:
- PEP 517/518 standardized build system
- `src/` layout prevents accidental imports from development directory
- `pyproject.toml` is the contemporary single-source configuration
- No `setup.py` needed for modern Python projects
- Compatible with editable installs (`pip install -e .`)

**Alternatives Considered**:
- Flat layout (package in root): Rejected - less safe, can import uninstalled code
- `setup.py` only: Rejected - deprecated pattern, pyproject.toml is standard
- Poetry: Rejected - adds dependency manager when pip suffices

**References**:
- PEP 517 (Build System)
- PEP 518 (pyproject.toml)
- Python Packaging User Guide 2024

## 2. YAML Schema Validation

**Decision**: Pydantic v2 for YAML schema validation

**Rationale**:
- Type-safe data validation with Python type hints
- Automatic JSON Schema generation
- Excellent error messages for invalid YAML
- Zero-cost abstractions (compiled with Rust)
- Native support for custom validators

**Alternatives Considered**:
- marshmallow: Rejected - more verbose, less type-safe
- dataclasses + manual validation: Rejected - requires custom validation logic
- JSON Schema + jsonschema library: Rejected - separate schema file, less Pythonic

**Dependencies**:
```
pydantic>=2.0
pyyaml>=6.0
```

## 3. HTTP Client for Fetching

**Decision**: `requests` library for HTTP fetching

**Rationale**:
- Battle-tested, stable API
- Synchronous is sufficient (GitHub rate limits prevent parallelism benefit)
- Simpler error handling than async
- Universal Python dependency

**Alternatives Considered**:
- httpx: Rejected - async unnecessary for this use case
- urllib (stdlib): Rejected - less ergonomic API
- aiohttp: Rejected - async adds complexity without benefit

**Dependencies**:
```
requests>=2.31
```

## 4. CLI Framework

**Decision**: Standard library `argparse`

**Rationale**:
- No external dependencies
- Sufficient for simple CLI: `con-duct-gallery generate [--force]`
- Native Python, well-documented
- Easy to test

**Alternatives Considered**:
- click: Rejected - external dependency for minimal CLI
- typer: Rejected - Pydantic integration nice but overkill
- fire: Rejected - magic behavior, harder to control

## 5. Testing Framework

**Decision**: pytest with pytest-cov for coverage

**Rationale**:
- Industry standard for Python testing
- Excellent fixtures and parametrization
- Plugin ecosystem (coverage, mocking)
- Clear, readable test code

**Dependencies**:
```
pytest>=7.4
pytest-cov>=4.1
```

## 6. con-duct Integration

**Decision**: Shell out to `con-duct plot` command via subprocess

**Rationale**:
- con-duct is CLI-first tool
- Subprocess isolation prevents version conflicts
- SVG output via `--output` flag
- Custom options pass-through via list of args

**Implementation Notes**:
```python
subprocess.run(['con-duct', 'plot', '--output', 'plot.svg', *custom_options, log_file])
```

**Alternatives Considered**:
- Import con-duct as library: Rejected - not designed as library, CLI is stable API
- Reimplement plotting: Rejected - violates DRY, hard to maintain

## 7. GitHub Actions Strategy

**Decision**: Two workflows - daily cron + PR preview

**Rationale**:
- Cron workflow: Fetch new examples, regenerate gallery, commit if changed
- PR workflow: Generate preview, post as comment for review
- Separate workflows for different triggers/permissions

**Workflow Details**:

### daily-update.yml
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Manual trigger
```
- Checks out repo
- Installs Python + dependencies
- Runs `con-duct-gallery generate`
- Commits changes if README.md or images/ modified
- Pushes to main

### pr-preview.yml
```yaml
on:
  pull_request:
    paths:
      - 'examples.yaml'
      - 'src/**'
```
- Generates gallery in PR context
- Posts preview comment with diff
- Does NOT commit (preview only)

## 8. Unicode Characters

**Decision**: Use unicode box drawing + symbols for visual enhancement

**Examples**:
- Tags: `🏷️ neuroimaging`, `🏷️ synthetic`
- Links: `📦 Repository`, `📊 Plot`
- Status: `✅ Updated`, `⚠️ Stale`
- Structure: `├──`, `└──` for file trees

**Rationale**:
- GitHub renders unicode correctly
- Enhances readability without HTML
- Maintains plain-text accessibility

## 9. Incremental Updates Strategy

**Decision**: Check file existence + modification time

**Rationale**:
- If log files exist locally: skip fetch (unless --force)
- If SVG plot exists and newer than log: skip generation
- Always regenerate README.md (cheap operation)

**Implementation**:
```python
def should_fetch(example):
    return args.force or not log_exists(example)

def should_plot(example):
    return args.force or not (plot_exists(example) and plot_newer_than_log(example))
```

## 10. YAML Schema Design

**Decision**: Flat list of examples with embedded metadata

**Schema**:
```yaml
examples:
  - title: "con/duct Demo Example"
    source_repo: "https://github.com/con/duct/"
    info_file: "https://raw.githubusercontent.com/.../example_output_info.json"
    tags:
      - synthetic
      - medium-length
    plot_options:
      - --style=seaborn
```

**Rationale**:
- Simple, human-editable
- Pydantic validates on load
- Easy to add examples manually
- Source of truth for gallery content

## 11. Error Handling Strategy

**Decision**: Fail-fast with detailed error messages, log partial failures

**Rationale**:
- Invalid YAML → immediate exit with Pydantic error
- Network errors → log warning, skip example, continue
- Plot generation failure → log error, mark example as broken
- README always generated (even if some examples fail)

## 12. Git Workflow

**Decision**: Commit generated files (README.md, images/) to main branch

**Rationale**:
- GitHub renders directly (no build step)
- History tracks gallery evolution
- Diff shows what changed per update
- Aligns with Markdown-Native principle

**.gitignore**:
```
logs/              # Fetched con/duct logs (large, reproducible)
__pycache__/
*.pyc
.pytest_cache/
.coverage
dist/
*.egg-info/
```

**Committed**:
```
README.md          # Generated gallery
images/            # SVG plots
examples.yaml      # Source of truth
```

## Summary of Technical Stack

| Component | Choice | Version |
|-----------|--------|---------|
| Language | Python | 3.11+ |
| Build | pyproject.toml | PEP 517/518 |
| Validation | Pydantic | 2.0+ |
| HTTP | requests | 2.31+ |
| CLI | argparse | stdlib |
| Testing | pytest | 7.4+ |
| Coverage | pytest-cov | 4.1+ |
| Plotting | con-duct CLI | subprocess |
| CI/CD | GitHub Actions | cron + PR |
| Markdown | GFM + unicode | N/A |

## Open Questions Resolved

All technical unknowns from Technical Context section have been researched and decided. No NEEDS CLARIFICATION markers remain.
