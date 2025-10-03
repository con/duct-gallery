# Quickstart: con/duct Examples Gallery

**Phase**: 1 - Design & Contracts
**Date**: 2025-10-03

## Purpose
This document provides step-by-step instructions for users to set up and use the con/duct examples gallery. It serves as both user documentation and an integration test specification.

## Prerequisites

- Python 3.11 or higher
- `con-duct` installed and available in PATH
- Git (for cloning repository)
- Internet connection (for fetching remote logs)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/con/con-duct-gallery.git
cd con-duct-gallery
```

### 2. Install dependencies
```bash
pip install -e .
```

This installs the package in editable mode with all dependencies.

### 3. Verify installation
```bash
con-duct-gallery --help
```

Expected output:
```
usage: con-duct-gallery [-h] {generate} ...

Generate markdown gallery of con/duct examples

positional arguments:
  {generate}  Available commands

optional arguments:
  -h, --help  show this help message and exit
```

## Quick Start: Generate Gallery

### Step 1: Create configuration (con-duct-gallery.yaml)

```yaml
examples:
  - title: "con/duct Demo Example"
    source_repo: "https://github.com/con/duct/"
    info_file: "https://raw.githubusercontent.com/con/duct/a539c3e20cccd4455a75cd7bfbae9cd644cdcbff/demo/example_output_info.json"
    tags:
      - synthetic
      - medium-length
    description: "Demo example from the con/duct repository showing resource usage tracking"
```

### Step 2: Generate the gallery

```bash
con-duct-gallery generate
```

Expected output:
```
✓ Loaded 1 example from con-duct-gallery.yaml
✓ Fetching logs for "con/duct Demo Example"
  ├─ Downloading example_output_info.json
  ├─ Downloading example_output_usage.json
  ├─ Downloading example_output_stdout
  └─ Downloading example_output_stderr
✓ Generating plot: images/con-duct-demo-example.svg
✓ Generated README.md with 1 example, 2 tags
```

### Step 3: View the gallery

```bash
# Open in browser (GitHub-like rendering)
open README.md

# Or view in terminal
cat README.md
```

## Expected Directory Structure

After running `generate`, you should see:

```
con-duct-gallery/
├── con-duct-gallery.yaml                 # Your configuration
├── README.md                      # ✅ Generated gallery
├── images/                        # ✅ Generated
│   └── con-duct-demo-example.svg
└── logs/                          # ✅ Fetched
    └── con-duct-demo-example/
        ├── example_output_info.json
        ├── example_output_usage.json
        ├── example_output_stdout
        └── example_output_stderr
```

## Expected README.md Content

The generated README.md should contain:

### 1. Header
```markdown
# con/duct Examples Gallery

> 🤖 Automatically generated gallery of con/duct usage examples
> Last updated: 2025-10-03 15:30 UTC
```

### 2. Tag Index
```markdown
## 📚 Browse by Tag

**medium-length**: [con/duct Demo Example](#con-duct-demo-example)
**synthetic**: [con/duct Demo Example](#con-duct-demo-example)
```

### 3. Example Section
```markdown
## 📊 Examples

### con/duct Demo Example

**Tags**: `medium-length` `synthetic`
**Repository**: [github.com/con/duct](https://github.com/con/duct/)

Demo example from the con/duct repository showing resource usage tracking

![Plot for con/duct Demo Example](images/con-duct-demo-example.svg)

<details>
<summary>📋 Metadata</summary>

- **Info file**: [example_output_info.json](logs/con-duct-demo-example/example_output_info.json)
- **Usage data**: [example_output_usage.json](logs/con-duct-demo-example/example_output_usage.json)
- **Standard output**: [stdout](logs/con-duct-demo-example/example_output_stdout)
- **Standard error**: [stderr](logs/con-duct-demo-example/example_output_stderr)

</details>

---
```

## Common Workflows

### Add a new example

1. Edit `con-duct-gallery.yaml`:
```yaml
examples:
  # Existing examples...

  - title: "My New Example"
    source_repo: "https://github.com/myuser/myrepo"
    info_file: "https://example.com/logs/output_info.json"
    tags:
      - real-world
      - neuroimaging
    plot_options:
      - --style=seaborn
      - --dpi=300
```

2. Regenerate:
```bash
con-duct-gallery generate
```

Only the new example will be fetched (existing ones cached).

### Force regenerate everything

```bash
con-duct-gallery generate --force
```

This re-fetches all logs and regenerates all plots.

### Custom output location

```bash
con-duct-gallery generate \
    --output docs/GALLERY.md \
    --image-dir docs/plots \
    --log-dir .cache/logs
```

## Validation Tests

### Test 1: Valid configuration loads
```bash
con-duct-gallery generate --dry-run
```

Expected: No errors, shows what would be generated.

### Test 2: Invalid YAML rejected
Create `bad.yaml`:
```yaml
examples:
  - title: ""  # Empty title - invalid
    source_repo: "https://github.com/test/repo"
    info_file: "https://example.com/info.json"
```

```bash
con-duct-gallery generate --config bad.yaml
```

Expected output:
```
[ERROR] Validation failed for bad.yaml:
  examples[0].title: Title cannot be empty
```

Exit code: 1

### Test 3: Missing con-duct command
```bash
# Temporarily remove con-duct from PATH
PATH=/usr/bin con-duct-gallery generate
```

Expected output:
```
[ERROR] con-duct command not found
[ERROR] Please install con-duct: pip install con-duct
```

Exit code: 3

### Test 4: Network failure handling
Configure with unreachable URL:
```yaml
examples:
  - title: "Broken Example"
    source_repo: "https://github.com/test/repo"
    info_file: "https://invalid-url-that-does-not-exist.example/file.json"
    tags: [test]
```

```bash
con-duct-gallery generate
```

Expected output:
```
✓ Loaded 1 example from con-duct-gallery.yaml
✗ Failed to fetch "Broken Example": HTTP 404 / Connection error
⚠️  Skipping example "Broken Example"
✓ Generated README.md with 0 examples, 0 tags
```

Exit code: 0 (partial success)

### Test 5: Incremental updates
```bash
# First run
con-duct-gallery generate
# Output: Fetched logs, generated plot

# Second run (immediate)
con-duct-gallery generate
# Output: Used cached logs, used cached plot

# Modify YAML (add description)
# Third run
con-duct-gallery generate
# Output: Used cached logs, used cached plot, regenerated README
```

## Troubleshooting

### "con-duct command not found"
**Solution**: Install con-duct
```bash
pip install con-duct
```

### "ValidationError: Duplicate titles found"
**Solution**: Ensure all example titles are unique (case-insensitive)

### "Plot generation failed"
**Diagnosis**:
```bash
# Test con-duct manually
con-duct plot --help
con-duct plot logs/example/usage.json --output test.svg
```

### "Network timeout"
**Solution**: Increase timeout or check internet connection
```bash
# Retry with verbose logging
con-duct-gallery generate --verbose
```

## Integration Test Checklist

When running `quickstart.md` as an integration test:

- [ ] Repository clones successfully
- [ ] `pip install -e .` completes without errors
- [ ] `con-duct-gallery --help` shows help text
- [ ] Creating `con-duct-gallery.yaml` with demo example
- [ ] `con-duct-gallery generate` runs successfully
- [ ] `README.md` is created
- [ ] `images/con-duct-demo-example.svg` exists and is valid SVG
- [ ] `logs/con-duct-demo-example/` contains 4 files
- [ ] Tag index links to example section
- [ ] Anchor links work correctly
- [ ] Second run uses cache (logs "cached" messages)
- [ ] `--force` flag re-fetches and regenerates
- [ ] Invalid YAML is rejected with clear error message
- [ ] Network errors handled gracefully

## Performance Expectations

| Operation | Time (1 example) | Time (10 examples) | Time (50 examples) |
|-----------|------------------|--------------------|--------------------|
| Fetch logs | ~2s | ~15s | ~60s |
| Generate plots | ~1s | ~8s | ~40s |
| Generate README | <0.1s | <0.5s | <2s |
| **Total** | ~3s | ~24s | ~102s |

All times assume:
- Good network connection (50 Mbps+)
- con-duct installed and working
- Modern CPU (2+ cores)

## Next Steps

- **Automate**: Set up GitHub Actions (see `.github/workflows/`)
- **Customize**: Add more examples to `con-duct-gallery.yaml`
- **Contribute**: Create a pull request with new examples
- **Deploy**: Push to GitHub, gallery auto-renders

## Success Criteria

✅ Gallery generation completes without errors
✅ README.md renders correctly on GitHub
✅ All plots display as SVG images
✅ Tag index links navigate to examples
✅ Incremental updates work (caching)
✅ Force regeneration works
✅ Invalid configurations rejected clearly
