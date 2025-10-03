
# Implementation Plan: con/duct Examples Gallery

**Branch**: `001-a-want-a` | **Date**: 2025-10-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/home/yoh/proj/CON/con-duct-gallery/specs/001-a-want-a/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Create an automated gallery of con/duct tool usage examples. Fetch con/duct log files from GitHub/DataLad, generate SVG plots, and organize into a markdown gallery with tag-based navigation. YAML configuration drives example registry. Daily GitHub Actions automate updates.

## Technical Context
**Language/Version**: Python 3.11+
**Primary Dependencies**: Pydantic (data validation), PyYAML (config), con-duct (plot generation), requests/httpx (fetching)
**Storage**: Local filesystem (logs in `logs/`, images in `images/`, generated README.md in repo root)
**Testing**: pytest with unit tests for robust behavior
**Target Platform**: GitHub Actions (Linux), local development (cross-platform)
**Project Type**: single (Python CLI tool)
**Project Name**: con-duct-gallery (entry point: `con-duct-gallery`)
**Configuration**: YAML file (`examples.yaml`) defining example sources, tags, plot options
**Markdown Flavor**: GitHub Flavored Markdown with unicode characters
**Performance Goals**: Gallery generation <5 minutes for 50 examples
**Constraints**: No PyPI distribution, GitHub-first design, incremental updates, SVG plots only
**Scale/Scope**: 10-100 examples, daily automated updates via cron, PR-triggered preview builds

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Content-First ✅
- **Requirement**: Gallery showcases examples and plots, not web features
- **Compliance**: YAML-driven example registry, markdown output, plot-centric design
- **Status**: PASS

### II. Automatic Updates ✅
- **Requirement**: Content updates without manual intervention
- **Compliance**: GitHub Actions cron (daily), PR automation, incremental fetching
- **Status**: PASS

### III. Minimalist Interface ✅
- **Requirement**: Headers, lists, images, links only in markdown
- **Compliance**: GitHub Flavored Markdown, no HTML embeds, simple structure
- **Status**: PASS

### IV. Markdown-Native ✅
- **Requirement**: Generate markdown only, no HTML/CSS/JS
- **Compliance**: Outputs README.md + SVG images, relies on GitHub rendering
- **Status**: PASS

### V. Reproducibility ✅
- **Requirement**: Examples reproducible from source
- **Compliance**: YAML tracks sources, con-duct logs stored, plot commands preserved
- **Status**: PASS

**Initial Gate Result**: ✅ PASS - All constitutional principles satisfied

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
con-duct-gallery/
├── src/
│   └── con_duct_gallery/
│       ├── __init__.py
│       ├── __main__.py          # Entry point for `con-duct-gallery` command
│       ├── models.py             # Pydantic models for YAML schema
│       ├── fetcher.py            # Download logs from GitHub/DataLad
│       ├── plotter.py            # Generate SVG plots via con-duct
│       ├── generator.py          # Generate README.md markdown
│       └── cli.py                # CLI argument parsing
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_fetcher.py
│   │   ├── test_plotter.py
│   │   └── test_generator.py
│   └── integration/
│       └── test_end_to_end.py
├── .github/
│   └── workflows/
│       ├── daily-update.yml      # Cron: daily gallery regeneration
│       └── pr-preview.yml        # PR: generate and comment preview
├── examples.yaml                 # Example registry (YAML)
├── logs/                         # Fetched con/duct logs (gitignored)
├── images/                       # Generated SVG plots
├── README.md                     # Generated gallery (root)
├── pyproject.toml                # Modern Python packaging
├── .gitignore
└── LICENSE
```

**Structure Decision**: Single Python project with contemporary tooling (pyproject.toml). No PyPI upload, but installable locally via `pip install -e .` for development. CLI entry point `con-duct-gallery` via console_scripts. GitHub Actions in `.github/workflows/` for automation. Generated content (README.md, images/) committed to repo for GitHub rendering.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
1. **Setup tasks** (3-4 tasks):
   - Project structure (pyproject.toml, src/, tests/)
   - Dependencies (Pydantic, PyYAML, requests, pytest)
   - .gitignore and directory creation

2. **Model tasks** from data-model.md (2-3 tasks [P]):
   - ExampleEntry Pydantic model with validation
   - ExampleRegistry model with YAML loading
   - Unit tests for models

3. **Contract tests** from contracts/ (3 tasks [P]):
   - CLI argument parsing tests
   - YAML schema validation tests
   - Markdown output validation tests

4. **Core implementation** (4-5 tasks):
   - Fetcher module (parse output_paths, download files)
   - Plotter module (subprocess call to con-duct)
   - Generator module (markdown template rendering)
   - CLI module (argparse integration)

5. **Integration tests** from quickstart.md (2 tasks):
   - End-to-end generation test
   - Incremental update test

6. **GitHub Actions** (2 tasks [P]):
   - daily-update.yml workflow
   - pr-preview.yml workflow

7. **Documentation** (1 task):
   - Initial examples.yaml with demo example

**Ordering Strategy**:
- Phase 3.1: Setup (sequential)
- Phase 3.2: Tests first (parallel where possible)
- Phase 3.3: Implementation (Models → Services → CLI)
- Phase 3.4: Integration (GitHub Actions, documentation)
- TDD throughout: contract tests fail before implementation

**Estimated Output**: 18-22 numbered tasks in tasks.md

**Parallel Execution Opportunities**:
- Model tests [P] (different files)
- Contract tests [P] (different contracts)
- GitHub workflow files [P]

**Dependencies**:
- Models block Fetcher/Plotter/Generator
- All core modules block CLI integration
- CLI blocks integration tests

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) → research.md created
- [x] Phase 1: Design complete (/plan command) → data-model.md, contracts/, quickstart.md, CLAUDE.md created
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (all 5 principles satisfied)
- [x] Post-Design Constitution Check: PASS (no violations introduced)
- [x] All NEEDS CLARIFICATION resolved (none in Technical Context)
- [x] Complexity deviations documented (none required)

**Artifacts Generated**:
- ✅ `/specs/001-a-want-a/plan.md` (this file)
- ✅ `/specs/001-a-want-a/research.md` (Phase 0)
- ✅ `/specs/001-a-want-a/data-model.md` (Phase 1)
- ✅ `/specs/001-a-want-a/contracts/cli-interface.md` (Phase 1)
- ✅ `/specs/001-a-want-a/contracts/yaml-schema.md` (Phase 1)
- ✅ `/specs/001-a-want-a/contracts/markdown-output.md` (Phase 1)
- ✅ `/specs/001-a-want-a/quickstart.md` (Phase 1)
- ✅ `/home/yoh/proj/CON/con-duct-gallery/CLAUDE.md` (Phase 1)

---
*Based on Constitution v2.0.0 - See `.specify/memory/constitution.md`*
