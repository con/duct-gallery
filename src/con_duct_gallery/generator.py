"""Module for generating markdown gallery output."""

import re
from datetime import datetime
from pathlib import Path

from .models import ExampleEntry, ExampleRegistry


def slugify(title: str) -> str:
    """Convert title to GitHub-compatible anchor slug.

    Args:
        title: Example title

    Returns:
        Slugified title for use in anchor links
    """
    # Convert to lowercase
    slug = title.lower()
    # Replace slashes with hyphens (special case for paths like "con/duct")
    slug = slug.replace('/', '-')
    # Remove special characters except hyphens, spaces, and alphanumeric
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'[\s]+', '-', slug)
    # Collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def generate_header(timestamp: str) -> str:
    """Generate header section with title and auto-update notice.

    Args:
        timestamp: Last updated timestamp (e.g., "2025-10-03 15:30 UTC")

    Returns:
        Markdown header section
    """
    return f"""# con/duct Examples Gallery

> 🤖 Automatically generated gallery of con/duct usage examples
> Last updated: {timestamp}

"""


def generate_tag_index(registry: ExampleRegistry) -> str:
    """Generate tag index section with hyperlinks to examples.

    Args:
        registry: Example registry

    Returns:
        Markdown tag index section
    """
    lines = ["## 📚 Browse by Tag\n"]

    # Get all tags sorted alphabetically
    tags = sorted(registry.get_all_tags())

    for tag in tags:
        # Get examples with this tag
        examples = registry.filter_by_tag(tag)
        # Generate links
        links = [f"[{e.title}](#{slugify(e.title)})" for e in examples]
        line = f"**{tag}**: {', '.join(links)}"
        lines.append(line)

    lines.append("")  # Empty line after section
    return "\n".join(lines)


def generate_example_section(
    example: ExampleEntry,
    svg_exists: bool,
    log_paths: dict[str, Path],
    image_dir: str
) -> str:
    """Generate markdown section for a single example.

    Args:
        example: Example entry
        svg_exists: Whether SVG plot file exists
        log_paths: Dictionary with 'info', 'usage', 'stdout', 'stderr' paths
        image_dir: Directory containing image files

    Returns:
        Markdown section for the example
    """
    lines = [f"### {example.title}\n"]

    # Tags
    if example.tags:
        tag_badges = " ".join(f"`{tag}`" for tag in example.tags)
        lines.append(f"**Tags**: {tag_badges}")

    # Repository link (only if not empty)
    repo_url = str(example.source_repo)
    if repo_url:
        # Extract domain and path for display
        repo_display = repo_url.replace("https://", "").replace("http://", "").rstrip("/")
        lines.append(f"**Repository**: [{repo_display}]({repo_url})")

    lines.append("")  # Blank line

    # Description
    if example.description:
        lines.append(example.description)
        lines.append("")

    # Plot image or warning
    slug = slugify(example.title)
    if svg_exists:
        lines.append(f"![Plot for {example.title}]({image_dir}/{slug}.svg)")
    else:
        lines.append("> ⚠️ **Plot not available** - Generation failed or plot file missing")

    lines.append("")

    # Metadata details
    lines.append("<details>")
    lines.append("<summary>📋 Metadata</summary>")
    lines.append("")
    lines.append(f"- **Info file**: [example_output_info.json]({log_paths['info']})")
    lines.append(f"- **Usage data**: [example_output_usage.json]({log_paths['usage']})")
    lines.append(f"- **Standard output**: [stdout]({log_paths['stdout']})")
    lines.append(f"- **Standard error**: [stderr]({log_paths['stderr']})")

    if example.plot_options:
        options_str = ", ".join(f"`{opt}`" for opt in example.plot_options)
        lines.append(f"- **Plot options**: {options_str}")

    lines.append("")
    lines.append("</details>")
    lines.append("")

    return "\n".join(lines)


def generate_footer() -> str:
    """Generate footer section with maintenance instructions.

    Returns:
        Markdown footer section
    """
    return """## 🛠️ Maintenance

This gallery is automatically updated daily via GitHub Actions.

- **Add an example**: Edit `con-duct-gallery.yaml` and create a pull request
- **Update plots**: Plots regenerate automatically when logs change
- **Force update**: Re-run the workflow with `workflow_dispatch`
"""


def generate_gallery(
    registry: ExampleRegistry,
    image_dir: Path,
    example_log_paths: dict[str, dict[str, Path]]
) -> str:
    """Generate complete gallery markdown.

    Args:
        registry: Example registry
        image_dir: Directory containing image files
        example_log_paths: Dict mapping example titles to their log file paths
                          (each with 'info', 'usage', 'stdout', 'stderr' keys)

    Returns:
        Complete README.md markdown content
    """
    # Generate timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Build sections
    sections = []
    sections.append(generate_header(timestamp))
    sections.append(generate_tag_index(registry))
    sections.append("## 📊 Examples\n")

    # Generate section for each example
    for example in registry.examples:
        slug = slugify(example.title)
        svg_path = image_dir / f"{slug}.svg"
        svg_exists = svg_path.exists()

        # Get log paths for this example
        log_paths = example_log_paths.get(example.title, {})

        section = generate_example_section(
            example,
            svg_exists,
            log_paths=log_paths,
            image_dir=str(image_dir)
        )
        sections.append(section)
        sections.append("---\n")  # Separator

    sections.append(generate_footer())

    return "\n".join(sections)
