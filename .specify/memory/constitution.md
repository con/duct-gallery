<!--
Sync Impact Report
==================
Version: 1.0.0 → 2.0.0 (MAJOR: Markdown-native architecture)
Ratification Date: 2025-10-03
Last Amended: 2025-10-03

Changes:
- BREAKING: Removed Static-First principle (HTML/CSS/JS generation)
- BREAKING: Replaced with Markdown-Native principle (GitHub/GitLab rendering)
- BREAKING: Updated Technical Constraints to remove web-specific requirements
- Updated Minimalist Interface to reflect markdown-only approach
- Removed browser support, performance, and mobile-first web constraints
- Added markdown-specific constraints (CommonMark, image formats, file organization)

Principles Modified:
- III. Minimalist Interface: Now specifies markdown structure (headers, lists, images, links only)
- IV. Markdown-Native (was Static-First): Generate markdown files only, rely on Git platform rendering

Principles Removed:
- None (replaced Static-First with Markdown-Native)

Templates Status:
✅ plan-template.md: Constitution Check section references this document
✅ spec-template.md: Requirements align with markdown gallery focus
✅ tasks-template.md: Task patterns support markdown generation workflows
✅ agent-file-template.md: Compatible with markdown-only approach

Follow-up TODOs:
- None - All placeholders resolved
-->

# con-duct-gallery Constitution

## Core Principles

### I. Content-First
The gallery exists to showcase examples and plots, not to demonstrate web technology features. Every design decision MUST prioritize content visibility and clarity. Interface elements that do not directly serve content discovery or viewing are prohibited. Content legibility takes precedence over aesthetic experimentation.

**Rationale**: Users visit to see examples and plots, not the website itself. Any visual complexity that draws attention away from the gallery content defeats the purpose.

### II. Automatic Updates
Content updates MUST occur without manual intervention. The system MUST detect new or modified examples and regenerate the gallery automatically. Manual content deployment steps are prohibited in production workflows.

**Rationale**: A manually-updated gallery becomes stale and unmaintained. Automation ensures the gallery reflects the current state of available examples without human bottlenecks.

### III. Minimalist Interface
Markdown files MUST use minimal structure: headers, lists, images, and links only. No HTML embeds, custom styling, or complex tables unless absolutely necessary for content comprehension. Use standard markdown features that render consistently across GitHub, GitLab, and other Git platforms.

**Rationale**: Markdown's constraint is its strength. Simple markdown renders predictably everywhere, ages gracefully, and remains readable as plain text. Complex markdown defeats the purpose of avoiding HTML.

### IV. Markdown-Native
Generate markdown files ONLY. No HTML, CSS, or JavaScript generation. Rely on Git platform rendering (GitHub, GitLab, Gitea, etc.) for display. The gallery is a collection of `.md` files organized in directories, viewable directly in any Git web interface or markdown viewer.

**Rationale**: Markdown files require no build process, no web hosting, no dependencies. They're version-controlled content that renders automatically on every Git platform. This eliminates all web development complexity while remaining universally accessible.

### V. Reproducibility
Every displayed example MUST be reproducible from source. Store example source code or generation scripts alongside outputs. Provide clear instructions for regenerating any plot or example locally. Dead examples (unreproducible outputs) MUST be flagged or removed.

**Rationale**: A gallery of orphaned outputs loses scientific and educational value. Reproducibility enables verification, modification, and learning.

## Technical Constraints

- **Markdown Standard**: Use CommonMark-compatible markdown. Avoid platform-specific extensions unless they gracefully degrade (e.g., GitHub's task lists).
- **Image Formats**: PNG for plots/diagrams, JPEG for photos, SVG for scalable graphics. Store images in `images/` subdirectories relative to markdown files.
- **File Organization**: Group related examples in directories. Use descriptive filenames. Include README.md or index.md as directory entry points.
- **Link Hygiene**: Use relative links between markdown files. Ensure all internal links remain valid after repository moves or forks.
- **Size Limits**: Individual markdown files SHOULD stay under 1MB. Large image collections SHOULD be organized across multiple pages with navigation links.

## Development Workflow

- **Test-First**: Write tests for markdown generation and image production before implementation
- **Local Preview**: All gallery changes MUST be previewable locally in any markdown viewer or Git platform
- **Incremental Updates**: Gallery generation MUST support incremental updates (only regenerate changed examples)
- **Version Control**: All example sources, generation scripts, and outputs under Git version control
- **CI/CD**: Automated testing and markdown generation pipeline required for production updates

## Governance

This constitution defines the immutable principles governing the con-duct-gallery project. All features, enhancements, and fixes MUST align with these principles. Deviations require explicit justification documented in the implementation plan's Complexity Tracking section.

**Amendment Process**:
1. Propose amendment with rationale and impact analysis
2. Document in pull request with constitutional amendment label
3. Require consensus from project maintainers
4. Update version following semantic versioning (breaking = MAJOR, new principle = MINOR, clarification = PATCH)
5. Cascade changes to all dependent templates and documentation

**Compliance Review**:
- All pull requests MUST verify alignment with constitutional principles
- Implementation plans MUST include Constitution Check gate
- Complexity that violates principles requires documented justification or simplification

**Version**: 2.0.0 | **Ratified**: 2025-10-03 | **Last Amended**: 2025-10-03
