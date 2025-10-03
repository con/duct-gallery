# Tasks: con/duct Examples Gallery

**Input**: Design documents from `/home/yoh/proj/CON/con-duct-gallery/specs/001-a-want-a/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → ✅ Tech stack: Python 3.11+, Pydantic, PyYAML, requests, pytest
   → ✅ Structure: Single project (src/con_duct_gallery/, tests/)
2. Load optional design documents:
   → ✅ data-model.md: 5 entities (ExampleEntry, ExampleRegistry, FetchedLog, GeneratedPlot, GalleryMarkdown)
   → ✅ contracts/: 3 contracts (cli-interface, yaml-schema, markdown-output)
   → ✅ research.md: Technical decisions extracted
3. Generate tasks by category:
   → Setup: pyproject.toml, dependencies, directory structure
   → Tests: 3 contract tests + 2 integration tests
   → Core: 3 models + 3 modules (fetcher, plotter, generator) + CLI
   → Integration: GitHub Actions workflows
   → Polish: Initial config file, unit tests
4. Apply task rules:
   → Different files marked [P]
   → Tests before implementation
5. Number tasks sequentially (T001-T022)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate: ✅ All contracts tested, all entities modeled, TDD enforced
9. Return: SUCCESS (22 tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- All file paths are absolute or relative to repository root

## Path Conventions
- **Single project structure** (from plan.md):
  - Source: `src/con_duct_gallery/`
  - Tests: `tests/unit/`, `tests/integration/`
  - Config: Repository root

---

## Phase 3.1: Setup

- [x] **T001** Create pyproject.toml with project metadata and dependencies
  - **File**: `pyproject.toml`
  - **Dependencies**: `pydantic>=2.0`, `pyyaml>=6.0`, `requests>=2.31`, `pytest>=7.4`, `pytest-cov>=4.1`
  - **Entry point**: `con-duct-gallery = "con_duct_gallery.__main__:main"`
  - **Build system**: setuptools with `src/` layout

- [x] **T002** Create project directory structure
  - **Directories**:
    - `src/con_duct_gallery/` (package)
    - `tests/unit/` (unit tests)
    - `tests/integration/` (integration tests)
    - `.github/workflows/` (CI/CD)
  - **Files**:
    - `src/con_duct_gallery/__init__.py`
    - `.gitignore` (logs/, __pycache__, *.pyc, .pytest_cache, dist/, *.egg-info/)

- [x] **T003** [P] Configure pytest with pytest.ini
  - **File**: `pytest.ini`
  - **Settings**: testpaths, python_files, addopts for coverage
  - **Coverage targets**: src/con_duct_gallery/

---

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests (All [P] - Different Files)

- [x] **T004** [P] Contract test for CLI argument parsing in tests/unit/test_cli.py
  - **From**: contracts/cli-interface.md
  - **Tests**:
    - `test_cli_defaults()`: Assert default config path is `con-duct-gallery.yaml`
    - `test_cli_force_flag()`: Assert --force flag sets force=True
    - `test_cli_custom_paths()`: Assert custom --config, --output, --log-dir, --image-dir
    - `test_cli_verbose_flag()`: Assert -v/--verbose enables verbose mode
    - `test_cli_dry_run()`: Assert --dry-run sets dry_run=True
  - **Must fail**: No CLI module exists yet

- [x] **T005** [P] Contract test for YAML schema validation in tests/unit/test_models.py
  - **From**: contracts/yaml-schema.md
  - **Tests**:
    - `test_valid_yaml_loads()`: Valid YAML with all fields
    - `test_empty_title_rejected()`: ValidationError for empty title
    - `test_title_too_long_rejected()`: ValidationError for >100 char title
    - `test_tags_normalized_lowercase()`: Tags converted to lowercase
    - `test_invalid_tag_format_rejected()`: ValidationError for tags with spaces/underscores
    - `test_info_file_must_be_json()`: ValidationError if not ending in .json
    - `test_duplicate_titles_rejected()`: ValidationError for duplicate titles
    - `test_at_least_one_example_required()`: ValidationError for empty examples list
  - **Must fail**: No models module exists yet

- [x] **T006** [P] Contract test for markdown output generation in tests/unit/test_generator.py
  - **From**: contracts/markdown-output.md
  - **Tests**:
    - `test_slugify()`: "con/duct Demo" → "con-duct-demo"
    - `test_tag_index_generation()`: Multiple tags with correct hyperlinks
    - `test_example_section_with_plot()`: H3 heading, tags, repo link, image embed
    - `test_example_section_without_plot()`: Warning message for missing plot
    - `test_anchor_uniqueness()`: No duplicate anchor IDs
    - `test_header_section()`: Title, auto-update notice, timestamp
    - `test_footer_section()`: Maintenance instructions
  - **Must fail**: No generator module exists yet

### Integration Tests (All [P] - Different Files)

- [x] **T007** [P] Integration test for end-to-end gallery generation in tests/integration/test_end_to_end.py
  - **From**: quickstart.md acceptance scenarios
  - **Tests**:
    - `test_generate_from_scratch(tmp_path)`: Empty dirs → full generation
      - Given: Empty directories, valid YAML
      - When: Run generate command
      - Then: README.md exists, images/ populated with SVGs, logs/ populated
    - `test_generate_with_cache(tmp_path)`: Cached logs → incremental update
      - Given: Existing logs/ and images/
      - When: Run generate without --force
      - Then: Cached files reused, README.md updated
    - `test_generate_force_flag(tmp_path)`: --force → full regeneration
      - Given: Existing cache
      - When: Run generate --force
      - Then: All logs re-fetched, all plots regenerated
  - **Must fail**: No CLI or core modules exist yet

- [x] **T008** [P] Integration test for error handling in tests/integration/test_error_handling.py
  - **From**: quickstart.md edge cases
  - **Tests**:
    - `test_invalid_yaml_rejected()`: ValidationError with clear message
    - `test_network_failure_graceful()`: HTTP 404 → warning, continue with other examples
    - `test_plot_generation_failure()`: con-duct error → warning, example without plot
    - `test_partial_fetch_success()`: Some examples fail → gallery still generated
  - **Must fail**: No error handling implemented yet

---

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models (All [P] - Different Classes in Same File)

- [x] **T009** [P] Implement ExampleEntry Pydantic model in src/con_duct_gallery/models.py
  - **From**: data-model.md § ExampleEntry
  - **Fields**: title, source_repo (HttpUrl), info_file (HttpUrl), tags, plot_options, description
  - **Validators**:
    - `title`: non-empty, max 100 chars
    - `tags`: lowercase, alphanumeric + hyphens only
    - `info_file`: must end with .json
  - **Properties**: `slug` (GitHub anchor slug from title)
  - **Makes tests pass**: T005 (YAML schema validation tests)

- [x] **T010** Implement ExampleRegistry Pydantic model in src/con_duct_gallery/models.py
  - **From**: data-model.md § ExampleRegistry
  - **Fields**: examples (list[ExampleEntry])
  - **Validators**: no duplicate titles, at least one example
  - **Class methods**: `from_yaml(path: Path) -> ExampleRegistry`
  - **Methods**: `get_all_tags() -> set[str]`, `filter_by_tag(tag: str) -> list[ExampleEntry]`
  - **Makes tests pass**: T005 (YAML loading tests)

### Core Modules (Sequential - Dependencies)

- [x] **T011** Implement fetcher module in src/con_duct_gallery/fetcher.py
  - **From**: research.md § HTTP Client, data-model.md § FetchedLog
  - **Functions**:
    - `fetch_info_json(url: str, dest: Path) -> dict`: Download and parse info JSON
    - `parse_output_paths(info_json: dict, base_url: str) -> dict[str, str]`: Extract file URLs from output_paths
    - `fetch_log_files(example: ExampleEntry, log_dir: Path, force: bool) -> FetchedLog`: Download all files
  - **Uses**: `requests` library
  - **Error handling**: HTTP errors → log warning, raise exception
  - **Caching**: Skip fetch if files exist and not force mode

- [x] **T012** Implement plotter module in src/con_duct_gallery/plotter.py
  - **From**: research.md § con-duct Integration, data-model.md § GeneratedPlot
  - **Functions**:
    - `generate_plot(usage_json: Path, output_svg: Path, plot_options: list[str]) -> Path`: Call con-duct plot
    - `should_regenerate_plot(svg_path: Path, usage_json: Path, force: bool) -> bool`: Check if plot needs regeneration
  - **Uses**: `subprocess.run()` to call `con-duct plot`
  - **Options**: `--output {svg_path} {plot_options} {usage_json}`
  - **Error handling**: Command not found → clear error, plot failure → log error

- [x] **T013** Implement generator module in src/con_duct_gallery/generator.py
  - **From**: contracts/markdown-output.md, data-model.md § GalleryMarkdown
  - **Functions**:
    - `slugify(title: str) -> str`: Convert title to GitHub anchor slug
    - `generate_header(timestamp: str) -> str`: Title + auto-update notice
    - `generate_tag_index(registry: ExampleRegistry) -> str`: Tag → example links
    - `generate_example_section(example: ExampleEntry, svg_exists: bool) -> str`: Full example markdown
    - `generate_footer() -> str`: Maintenance instructions
    - `generate_gallery(registry: ExampleRegistry, image_dir: Path, log_dir: Path) -> str`: Complete README.md
  - **Unicode**: Use emojis (📚 📊 🛠️ 🤖 📋)
  - **Makes tests pass**: T006 (markdown output tests)

### CLI Integration

- [x] **T014** Implement CLI argument parsing in src/con_duct_gallery/cli.py
  - **From**: contracts/cli-interface.md
  - **Arguments**: generate subcommand with --force, --config, --output, --log-dir, --image-dir, --verbose, --dry-run
  - **Defaults**: config=con-duct-gallery.yaml, output=README.md, log-dir=logs/, image-dir=images/
  - **Returns**: Namespace with parsed arguments
  - **Makes tests pass**: T004 (CLI parsing tests)

- [x] **T015** Implement main entry point in src/con_duct_gallery/__main__.py
  - **From**: contracts/cli-interface.md § Behavior
  - **Flow**:
    1. Parse CLI arguments
    2. Load and validate YAML configuration
    3. For each example: fetch logs (if needed), generate plot (if needed)
    4. Generate README.md markdown
    5. Write output file
  - **Error handling**: Exit codes 0-4 per contract
  - **Logging**: Use logging module, verbose mode shows DEBUG
  - **Dry run**: Show what would be done, don't execute
  - **Makes tests pass**: T007 (end-to-end integration tests)

---

## Phase 3.4: Integration & Automation

### GitHub Actions (Both [P] - Different Files)

- [x] **T016** [P] Create daily update workflow in .github/workflows/daily-update.yml
  - **From**: research.md § GitHub Actions Strategy
  - **Trigger**: `schedule: cron '0 0 * * *'` (daily at midnight UTC), `workflow_dispatch` (manual)
  - **Steps**:
    1. Checkout repository
    2. Setup Python 3.11
    3. Install dependencies (`pip install -e .`)
    4. Run `con-duct-gallery generate`
    5. Commit changes if README.md or images/ modified
    6. Push to main branch
  - **Permissions**: contents: write

- [x] **T017** [P] Create PR preview workflow in .github/workflows/pr-preview.yml
  - **From**: research.md § GitHub Actions Strategy
  - **Trigger**: `pull_request` on paths `con-duct-gallery.yaml`, `src/**`
  - **Steps**:
    1. Checkout PR branch
    2. Setup Python 3.11
    3. Install dependencies
    4. Run `con-duct-gallery generate`
    5. Post comment with diff preview (do NOT commit)
  - **Permissions**: contents: read, pull-requests: write

---

## Phase 3.5: Polish & Documentation

- [x] **T018** [P] Create initial con-duct-gallery.yaml with demo example
  - **From**: quickstart.md § Step 1
  - **Content**: Single example using con/duct demo from spec.md
    ```yaml
    examples:
      - title: "con/duct Demo Example"
        source_repo: "https://github.com/con/duct/"
        info_file: "https://raw.githubusercontent.com/con/duct/a539c3e20cccd4455a75cd7bfbae9cd644cdcbff/demo/example_output_info.json"
        tags:
          - synthetic
          - medium-length
        description: "Demo example from the con/duct repository"
    ```

- [x] **T019** [P] Add unit tests for fetcher module in tests/unit/test_fetcher.py
  - **Tests**:
    - `test_fetch_info_json()`: Download and parse JSON
    - `test_parse_output_paths()`: Extract file URLs from info JSON
    - `test_fetch_with_cache()`: Skip fetch if files exist
    - `test_fetch_force_mode()`: Re-fetch even if cached
    - `test_network_error_handling()`: HTTP errors raise exceptions

- [x] **T020** [P] Add unit tests for plotter module in tests/unit/test_plotter.py
  - **Tests**:
    - `test_generate_plot()`: Call con-duct plot command
    - `test_should_regenerate_plot()`: Check timestamp logic
    - `test_plot_with_custom_options()`: Pass plot_options to command
    - `test_con_duct_not_found()`: Handle command not found error

- [x] **T021** [P] Create README.md with project description and usage
  - **File**: Repository root README.md (development docs, NOT generated gallery)
  - **Sections**:
    - Project description
    - Installation: `pip install -e .`
    - Usage: `con-duct-gallery generate`
    - Configuration: con-duct-gallery.yaml format
    - Development: Running tests with pytest
  - **Note**: This is the development README; gallery README is generated

- [x] **T022** Run full test suite and verify coverage
  - **Command**: `pytest --cov=src/con_duct_gallery --cov-report=term-missing`
  - **Coverage target**: >80% for all modules
  - **Verify**: All tests pass, no warnings
  - **Fix**: Any failing tests or low coverage areas

---

## Dependencies

**Setup blocks everything**:
- T001 (pyproject.toml) → T002-T022
- T002 (directories) → T003-T022
- T003 (pytest config) → T004-T008

**Tests block implementation** (TDD):
- T004-T008 (all tests) → T009-T015

**Models block services**:
- T009-T010 (models) → T011-T013, T015

**Core modules block CLI**:
- T011 (fetcher) → T015
- T012 (plotter) → T015
- T013 (generator) → T015
- T014 (CLI parsing) → T015

**Implementation blocks polish**:
- T009-T015 (all core) → T019-T022

**No dependencies** (can run anytime after setup):
- T016, T017 (GitHub Actions) - independent
- T018 (demo config) - independent
- T021 (dev README) - independent

---

## Parallel Execution Examples

### Setup phase (sequential):
```bash
# Must run in order
T001 → T002 → T003
```

### Test phase (all parallel):
```bash
# Launch all 5 test tasks together:
Task: "Contract test for CLI argument parsing in tests/unit/test_cli.py"
Task: "Contract test for YAML schema validation in tests/unit/test_models.py"
Task: "Contract test for markdown output generation in tests/unit/test_generator.py"
Task: "Integration test for end-to-end gallery generation in tests/integration/test_end_to_end.py"
Task: "Integration test for error handling in tests/integration/test_error_handling.py"
```

### Model implementation:
```bash
# T009 and T010 modify same file, so sequential
T009 → T010
```

### Core modules (sequential due to dependencies):
```bash
T011 → T012 → T013 → T014 → T015
```

### Automation (both parallel):
```bash
# Different files, no dependencies
Task: "Create daily update workflow in .github/workflows/daily-update.yml"
Task: "Create PR preview workflow in .github/workflows/pr-preview.yml"
```

### Polish (all parallel):
```bash
# All different files
Task: "Create initial con-duct-gallery.yaml with demo example"
Task: "Add unit tests for fetcher module in tests/unit/test_fetcher.py"
Task: "Add unit tests for plotter module in tests/unit/test_plotter.py"
Task: "Create README.md with project description and usage"
```

---

## Validation Checklist

✅ **All contracts have corresponding tests**:
- cli-interface.md → T004
- yaml-schema.md → T005
- markdown-output.md → T006

✅ **All entities have model tasks**:
- ExampleEntry → T009
- ExampleRegistry → T010
- FetchedLog, GeneratedPlot, GalleryMarkdown → implemented in T011-T013

✅ **All tests come before implementation**:
- Tests: T004-T008
- Implementation: T009-T015

✅ **Parallel tasks truly independent**:
- T004, T005, T006, T007, T008: Different test files
- T016, T017: Different workflow files
- T018, T019, T020, T021: Different files

✅ **Each task specifies exact file path**: All tasks include specific file paths

✅ **No task modifies same file as another [P] task**: Verified - T009 and T010 share file but not marked [P]

---

## Notes

- **[P] tasks**: Different files, no dependencies - safe to run in parallel
- **TDD enforcement**: Tests T004-T008 MUST be written and failing before T009-T015
- **Commit strategy**: Commit after each completed task for granular history
- **Test verification**: Run `pytest` after each implementation task to see tests pass
- **Entry point**: After T015, `con-duct-gallery generate` command should work end-to-end
