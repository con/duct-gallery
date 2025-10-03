"""Contract tests for YAML schema validation."""

import pytest
from pydantic import ValidationError


def test_valid_yaml_loads():
    """Valid YAML with all fields should load without errors."""
    from con_duct_gallery.models import ExampleEntry, ExampleRegistry

    entry = ExampleEntry(
        title="Test Example",
        source_repo="https://github.com/test/repo",
        info_file="https://example.com/info.json",
        tags=["tag1", "tag2"],
        plot_options=["--option1"],
        description="Test description"
    )
    assert entry.title == "Test Example"
    assert len(entry.tags) == 2

    registry = ExampleRegistry(examples=[entry])
    assert len(registry.examples) == 1


def test_empty_title_rejected():
    """Empty title should raise ValidationError."""
    from con_duct_gallery.models import ExampleEntry

    with pytest.raises(ValidationError) as exc:
        ExampleEntry(
            title="",
            source_repo="https://github.com/test/repo",
            info_file="https://example.com/info.json"
        )
    assert "Title cannot be empty" in str(exc.value)


def test_title_too_long_rejected():
    """Title >100 characters should raise ValidationError."""
    from con_duct_gallery.models import ExampleEntry

    long_title = "a" * 101
    with pytest.raises(ValidationError) as exc:
        ExampleEntry(
            title=long_title,
            source_repo="https://github.com/test/repo",
            info_file="https://example.com/info.json"
        )
    assert "100 characters" in str(exc.value)


def test_tags_normalized_lowercase():
    """Tags should be converted to lowercase."""
    from con_duct_gallery.models import ExampleEntry

    entry = ExampleEntry(
        title="Test",
        source_repo="https://github.com/test/repo",
        info_file="https://example.com/info.json",
        tags=["Synthetic", "MEDIUM-length"]
    )
    assert entry.tags == ["synthetic", "medium-length"]


def test_invalid_tag_format_rejected():
    """Tags with spaces or underscores should raise ValidationError."""
    from con_duct_gallery.models import ExampleEntry

    with pytest.raises(ValidationError) as exc:
        ExampleEntry(
            title="Test",
            source_repo="https://github.com/test/repo",
            info_file="https://example.com/info.json",
            tags=["Has Spaces"]
        )
    assert "alphanumeric + hyphens" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        ExampleEntry(
            title="Test",
            source_repo="https://github.com/test/repo",
            info_file="https://example.com/info.json",
            tags=["under_score"]
        )
    assert "alphanumeric + hyphens" in str(exc.value)


def test_info_file_must_be_json():
    """info_file not ending in .json should raise ValidationError."""
    from con_duct_gallery.models import ExampleEntry

    with pytest.raises(ValidationError) as exc:
        ExampleEntry(
            title="Test",
            source_repo="https://github.com/test/repo",
            info_file="https://example.com/file.txt"
        )
    assert ".json" in str(exc.value)


def test_duplicate_titles_rejected():
    """Duplicate titles (case-insensitive) should raise ValidationError."""
    from con_duct_gallery.models import ExampleEntry, ExampleRegistry

    entry1 = ExampleEntry(
        title="Example",
        source_repo="https://github.com/test/repo1",
        info_file="https://example.com/info1.json"
    )
    entry2 = ExampleEntry(
        title="EXAMPLE",
        source_repo="https://github.com/test/repo2",
        info_file="https://example.com/info2.json"
    )

    with pytest.raises(ValidationError) as exc:
        ExampleRegistry(examples=[entry1, entry2])
    assert "Duplicate titles" in str(exc.value)


def test_at_least_one_example_required():
    """Empty examples list should raise ValidationError."""
    from con_duct_gallery.models import ExampleRegistry

    with pytest.raises(ValidationError) as exc:
        ExampleRegistry(examples=[])
    assert "At least one example" in str(exc.value)
