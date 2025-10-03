# Markdown Output Contract

**Phase**: 1 - Design & Contracts
**Date**: 2025-10-03

## Generated README.md Structure

### Template Structure
```markdown
# con/duct Examples Gallery

> 🤖 Automatically generated gallery of con/duct usage examples
> Last updated: YYYY-MM-DD HH:MM UTC

## 📚 Browse by Tag

**tag1**: [Example A](#example-a), [Example B](#example-b)
**tag2**: [Example C](#example-c)
**tag3**: [Example A](#example-a), [Example C](#example-c)

## 📊 Examples

### Example A

**Tags**: `tag1` `tag3`
**Repository**: [github.com/repo/a](https://github.com/repo/a)

Description text here (if provided)

![Plot for Example A](images/example-a.svg)

<details>
<summary>📋 Metadata</summary>

- **Info file**: [example_output_info.json](logs/example-a/example_output_info.json)
- **Usage data**: [example_output_usage.json](logs/example-a/example_output_usage.json)
- **Standard output**: [stdout](logs/example-a/example_output_stdout)
- **Standard error**: [stderr](logs/example-a/example_output_stderr)
- **Plot options**: `--style=seaborn`, `--dpi=300`

</details>

---

### Example B

...

---

## 🛠️ Maintenance

This gallery is automatically updated daily via GitHub Actions.

- **Add an example**: Edit `con-duct-gallery.yaml` and create a pull request
- **Update plots**: Plots regenerate automatically when logs change
- **Force update**: Re-run the workflow with `workflow_dispatch`
```

## Specification

### Header Section
```markdown
# con/duct Examples Gallery

> 🤖 Automatically generated gallery of con/duct usage examples
> Last updated: YYYY-MM-DD HH:MM UTC
```

**Requirements**:
- H1 heading: "con/duct Examples Gallery"
- Blockquote with robot emoji (🤖) and auto-update notice
- Last updated timestamp in UTC (ISO 8601 format)

### Tag Index Section
```markdown
## 📚 Browse by Tag

**tag1**: [Example A](#example-a), [Example B](#example-b)
**tag2**: [Example C](#example-c)
**tag3**: [Example A](#example-a), [Example C](#example-c)
```

**Requirements**:
- H2 heading with books emoji (📚)
- One line per tag (alphabetically sorted)
- Tag name in bold, followed by colon
- Comma-separated list of example hyperlinks
- Links use GitHub anchor format: `[Title](#slug)`
- Anchors match slugified example titles (lowercase, hyphens)
- Two trailing spaces for markdown line break

### Examples Section
Each example rendered as:

```markdown
### Example Title

**Tags**: `tag1` `tag2`
**Repository**: [github.com/user/repo](https://github.com/user/repo)

Optional description paragraph(s) in markdown.

![Plot for Example Title](images/example-slug.svg)

<details>
<summary>📋 Metadata</summary>

- **Info file**: [example_output_info.json](logs/example-slug/example_output_info.json)
- **Usage data**: [example_output_usage.json](logs/example-slug/example_output_usage.json)
- **Standard output**: [stdout](logs/example-slug/example_output_stdout)
- **Standard error**: [stderr](logs/example-slug/example_output_stderr)
- **Plot options**: `--option1`, `--option2`

</details>

---
```

**Requirements**:
- H3 heading with example title (creates anchor)
- Tags line: bold "Tags" followed by inline code blocks
- Repository line: bold "Repository" with clickable link
- Description (if provided): Rendered as markdown
- Plot image: Alt text "Plot for {title}", relative path to SVG
- Collapsible metadata section using HTML `<details>`
- Metadata links: relative paths to log files
- Plot options: comma-separated list (if any specified)
- Horizontal rule (`---`) separator between examples

### Footer Section
```markdown
## 🛠️ Maintenance

This gallery is automatically updated daily via GitHub Actions.

- **Add an example**: Edit `con-duct-gallery.yaml` and create a pull request
- **Update plots**: Plots regenerate automatically when logs change
- **Force update**: Re-run the workflow with `workflow_dispatch`
```

**Requirements**:
- H2 heading with wrench emoji (🛠️)
- Maintenance instructions
- Markdown list with contribution guidance

## Anchor Slug Rules

GitHub anchor generation (simplified):
1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove special characters except hyphens
4. Remove leading/trailing hyphens

**Examples**:
- `"con/duct Demo Example"` → `#con-duct-demo-example`
- `"fMRIPrep 1.2.3"` → `#fmriprep-123`
- `"Test (2024)"` → `#test-2024`

**Implementation**:
```python
def slugify(title: str) -> str:
    """Convert title to GitHub-compatible anchor slug"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'[\s]+', '-', slug)    # Spaces to hyphens
    slug = slug.strip('-')                # Trim leading/trailing
    return slug
```

## Unicode Character Usage

**Allowed**:
- Emojis in headings: 📚 📊 🛠️ 🤖 📋 📦
- Box drawing: ├── └── │ ─
- Symbols: ✓ ✗ → ⚠️
- Math: ≤ ≥ ± ×

**Examples in context**:
```markdown
✓ Plot generated successfully
⚠️ Warning: con-duct not found
→ See documentation for details
```

## Error Handling

### Missing plot image:
```markdown
![Plot for Example](images/example.svg)

> ⚠️ Plot generation failed. See logs for details.
```

### Fetch failure:
Do not include example in generated gallery. Log warning to console.

### Partial metadata:
```markdown
<details>
<summary>📋 Metadata (partial)</summary>

- **Info file**: [example_output_info.json](logs/example/example_output_info.json)
- ⚠️ **Usage data**: Not available
- ⚠️ **Standard output**: Not available
- ⚠️ **Standard error**: Not available

</details>
```

## Validation Requirements

Generated README.md must:
1. Be valid GitHub Flavored Markdown
2. Have unique anchor IDs (no duplicates)
3. Have all internal links resolve (tag index → examples)
4. Reference existing image files
5. Reference existing log files (or mark as unavailable)
6. Be under 1MB file size
7. Render correctly on GitHub

## Testing Contract

**Unit tests** (`tests/unit/test_generator.py`):
```python
def test_slugify():
    """Test anchor slug generation"""
    assert slugify("con/duct Demo") == "con-duct-demo"
    assert slugify("Example 123") == "example-123"
    assert slugify("Test (2024)") == "test-2024"

def test_tag_index_generation():
    """Test tag index section"""
    examples = [
        ExampleEntry(title="A", tags=["tag1", "tag2"]),
        ExampleEntry(title="B", tags=["tag1"]),
    ]
    markdown = generate_tag_index(examples)
    assert "**tag1**: [A](#a), [B](#b)" in markdown
    assert "**tag2**: [A](#a)" in markdown

def test_example_section_with_plot():
    """Test individual example rendering"""
    example = ExampleEntry(
        title="Test Example",
        source_repo="https://github.com/test/repo",
        tags=["demo"],
        description="Test description"
    )
    markdown = generate_example_section(example, has_plot=True)
    assert "### Test Example" in markdown
    assert "![Plot for Test Example](images/test-example.svg)" in markdown

def test_missing_plot_warning():
    """Test warning for missing plots"""
    markdown = generate_example_section(example, has_plot=False)
    assert "⚠️ Plot generation failed" in markdown
```

**Integration tests** (`tests/integration/test_markdown_validity.py`):
```python
def test_generated_markdown_valid_gfm(tmp_path):
    """Generated markdown should be valid GFM"""
    # Generate README.md
    # Validate with markdown linter
    # Check all links resolve

def test_anchor_uniqueness(tmp_path):
    """All anchors should be unique"""
    # Generate README with duplicate-prone titles
    # Extract all anchor IDs
    # Assert no duplicates
```

## Example Output

See `quickstart.md` for complete generated example.
