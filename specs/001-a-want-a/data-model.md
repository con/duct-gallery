# Data Model: con/duct Examples Gallery

**Phase**: 1 - Design & Contracts
**Date**: 2025-10-03

## Overview
This document defines the data entities and their relationships for the con/duct examples gallery.

## Core Entities

### 1. ExampleEntry
Represents a single con/duct usage example in the gallery.

**Fields**:
- `title` (str, required): Human-readable name (e.g., "con/duct Demo Example")
- `source_repo` (HttpUrl, required): GitHub/GitLab repository URL
- `info_file` (HttpUrl, required): URL to `*_info.json` file
- `tags` (list[str], optional): Categorization tags (e.g., ["synthetic", "medium-length"])
- `plot_options` (list[str], optional): Additional CLI args for `con-duct plot`
- `description` (str, optional): Markdown-formatted description

**Validation Rules**:
- `title`: Non-empty, max 100 characters
- `source_repo`: Valid HTTP(S) URL
- `info_file`: Valid HTTP(S) URL, must end with `.json`
- `tags`: Each tag lowercase alphanumeric + hyphens, no spaces
- `plot_options`: Each item non-empty string

**Derived Fields** (computed at runtime):
- `local_log_dir`: `logs/{slugified_title}/`
- `plot_svg_path`: `images/{slugified_title}.svg`
- `anchor_id`: `#{slugified_title}` for markdown links

**State**:
- Immutable after loading from YAML
- No persistence layer (YAML is source of truth)

### 2. ExampleRegistry
Collection of all examples, loaded from YAML configuration.

**Fields**:
- `examples` (list[ExampleEntry], required): All gallery examples

**Methods**:
- `from_yaml(path: Path) -> ExampleRegistry`: Load and validate YAML
- `get_all_tags() -> set[str]`: Extract unique tags across examples
- `filter_by_tag(tag: str) -> list[ExampleEntry]`: Examples with given tag

**Validation Rules**:
- At least one example required
- No duplicate titles (case-insensitive)

### 3. FetchedLog
Represents downloaded con/duct log files for an example.

**Fields**:
- `info_json` (Path): Local path to info file
- `usage_json` (Path): Local path to usage file
- `stdout` (Path): Local path to stdout file
- `stderr` (Path): Local path to stderr file

**Derived from**:
- Parsed from `output_paths` field in info JSON
- All paths relative to `local_log_dir`

**Validation**:
- All files must exist after fetch
- JSON files must parse successfully

### 4. GeneratedPlot
Represents a plot SVG generated from logs.

**Fields**:
- `svg_path` (Path): Location of generated SVG file
- `source_log` (Path): Usage JSON file used for plotting
- `options` (list[str]): con-duct plot options used
- `timestamp` (datetime): When plot was generated

**Validation**:
- SVG file must exist and be valid XML
- Size must be >0 bytes

### 5. GalleryMarkdown
The generated README.md structure.

**Sections**:
1. **Header**: Title, description, auto-update badge
2. **Tag Index**: For each tag, list of hyperlinked example titles
3. **Examples**: For each example, detailed section with:
   - Title (as heading)
   - Description
   - Tags
   - Source repository link
   - Embedded SVG plot
   - Metadata (last updated, log files)

**Anchor Links**:
- Tag index links to `#{example-anchor-id}`
- Anchor IDs follow GitHub slug rules (lowercase, hyphens, no special chars)

## Relationships

```
ExampleRegistry
    │
    ├──> ExampleEntry (1..N)
    │       ├──> FetchedLog (0..1)
    │       │       └──> usage_json, stdout, stderr, info_json
    │       └──> GeneratedPlot (0..1)
    │               └──> svg_path
    │
    └──> GalleryMarkdown (1)
            └──> Renders all ExampleEntry items
```

## Pydantic Model Definitions

### ExampleEntry
```python
from pydantic import BaseModel, HttpUrl, field_validator

class ExampleEntry(BaseModel):
    title: str
    source_repo: HttpUrl
    info_file: HttpUrl
    tags: list[str] = []
    plot_options: list[str] = []
    description: str = ""

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title must be ≤100 characters')
        return v

    @field_validator('tags')
    @classmethod
    def tags_lowercase_hyphenated(cls, v):
        for tag in v:
            if not tag.replace('-', '').isalnum():
                raise ValueError(f'Tag "{tag}" must be alphanumeric + hyphens')
        return [t.lower() for t in v]

    @property
    def slug(self) -> str:
        """GitHub-compatible anchor slug"""
        return self.title.lower().replace(' ', '-').replace('/', '-')
```

### ExampleRegistry
```python
class ExampleRegistry(BaseModel):
    examples: list[ExampleEntry]

    @field_validator('examples')
    @classmethod
    def no_duplicate_titles(cls, v):
        titles = [e.title.lower() for e in v]
        if len(titles) != len(set(titles)):
            raise ValueError('Duplicate titles found')
        return v

    @classmethod
    def from_yaml(cls, path: Path) -> 'ExampleRegistry':
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def get_all_tags(self) -> set[str]:
        tags = set()
        for ex in self.examples:
            tags.update(ex.tags)
        return tags
```

## File System Layout

```
logs/{example-slug}/
    ├── example_output_info.json
    ├── example_output_usage.json
    ├── example_output_stdout
    └── example_output_stderr

images/
    ├── {example-slug}.svg
    └── {another-example}.svg

con-duct-gallery.yaml
README.md
```

## Validation Strategy

1. **Load-time validation** (Pydantic):
   - YAML schema correctness
   - URL validity
   - Tag formatting

2. **Runtime validation**:
   - Network reachability (info_file URL)
   - JSON parsing (output_paths field)
   - File existence (after fetch)

3. **Generation validation**:
   - SVG file non-empty
   - Markdown anchor uniqueness
   - Link validity (internal refs)

## State Transitions

```
[YAML Config]
    → Load → [ExampleRegistry (in-memory)]
    → Fetch → [FetchedLog (on disk)]
    → Plot → [GeneratedPlot (SVG on disk)]
    → Generate → [GalleryMarkdown (README.md)]
```

No database, no state persistence. Idempotent operations based on file system state.
