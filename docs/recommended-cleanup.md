# Recommended Cleanup Tasks

## Files to Consider for Removal

### 1. Python Cache Files
**Path**: `**/__pycache__/`  
**Reason**: Auto-generated files that should not be in version control  
**Action**: Already in .gitignore, can be safely removed from working directory

### 2. Duplicate/Backup Scripts
**Path**: `scripts/original_versions/`  
**Reason**: Backup copies of scripts - should use git for version control instead  
**Action**: Verify scripts are committed to git, then remove directory

### 3. Test Application
**Path**: `asma_al_husna_cli/test_app.py`  
**Reason**: Appears to be a manual testing script, not part of test suite  
**Action**: Move functionality to proper pytest tests, then remove

### 4. Demo Scripts
**Path**: `asma_al_husna_cli/demo_randomness.py`  
**Reason**: Demo/example code not needed in production  
**Action**: Move to examples/ directory or documentation

### 5. Redundant Scripts
**Path**: `scripts/extract_and_fix_csv.py`  
**Path**: `scripts/reconstruct_csv.py`  
**Path**: `scripts/parse_all_names.py`  
**Reason**: Appear to be one-off data processing scripts  
**Action**: Document their purpose, archive if no longer needed

### 6. Empty Directories
**Path**: `data/cache/`  
**Reason**: Empty cache directory  
**Action**: Add .gitkeep if needed, or remove if not used

### 7. Specification Files in Code Directory
**Path**: `asma_al_husna_cli/specs/`  
**Reason**: Documentation should be in docs/ directory  
**Action**: Move to docs/specs/ directory

## Files to Reorganize

### 1. Requirements Files
**Current**: `asma_al_husna_cli/requirements.txt` and `requirements-dev.txt`  
**Recommendation**: Consolidate into single `requirements.txt` with sections:
```
# Core dependencies
typer>=0.9.0
rich>=13.7.0

# Optional dependencies
python-bidi>=0.4.2  # Arabic text
pyfiglet>=1.0.2     # ASCII art

# Development dependencies
pytest>=7.0.0
pytest-cov>=4.0.0
```

### 2. Configuration Files
**Current**: Settings hardcoded in various files  
**Recommendation**: Create `config/` directory with:
- `config/default.yaml` - Default settings
- `config/development.yaml` - Dev overrides
- `config/production.yaml` - Prod settings

## Code Cleanup Tasks

### 1. Remove Debug/Development Code
- Remove or properly gate print statements used for debugging
- Remove commented-out code blocks
- Remove TODO comments that are completed

### 2. Standardize Import Order
All files should follow:
```python
# Standard library imports
import os
import sys

# Third-party imports
import typer
from rich import print

# Local imports
from .module import function
```

### 3. Remove Unused Imports
Several files have imports that are never used:
- Check all imports with `pylint` or `flake8`
- Remove any that are unnecessary

### 4. Consolidate Duplicate Constants
Constants are defined in multiple places:
- Move all to `asma_core/constants.py`
- Remove local definitions

## Data Cleanup

### 1. Processed CSV Files
**Path**: `data/processed/`  
**Issue**: Multiple similar CSV files  
**Action**: Document purpose of each, consolidate if possible

### 2. Log Files
**Path**: `data/logs/meditation_sessions.csv`  
**Action**: Add log rotation or archiving mechanism

## Documentation Cleanup

### 1. Conflicting Documentation
- README.md and CLAUDE.md have overlapping content
- Consolidate into single source of truth

### 2. Outdated Planning Docs
**Path**: `RESTRUCTURING_PLAN.md`  
**Action**: Move to docs/archive/ if plan is implemented

## Testing Cleanup

### 1. Test Organization
Current test files test existence rather than behavior  
**Action**: Rewrite tests to focus on functionality

### 2. Test Data
No test fixtures or mock data  
**Action**: Create `tests/fixtures/` with sample CSV data

## Important Notes

⚠️ **DO NOT DELETE** any files without:
1. Confirming they are properly committed to git
2. Verifying no other code depends on them
3. Documenting why they were removed

⚠️ **BACKUP FIRST**: Create a backup branch before any cleanup:
```bash
git checkout -b pre-cleanup-backup
git push origin pre-cleanup-backup
```