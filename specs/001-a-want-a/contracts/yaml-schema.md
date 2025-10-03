# YAML Configuration Schema Contract

**Phase**: 1 - Design & Contracts
**Date**: 2025-10-03

## Schema Definition

### Root Structure
```yaml
examples:
  - <ExampleEntry>
  - <ExampleEntry>
  ...
```

### ExampleEntry Schema
```yaml
title: string                    # REQUIRED: Human-readable name
source_repo: url                 # REQUIRED: GitHub/GitLab repo URL
info_file: url                   # REQUIRED: URL to *_info.json
tags:                            # OPTIONAL: List of tags
  - string
  - string
plot_options:                    # OPTIONAL: Additional con-duct plot args
  - string
  - string
description: string              # OPTIONAL: Markdown description
```

## Field Specifications

### `title` (required)
- **Type**: string
- **Constraints**:
  - Non-empty after stripping whitespace
  - Maximum 100 characters
  - Must be unique within configuration (case-insensitive)
- **Examples**:
  - ✅ `"con/duct Demo Example"`
  - ✅ `"fMRIPrep 1.2.3 Processing"`
  - ❌ `""` (empty)
  - ❌ `"a" * 101` (too long)

### `source_repo` (required)
- **Type**: URL (http/https)
- **Constraints**:
  - Valid HTTP(S) URL
  - Typically GitHub/GitLab repository
- **Examples**:
  - ✅ `"https://github.com/con/duct/"`
  - ✅ `"https://gitlab.com/user/project"`
  - ❌ `"github.com/user/repo"` (missing protocol)
  - ❌ `"not-a-url"` (invalid URL)

### `info_file` (required)
- **Type**: URL (http/https)
- **Constraints**:
  - Valid HTTP(S) URL
  - Must end with `.json`
  - Should point to con/duct info file (contains `output_paths` field)
- **Examples**:
  - ✅ `"https://raw.githubusercontent.com/.../example_output_info.json"`
  - ❌ `"https://example.com/file.txt"` (not .json)

### `tags` (optional, default: [])
- **Type**: list of strings
- **Constraints**:
  - Each tag: lowercase alphanumeric + hyphens only
  - No spaces, underscores, or special characters
  - Automatically lowercased during validation
- **Examples**:
  - ✅ `["synthetic", "medium-length", "neuroimaging"]`
  - ✅ `[]` (empty list)
  - ❌ `["Has Spaces"]` (spaces not allowed)
  - ❌ `["under_score"]` (underscores not allowed)

### `plot_options` (optional, default: [])
- **Type**: list of strings
- **Constraints**:
  - Each item non-empty string
  - Passed directly to `con-duct plot` command
- **Examples**:
  - ✅ `["--style=seaborn", "--dpi=300"]`
  - ✅ `[]` (use con-duct defaults)
  - ✅ `["--xlabel", "Time (s)"]` (multi-argument options)

### `description` (optional, default: "")
- **Type**: string (markdown)
- **Constraints**:
  - GitHub Flavored Markdown
  - Keep concise (renders in gallery)
- **Examples**:
  - ✅ `"Demo example from con/duct repository"`
  - ✅ `"Processing run on **HPC cluster** with 48 cores"`

## Complete Example

```yaml
examples:
  - title: "con/duct Demo Example"
    source_repo: "https://github.com/con/duct/"
    info_file: "https://raw.githubusercontent.com/con/duct/a539c3e20cccd4455a75cd7bfbae9cd644cdcbff/demo/example_output_info.json"
    tags:
      - synthetic
      - medium-length
    plot_options:
      - --style=seaborn
    description: "Synthetic demo from the con/duct repository"

  - title: "fMRIPrep Processing"
    source_repo: "https://github.com/nipreps/fmriprep/"
    info_file: "https://example.com/fmriprep_logs/output_info.json"
    tags:
      - neuroimaging
      - fmriprep
      - real-world
    description: |
      Real-world fMRIPrep run on **OpenNeuro dataset ds000114**.
      Processing time: ~3 hours on 16-core machine.

  - title: "Quick Test Run"
    source_repo: "https://github.com/con/duct/"
    info_file: "https://example.com/test_run_info.json"
    # Minimal example with defaults
```

## Validation Rules

### Pydantic Model
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
    def validate_title(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title must be ≤100 characters')
        return v

    @field_validator('info_file')
    @classmethod
    def validate_info_file(cls, v):
        if not str(v).endswith('.json'):
            raise ValueError('info_file must end with .json')
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        validated = []
        for tag in v:
            tag_lower = tag.lower()
            if not tag_lower.replace('-', '').isalnum():
                raise ValueError(
                    f'Tag "{tag}" must be alphanumeric + hyphens only'
                )
            validated.append(tag_lower)
        return validated

class ExampleRegistry(BaseModel):
    examples: list[ExampleEntry]

    @field_validator('examples')
    @classmethod
    def no_duplicate_titles(cls, v):
        titles_lower = [e.title.lower() for e in v]
        if len(titles_lower) != len(set(titles_lower)):
            duplicates = [t for t in titles_lower if titles_lower.count(t) > 1]
            raise ValueError(f'Duplicate titles found: {duplicates}')
        if not v:
            raise ValueError('At least one example required')
        return v
```

## Error Messages

### Invalid YAML syntax:
```
Error: Invalid YAML syntax in examples.yaml:
  Line 5: mapping values are not allowed here
```

### Validation errors:
```
Error: Validation failed for examples.yaml:
  examples[0].title: Title cannot be empty
  examples[1].tags[0]: Tag "Has Spaces" must be alphanumeric + hyphens only
  examples[2].info_file: info_file must end with .json
```

### Duplicate titles:
```
Error: Validation failed for examples.yaml:
  examples: Duplicate titles found: ['demo example']
```

## Testing Contract

**Unit tests** (`tests/unit/test_models.py`):
```python
def test_valid_yaml_loads():
    """Valid YAML should load without errors"""
    yaml_str = """
    examples:
      - title: "Test"
        source_repo: "https://github.com/test/repo"
        info_file: "https://example.com/info.json"
    """
    registry = ExampleRegistry.from_yaml_string(yaml_str)
    assert len(registry.examples) == 1
    assert registry.examples[0].title == "Test"

def test_empty_title_rejected():
    """Empty title should raise ValidationError"""
    with pytest.raises(ValidationError) as exc:
        ExampleEntry(title="", source_repo="https://github.com/a/b", ...)
    assert "Title cannot be empty" in str(exc.value)

def test_tags_normalized_to_lowercase():
    """Tags should be converted to lowercase"""
    entry = ExampleEntry(
        title="Test",
        tags=["Synthetic", "MEDIUM-length"],
        ...
    )
    assert entry.tags == ["synthetic", "medium-length"]

def test_duplicate_titles_rejected():
    """Duplicate titles (case-insensitive) should raise error"""
    with pytest.raises(ValidationError) as exc:
        ExampleRegistry(examples=[
            ExampleEntry(title="Example", ...),
            ExampleEntry(title="EXAMPLE", ...),
        ])
    assert "Duplicate titles" in str(exc.value)
```

## Migration Path

If schema changes in future:
1. Add new optional fields (backward compatible)
2. Deprecate old fields with warnings
3. Provide migration script
4. Version schema in YAML (optional `schema_version: 1`)

Current version: **1.0** (implicit, no version field needed)
