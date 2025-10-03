"""Contract tests for markdown output generation."""

import pytest


def test_slugify():
    """Test anchor slug generation."""
    from con_duct_gallery.generator import slugify

    assert slugify("con/duct Demo") == "con-duct-demo"
    assert slugify("Example 123") == "example-123"
    assert slugify("Test (2024)") == "test-2024"
    assert slugify("fMRIPrep 1.2.3") == "fmriprep-123"


def test_tag_index_generation():
    """Test tag index section with multiple tags."""
    from con_duct_gallery.generator import generate_tag_index
    from con_duct_gallery.models import ExampleEntry, ExampleRegistry

    entry_a = ExampleEntry(
        title="Example A",
        source_repo="https://github.com/test/a",
        info_file="https://example.com/a.json",
        tags=["tag1", "tag2"]
    )
    entry_b = ExampleEntry(
        title="Example B",
        source_repo="https://github.com/test/b",
        info_file="https://example.com/b.json",
        tags=["tag1"]
    )
    registry = ExampleRegistry(examples=[entry_a, entry_b])

    markdown = generate_tag_index(registry)

    assert "**tag1**: [Example A](#example-a), [Example B](#example-b)" in markdown
    assert "**tag2**: [Example A](#example-a)" in markdown


def test_example_section_with_plot():
    """Test individual example rendering with plot."""
    from con_duct_gallery.generator import generate_example_section
    from con_duct_gallery.models import ExampleEntry

    example = ExampleEntry(
        title="Test Example",
        source_repo="https://github.com/test/repo",
        info_file="https://example.com/info.json",
        tags=["demo"],
        description="Test description"
    )

    markdown = generate_example_section(example, svg_exists=True, log_dir="logs", image_dir="images")

    assert "### Test Example" in markdown
    assert "**Tags**: `demo`" in markdown
    assert "[github.com/test/repo](https://github.com/test/repo)" in markdown
    assert "Test description" in markdown
    assert "![Plot for Test Example](images/test-example.svg)" in markdown


def test_example_section_without_plot():
    """Test warning message for missing plot."""
    from con_duct_gallery.generator import generate_example_section
    from con_duct_gallery.models import ExampleEntry

    example = ExampleEntry(
        title="Test Example",
        source_repo="https://github.com/test/repo",
        info_file="https://example.com/info.json"
    )

    markdown = generate_example_section(example, svg_exists=False, log_dir="logs", image_dir="images")

    assert "⚠️" in markdown
    assert "Plot generation failed" in markdown or "not available" in markdown.lower()


def test_anchor_uniqueness():
    """Test that all anchors are unique."""
    from con_duct_gallery.generator import slugify

    titles = ["Example", "Example", "Different Example"]
    slugs = [slugify(t) for t in titles]

    # Slugs from same title should be identical
    assert slugs[0] == slugs[1]
    # Different titles should produce different slugs
    assert slugs[0] != slugs[2]


def test_header_section():
    """Test header with title, auto-update notice, timestamp."""
    from con_duct_gallery.generator import generate_header

    header = generate_header("2025-10-03 15:30 UTC")

    assert "# con/duct Examples Gallery" in header
    assert "🤖" in header
    assert "Automatically generated" in header or "auto" in header.lower()
    assert "2025-10-03 15:30 UTC" in header


def test_footer_section():
    """Test footer with maintenance instructions."""
    from con_duct_gallery.generator import generate_footer

    footer = generate_footer()

    assert "🛠️" in footer or "Maintenance" in footer
    assert "con-duct-gallery.yaml" in footer or "examples" in footer.lower()
    assert "GitHub Actions" in footer or "automatically" in footer.lower()
