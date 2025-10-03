"""Pydantic models for con/duct examples gallery configuration."""

import re
from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, HttpUrl, field_validator


class ExampleEntry(BaseModel):
    """Represents a single con/duct usage example in the gallery."""

    title: str
    source_repo: HttpUrl
    info_file: HttpUrl
    tags: list[str] = []
    plot_options: list[str] = []
    description: str = ""

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is non-empty and under 100 characters."""
        v = v.strip()
        if not v:
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title must be ≤100 characters')
        return v

    @field_validator('info_file')
    @classmethod
    def validate_info_file(cls, v: HttpUrl) -> HttpUrl:
        """Validate info_file ends with .json."""
        if not str(v).endswith('.json'):
            raise ValueError('info_file must end with .json')
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate tags are lowercase alphanumeric + hyphens only."""
        validated = []
        for tag in v:
            tag_lower = tag.lower()
            # Check alphanumeric + hyphens only
            if not tag_lower.replace('-', '').isalnum():
                raise ValueError(
                    f'Tag "{tag}" must be alphanumeric + hyphens only'
                )
            validated.append(tag_lower)
        return validated

    @property
    def slug(self) -> str:
        """Generate GitHub-compatible anchor slug from title."""
        # Convert to lowercase
        slug = self.title.lower()
        # Remove special characters except hyphens and alphanumeric
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace spaces with hyphens
        slug = re.sub(r'[\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug


class ExampleRegistry(BaseModel):
    """Collection of all examples, loaded from YAML configuration."""

    examples: list[ExampleEntry]

    @field_validator('examples')
    @classmethod
    def validate_examples(cls, v: list[ExampleEntry]) -> list[ExampleEntry]:
        """Validate at least one example and no duplicate titles."""
        if not v:
            raise ValueError('At least one example required')

        # Check for duplicate titles (case-insensitive)
        titles_lower = [e.title.lower() for e in v]
        if len(titles_lower) != len(set(titles_lower)):
            duplicates = [t for t in titles_lower if titles_lower.count(t) > 1]
            unique_dupes = list(set(duplicates))
            raise ValueError(f'Duplicate titles found: {unique_dupes}')

        return v

    @classmethod
    def from_yaml(cls, path: Path) -> 'ExampleRegistry':
        """Load and validate registry from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def get_all_tags(self) -> set[str]:
        """Extract unique tags across all examples."""
        tags = set()
        for example in self.examples:
            tags.update(example.tags)
        return tags

    def filter_by_tag(self, tag: str) -> list[ExampleEntry]:
        """Get examples with the specified tag."""
        return [e for e in self.examples if tag in e.tags]
