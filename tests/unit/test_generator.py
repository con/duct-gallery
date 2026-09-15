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
    """Test tag index section with multiple tags as subsections."""
    from con_duct_gallery.generator import generate_tag_index
    from con_duct_gallery.models import ExampleEntry, ExampleRegistry, PlotVariant

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
    registry = ExampleRegistry(
        examples=[entry_a, entry_b], variants=[PlotVariant(name="only")]
    )

    markdown = generate_tag_index(registry)

    # Check for subsection headers
    assert "#### tag1" in markdown
    assert "#### tag2" in markdown

    # Check for example links under tags
    assert "[Example A](#example-a), [Example B](#example-b)" in markdown
    assert "[Example A](#example-a)" in markdown


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


def _variant_fixture():
    from pathlib import Path
    from con_duct_gallery.models import ExampleEntry, PlotVariant

    example = ExampleEntry(
        title="Test Example",
        source_repo="https://github.com/test/repo",
        info_file="https://example.com/info.json",
        tags=["demo"],
        description="Test description",
    )
    variants = [
        PlotVariant(name="ps-pcpu", label="ps pcpu (raw)", plot_options=["--cpu", "ps-pcpu"]),
        PlotVariant(name="ps-cpu-timepoint", plot_options=["--cpu", "ps-cpu-timepoint"]),
    ]
    log_paths = {
        'info': Path('logs/test-example/example_output_info.json'),
        'usage': Path('logs/test-example/example_output_usage.json'),
        'stdout': Path('logs/test-example/example_output_stdout'),
        'stderr': Path('logs/test-example/example_output_stderr')
    }
    return example, variants, log_paths


def test_example_section_with_variants():
    """An example renders its header, then one <img> per variant in a table."""
    from con_duct_gallery.generator import generate_example_section

    example, variants, log_paths = _variant_fixture()

    markdown = generate_example_section(
        example, log_paths=log_paths, image_dir="images",
        variants=variants,
        variant_svg_exists={"ps-pcpu": True, "ps-cpu-timepoint": True},
    )

    assert "### Test Example" in markdown
    assert "**Tags**: [`demo`](#demo)" in markdown
    assert "[github.com/test/repo](https://github.com/test/repo)" in markdown
    assert "Test description" in markdown
    assert "<table>" in markdown
    assert '<th align="center">ps pcpu (raw)</th>' in markdown
    assert '<th align="center">ps-cpu-timepoint</th>' in markdown  # label falls back to name
    assert 'src="images/test-example__ps-pcpu.svg"' in markdown
    assert 'src="images/test-example__ps-cpu-timepoint.svg"' in markdown


def test_example_section_variant_missing_svg():
    """A variant whose SVG is missing gets a warning cell, the others still render."""
    from con_duct_gallery.generator import generate_example_section

    example, variants, log_paths = _variant_fixture()

    markdown = generate_example_section(
        example, log_paths=log_paths, image_dir="images",
        variants=variants,
        variant_svg_exists={"ps-pcpu": True},
    )

    assert 'src="images/test-example__ps-pcpu.svg"' in markdown
    assert "test-example__ps-cpu-timepoint.svg" not in markdown
    assert "Plot not available" in markdown


def test_example_section_single_variant_is_one_column():
    """A single variant is the same table with one column, not a special case."""
    from con_duct_gallery.generator import generate_example_section

    example, variants, log_paths = _variant_fixture()

    markdown = generate_example_section(
        example, log_paths=log_paths, image_dir="images",
        variants=variants[:1],
        variant_svg_exists={"ps-pcpu": True},
    )

    assert markdown.count("<th ") == 1
    assert 'src="images/test-example__ps-pcpu.svg"' in markdown


def test_reading_guide_lists_variant_descriptions():
    """The guide has one bullet per variant, description included when given."""
    from con_duct_gallery.generator import generate_reading_guide
    from con_duct_gallery.models import PlotVariant

    variants = [
        PlotVariant(name="raw", label="Raw", description="As sampled."),
        PlotVariant(name="est"),
    ]

    guide = generate_reading_guide(variants)

    assert guide.startswith("## 📖 Reading the plots")
    assert "- **Raw**: As sampled." in guide
    assert "- **est**\n" in guide


