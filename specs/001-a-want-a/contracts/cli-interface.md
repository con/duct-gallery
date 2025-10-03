# CLI Interface Contract

**Phase**: 1 - Design & Contracts
**Date**: 2025-10-03

## Command: `con-duct-gallery generate`

### Purpose
Generate the gallery README.md and plot images from examples.yaml configuration.

### Signature
```bash
con-duct-gallery generate [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--force` | flag | False | Re-fetch logs and regenerate plots even if cached |
| `--config` | path | `examples.yaml` | Path to YAML configuration file |
| `--output` | path | `README.md` | Path for generated markdown file |
| `--log-dir` | path | `logs/` | Directory for cached log files |
| `--image-dir` | path | `images/` | Directory for generated SVG plots |
| `--verbose`, `-v` | flag | False | Enable detailed logging |
| `--dry-run` | flag | False | Show what would be done without executing |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - gallery generated |
| 1 | Invalid configuration (YAML parse error, validation failure) |
| 2 | Fetch error (all examples failed to fetch) |
| 3 | Plot error (all examples failed to plot) |
| 4 | File system error (cannot write output) |

### Output

**stdout** (normal mode):
```
✓ Loaded 3 examples from examples.yaml
✓ Fetched logs for "con/duct Demo Example" (4 files)
✓ Generated plot: images/con-duct-demo-example.svg
✓ Fetched logs for "Example 2" (cached)
✓ Generated plot: images/example-2.svg (cached)
✓ Generated README.md with 3 examples, 5 tags
```

**stdout** (verbose mode):
```
[INFO] Loading configuration from examples.yaml
[DEBUG] Validating 3 examples
[INFO] Processing "con/duct Demo Example"
[DEBUG] Fetching https://raw.githubusercontent.com/.../example_output_info.json
[DEBUG] Parsing output_paths: 4 files found
[DEBUG] Fetching usage.json, stdout, stderr
[INFO] Generating plot with options: []
[DEBUG] Running: con-duct plot --output images/demo.svg logs/demo/usage.json
[INFO] Plot saved: images/con-duct-demo-example.svg (42.3 KB)
[INFO] Generating markdown gallery
[DEBUG] Tag index: 5 tags, 3 examples
[DEBUG] Writing README.md (15.2 KB)
[INFO] ✓ Gallery generation complete
```

**stderr** (errors):
```
[ERROR] Failed to fetch example "Broken Example": HTTP 404
[WARN] Skipping example "Broken Example" - will not appear in gallery
[ERROR] Plot generation failed for "Example 2": con-duct command not found
[WARN] Example "Example 2" will appear without plot image
```

### Behavior

#### First Run (empty cache):
1. Load and validate `examples.yaml`
2. For each example:
   - Fetch info JSON
   - Parse `output_paths` to discover related files
   - Fetch usage, stdout, stderr
   - Save to `logs/{example-slug}/`
   - Run `con-duct plot --output {svg_path} {usage_json} {plot_options}`
   - Save SVG to `images/{example-slug}.svg`
3. Generate README.md:
   - Header with auto-update badge
   - Tag index with hyperlinks
   - Example sections with plots
4. Write README.md to output path

#### Subsequent Runs (with cache):
1. Load and validate `examples.yaml`
2. For each example:
   - Check if `logs/{example-slug}/` exists
     - Yes → skip fetch (unless `--force`)
     - No → fetch as above
   - Check if `images/{example-slug}.svg` exists and is newer than usage JSON
     - Yes → skip plot generation (unless `--force`)
     - No → regenerate plot
3. Always regenerate README.md (cheap operation)

#### With `--force`:
- Ignore cache entirely
- Re-fetch all logs
- Regenerate all plots
- Regenerate README.md

#### With `--dry-run`:
- Validate configuration
- Show what would be fetched/generated
- Do not write any files
- Exit with code 0

### Error Handling

**Partial failures allowed**:
- If some examples fail to fetch → warn, continue with others
- If some plots fail → warn, show example without plot
- README always generated (even if all plots fail)

**Fatal errors**:
- Invalid YAML schema → exit 1
- Cannot write output file → exit 4
- All examples failed → exit 2 or 3

### Examples

#### Basic usage:
```bash
$ con-duct-gallery generate
✓ Loaded 5 examples from examples.yaml
✓ Generated README.md with 5 examples, 8 tags
```

#### Force regeneration:
```bash
$ con-duct-gallery generate --force
✓ Loaded 5 examples from examples.yaml
✓ Re-fetched all logs (20 files)
✓ Regenerated all plots (5 SVGs)
✓ Generated README.md with 5 examples, 8 tags
```

#### Custom paths:
```bash
$ con-duct-gallery generate \
    --config gallery-config.yaml \
    --output docs/GALLERY.md \
    --image-dir docs/plots \
    --log-dir .cache/logs
```

#### Dry run:
```bash
$ con-duct-gallery generate --dry-run
[DRY RUN] Would fetch logs for 3 examples
[DRY RUN] Would generate 3 plots
[DRY RUN] Would write README.md (estimated 12 KB)
```

### Testing Contract

**Unit tests** (`tests/unit/test_cli.py`):
```python
def test_cli_defaults():
    """Test default argument values"""
    args = parse_args(['generate'])
    assert args.config == Path('examples.yaml')
    assert args.output == Path('README.md')
    assert args.force is False

def test_cli_force_flag():
    """Test --force flag parsing"""
    args = parse_args(['generate', '--force'])
    assert args.force is True

def test_cli_custom_paths():
    """Test custom path arguments"""
    args = parse_args([
        'generate',
        '--config', 'custom.yaml',
        '--output', 'GALLERY.md',
        '--log-dir', 'cache/',
        '--image-dir', 'plots/'
    ])
    assert args.config == Path('custom.yaml')
    assert args.output == Path('GALLERY.md')
```

**Integration tests** (`tests/integration/test_end_to_end.py`):
```python
def test_generate_from_scratch(tmp_path):
    """Test full generation with no cache"""
    # Given: empty directories, valid YAML
    # When: run generate command
    # Then: README.md exists, images/ populated, logs/ populated

def test_generate_with_cache(tmp_path):
    """Test incremental generation"""
    # Given: existing logs/ and images/
    # When: run generate without --force
    # Then: cached files reused, README.md updated

def test_generate_force_flag(tmp_path):
    """Test --force regenerates everything"""
    # Given: existing cache
    # When: run generate --force
    # Then: all logs re-fetched, all plots regenerated
```

### Dependencies

- `argparse` (stdlib): Argument parsing
- `pathlib` (stdlib): Path handling
- `sys` (stdlib): Exit codes
- `logging` (stdlib): Verbose output
