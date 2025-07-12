# Task: Package Structure Refactoring

**Priority**: CRITICAL  
**Issue**: Mixed package structures - old `asma_al_husna_cli` & `asma_core` alongside new `src/aysekai`  
**Solution**: Consolidate into single modern Python package structure

## Feature Branch
`feature/architecture-package-structure`

## Dependencies
- Requires: All Phase 1 tasks completed

## 1. Tests (RED Phase)

### Create test file: `tests/unit/test_package/test_package_structure.py`

```python
import pytest
import sys
from pathlib import Path
import importlib
import ast

from aysekai.core.models import DivineName
from aysekai.utils.csv_handler import AsmaCSVReader
from aysekai.cli.main import app


class TestPackageStructure:
    """Test modern package structure is working correctly"""
    
    def test_aysekai_package_imports(self):
        """Test all aysekai subpackages can be imported"""
        # Core modules
        from aysekai.core import models, exceptions
        from aysekai.utils import validators, csv_handler
        from aysekai.cli import main, error_handler, path_resolver, secure_logger
        from aysekai.config import settings
        
        # Verify modules are properly loaded
        assert hasattr(models, 'DivineName')
        assert hasattr(exceptions, 'ValidationError')
        assert hasattr(validators, 'InputValidator')
        assert hasattr(settings, 'Settings')
    
    def test_no_old_package_imports(self):
        """Test old packages are not importable"""
        old_packages = [
            'asma_al_husna_cli',
            'asma_core',
        ]
        
        for package in old_packages:
            with pytest.raises(ImportError):
                importlib.import_module(package)
    
    def test_divine_name_model_accessible(self):
        """Test DivineName model is accessible from new location"""
        name = DivineName(
            number=1,
            arabic="الرَّحْمَنُ",
            transliteration="Ar-Rahman",
            brief_meaning="The Most Compassionate",
            level_1_sharia="Divine mercy in creation",
            level_2_tariqa="Path of compassion",
            level_3_haqiqa="Reality of mercy",
            level_4_marifa="Knowledge of divine compassion",
            quranic_references="Quran 55:1",
            dhikr_formulas="Ya Rahman (يا رحمن)",
            pronunciation_guide="Ar-rah-MAAN"
        )
        assert name.number == 1
        assert name.arabic == "الرَّحْمَنُ"
    
    def test_csv_handler_working(self, tmp_path):
        """Test CSV handler works from new location"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "Number,Arabic,Transliteration,Brief Meaning\n"
            "1,الرَّحْمَنُ,Ar-Rahman,The Most Compassionate\n"
        )
        
        reader = AsmaCSVReader(csv_file)
        names = reader.read_all()
        
        assert len(names) == 1
        assert names[0].number == 1
    
    def test_cli_app_accessible(self):
        """Test CLI app is accessible from new location"""
        from aysekai.cli.main import app
        assert app is not None
        assert hasattr(app, 'registered_commands')
    
    def test_no_circular_imports(self):
        """Test no circular import issues exist"""
        # This test will fail if there are circular imports
        try:
            from aysekai.core.models import DivineName
            from aysekai.utils.csv_handler import AsmaCSVReader
            from aysekai.cli.main import app
            from aysekai.config.settings import Settings
            # If we get here without ImportError, no circular imports
            assert True
        except ImportError as e:
            pytest.fail(f"Circular import detected: {e}")
    
    def test_package_metadata(self):
        """Test package metadata is correct"""
        import aysekai
        
        assert hasattr(aysekai, '__version__')
        assert hasattr(aysekai, '__author__')
        assert aysekai.__version__ is not None


class TestPackageCleanup:
    """Test old package files are properly removed/migrated"""
    
    def get_project_root(self) -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent.parent.parent
    
    def test_old_directories_removed(self):
        """Test old package directories are removed"""
        root = self.get_project_root()
        
        old_dirs = [
            root / "asma_al_husna_cli",
            root / "asma_core",
        ]
        
        for old_dir in old_dirs:
            assert not old_dir.exists(), f"Old directory still exists: {old_dir}"
    
    def test_src_structure_correct(self):
        """Test src/aysekai structure is correct"""
        root = self.get_project_root()
        src_dir = root / "src" / "aysekai"
        
        required_subdirs = [
            src_dir / "core",
            src_dir / "utils", 
            src_dir / "cli",
            src_dir / "config",
        ]
        
        for subdir in required_subdirs:
            assert subdir.exists(), f"Required directory missing: {subdir}"
            assert (subdir / "__init__.py").exists(), f"__init__.py missing in {subdir}"
    
    def test_data_files_migrated(self):
        """Test data files are in correct location"""
        root = self.get_project_root()
        data_dir = root / "data"
        
        # Data should still be in root/data (not in src)
        assert data_dir.exists()
        assert (data_dir / "processed").exists()
        assert (data_dir / "source").exists()
    
    def test_scripts_migrated(self):
        """Test scripts use new package imports"""
        root = self.get_project_root()
        scripts_dir = root / "scripts"
        
        for script_file in scripts_dir.glob("*.py"):
            if script_file.name == "__init__.py":
                continue
                
            content = script_file.read_text()
            
            # Should not import old packages
            assert "from asma_al_husna_cli" not in content
            assert "from asma_core" not in content
            assert "import asma_al_husna_cli" not in content
            assert "import asma_core" not in content
            
            # Should use new package imports
            if "from aysekai" in content or "import aysekai" in content:
                # If it imports aysekai, verify it's valid
                try:
                    # Parse the file to check syntax
                    ast.parse(content)
                except SyntaxError as e:
                    pytest.fail(f"Syntax error in {script_file}: {e}")
```

### Create test file: `tests/integration/test_package_migration.py`

```python
import pytest
import subprocess
import sys
from pathlib import Path


class TestPackageMigration:
    """Integration tests for package migration"""
    
    def test_old_imports_removed_globally(self):
        """Test no files in project use old import patterns"""
        root = Path(__file__).parent.parent.parent
        
        old_import_patterns = [
            "from asma_al_husna_cli",
            "import asma_al_husna_cli", 
            "from asma_core",
            "import asma_core",
        ]
        
        # Search all Python files
        python_files = list(root.rglob("*.py"))
        violations = []
        
        for py_file in python_files:
            # Skip test files that might reference old imports
            if "test_package" in str(py_file):
                continue
                
            try:
                content = py_file.read_text()
                for pattern in old_import_patterns:
                    if pattern in content:
                        violations.append((py_file, pattern))
            except UnicodeDecodeError:
                # Skip binary files
                continue
        
        assert len(violations) == 0, f"Old imports found: {violations}"
    
    def test_cli_still_works(self):
        """Test CLI still works after migration"""
        # This would normally run the CLI, but for testing we'll check module
        try:
            from aysekai.cli.main import app
            assert app is not None
        except ImportError as e:
            pytest.fail(f"CLI not working after migration: {e}")
    
    def test_scripts_still_work(self):
        """Test data processing scripts still work"""
        root = Path(__file__).parent.parent.parent
        scripts_dir = root / "scripts"
        
        for script_file in scripts_dir.glob("*.py"):
            if script_file.name == "__init__.py":
                continue
                
            # Try to import/parse the script
            try:
                # Check if it can be imported without errors
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(script_file)],
                    capture_output=True,
                    text=True,
                    cwd=root
                )
                assert result.returncode == 0, f"Script {script_file} has syntax errors: {result.stderr}"
            except Exception as e:
                pytest.fail(f"Script {script_file} cannot be compiled: {e}")
```

## 2. Implementation (GREEN Phase)

### Step 1: Create new package structure in src/aysekai

```bash
# Create missing core modules
mkdir -p src/aysekai/core
mkdir -p src/aysekai/utils
```

### Step 2: Migrate DivineName model to `src/aysekai/core/models.py`

```python
"""Core data models for Aysekai application"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DivineName:
    """Represents one of the 99 Beautiful Names of Allah"""
    
    number: int
    arabic: str
    transliteration: str
    brief_meaning: str
    level_1_sharia: str
    level_2_tariqa: str
    level_3_haqiqa: str
    level_4_marifa: str
    quranic_references: str
    dhikr_formulas: str
    pronunciation_guide: str
    
    def __post_init__(self):
        """Validate divine name data"""
        if not 1 <= self.number <= 99:
            raise ValueError(f"Divine name number must be 1-99, got {self.number}")
        
        if not self.arabic or not self.transliteration:
            raise ValueError("Arabic name and transliteration are required")
    
    @property
    def display_name(self) -> str:
        """Get formatted display name"""
        return f"{self.number}. {self.arabic} ({self.transliteration})"
    
    @property
    def meaning_summary(self) -> str:
        """Get brief meaning summary"""
        return f"{self.transliteration}: {self.brief_meaning}"
    
    def get_level_interpretation(self, level: int) -> Optional[str]:
        """Get interpretation for specific level (1-4)"""
        level_map = {
            1: self.level_1_sharia,
            2: self.level_2_tariqa, 
            3: self.level_3_haqiqa,
            4: self.level_4_marifa,
        }
        return level_map.get(level)


@dataclass 
class MeditationSession:
    """Represents a meditation session"""
    
    divine_name: DivineName
    start_time: str
    user_intention: Optional[str] = None
    session_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate session data"""
        if not isinstance(self.divine_name, DivineName):
            raise ValueError("divine_name must be a DivineName instance")
```

### Step 3: Migrate CSV handler to `src/aysekai/utils/csv_handler.py`

```python
"""CSV handling utilities for Aysekai application"""

import csv
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..core.models import DivineName
from ..core.exceptions import DataError


class AsmaCSVReader:
    """Reader for Asma al-Husna CSV files"""
    
    def __init__(self, csv_path: Path):
        """
        Initialize CSV reader.
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise DataError(f"CSV file not found: {csv_path}")
    
    def read_all(self) -> List[DivineName]:
        """
        Read all divine names from CSV.
        
        Returns:
            List of DivineName objects
        """
        names = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = self._row_to_divine_name(row)
                    if name:
                        names.append(name)
        except Exception as e:
            raise DataError(f"Error reading CSV file {self.csv_path}: {e}")
        
        return names
    
    def _row_to_divine_name(self, row: Dict[str, str]) -> Optional[DivineName]:
        """Convert CSV row to DivineName object"""
        try:
            return DivineName(
                number=int(row.get('Number', 0)),
                arabic=row.get('Arabic', '').strip(),
                transliteration=row.get('Transliteration', '').strip(),
                brief_meaning=row.get('Brief Meaning', '').strip(),
                level_1_sharia=row.get('Level 1 - Shari\'a', '').strip(),
                level_2_tariqa=row.get('Level 2 - Tariqa', '').strip(), 
                level_3_haqiqa=row.get('Level 3 - Haqiqa', '').strip(),
                level_4_marifa=row.get('Level 4 - Ma\'rifa', '').strip(),
                quranic_references=row.get('Quranic References', '').strip(),
                dhikr_formulas=row.get('Dhikr Formulas', '').strip(),
                pronunciation_guide=row.get('Pronunciation Guide', '').strip(),
            )
        except (ValueError, KeyError) as e:
            # Log warning but don't fail entire import
            return None


class AsmaCSVWriter:
    """Writer for Asma al-Husna CSV files"""
    
    def __init__(self, csv_path: Path):
        """
        Initialize CSV writer.
        
        Args:
            csv_path: Path where CSV will be written
        """
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    def write_all(self, names: List[DivineName]) -> None:
        """
        Write divine names to CSV.
        
        Args:
            names: List of DivineName objects to write
        """
        fieldnames = [
            'Number', 'Arabic', 'Transliteration', 'Brief Meaning',
            'Level 1 - Shari\'a', 'Level 2 - Tariqa', 
            'Level 3 - Haqiqa', 'Level 4 - Ma\'rifa',
            'Quranic References', 'Dhikr Formulas', 'Pronunciation Guide'
        ]
        
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for name in names:
                    writer.writerow(self._divine_name_to_row(name))
        except Exception as e:
            raise DataError(f"Error writing CSV file {self.csv_path}: {e}")
    
    def _divine_name_to_row(self, name: DivineName) -> Dict[str, str]:
        """Convert DivineName object to CSV row"""
        return {
            'Number': str(name.number),
            'Arabic': name.arabic,
            'Transliteration': name.transliteration,
            'Brief Meaning': name.brief_meaning,
            'Level 1 - Shari\'a': name.level_1_sharia,
            'Level 2 - Tariqa': name.level_2_tariqa,
            'Level 3 - Haqiqa': name.level_3_haqiqa,
            'Level 4 - Ma\'rifa': name.level_4_marifa,
            'Quranic References': name.quranic_references,
            'Dhikr Formulas': name.dhikr_formulas,
            'Pronunciation Guide': name.pronunciation_guide,
        }
```

### Step 4: Update CLI to use new imports

Update `src/aysekai/cli/main.py`:

```python
"""Main CLI entry point - updated with new package structure"""

import typer
from typing import Optional
from pathlib import Path
import sys
from rich import print as rprint

from .path_resolver import get_path_resolver
from .error_handler import error_boundary, setup_exception_handler
from ..config import get_settings
from ..utils.csv_handler import AsmaCSVReader
from ..core.models import DivineName
# ... rest of imports

# Rest of CLI implementation using new imports
```

### Step 5: Update package `__init__.py` files

Update `src/aysekai/__init__.py`:

```python
"""Aysekai - Islamic meditation CLI using the 99 Beautiful Names of Allah"""

__version__ = "2.0.0"
__author__ = "Aysekai International"
__email__ = "contact@aysekai.com"

from .core.models import DivineName, MeditationSession
from .core.exceptions import AysekaiError, ValidationError, DataError, ConfigurationError

__all__ = [
    "DivineName",
    "MeditationSession", 
    "AysekaiError",
    "ValidationError",
    "DataError",
    "ConfigurationError",
]
```

Update `src/aysekai/core/__init__.py`:

```python
"""Core data models and business logic"""

from .models import DivineName, MeditationSession
from .exceptions import AysekaiError, ValidationError, DataError, ConfigurationError

__all__ = [
    "DivineName",
    "MeditationSession",
    "AysekaiError", 
    "ValidationError",
    "DataError",
    "ConfigurationError",
]
```

Update `src/aysekai/utils/__init__.py`:

```python
"""Utility functions and helpers"""

from .validators import InputValidator
from .csv_handler import AsmaCSVReader, AsmaCSVWriter

__all__ = [
    "InputValidator",
    "AsmaCSVReader",
    "AsmaCSVWriter",
]
```

### Step 6: Update scripts to use new imports

Update all files in `scripts/` directory:

```python
# Example: scripts/extract_all_99_names.py
"""Extract names script - updated imports"""

from pathlib import Path
import sys

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aysekai.utils.csv_handler import AsmaCSVReader, AsmaCSVWriter
from aysekai.core.models import DivineName
from aysekai.cli.path_resolver import get_path_resolver

# Rest of script logic...
```

### Step 7: Remove old package directories

```bash
# After all migration is complete and tests pass
rm -rf asma_al_husna_cli/
rm -rf asma_core/
```

## 3. Verification (REFACTOR Phase)

```bash
# Run tests
pytest tests/unit/test_package/ -v
pytest tests/integration/test_package_migration.py -v

# Check imports work
python -c "from aysekai.core.models import DivineName; print('✓ Core imports work')"
python -c "from aysekai.utils.csv_handler import AsmaCSVReader; print('✓ Utils imports work')"
python -c "from aysekai.cli.main import app; print('✓ CLI imports work')"

# Check no old imports
rg "from asma_al_husna_cli|import asma_al_husna_cli|from asma_core|import asma_core" src/ scripts/ --type py || echo "✓ No old imports found"

# Check types
mypy src/aysekai/core/models.py
mypy src/aysekai/utils/csv_handler.py

# Lint code
ruff check src/aysekai/core/models.py
ruff check src/aysekai/utils/csv_handler.py

# Test CLI still works
python -m aysekai --help
```

## 4. Commit & PR

```bash
# Create feature branch
git checkout -b feature/architecture-package-structure

# Stage changes
git add -A

# Commit with conventional message
git commit -m "feat(architecture): consolidate into modern package structure

- Migrate DivineName model to src/aysekai/core/models.py
- Migrate CSV handlers to src/aysekai/utils/csv_handler.py
- Update all imports to use new aysekai package structure
- Remove old asma_al_husna_cli and asma_core packages
- Add proper __init__.py files with exports
- Update scripts to use new import paths
- Maintain backward compatibility for data files

BREAKING CHANGE: Old package imports no longer work

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push and create PR
git push origin feature/architecture-package-structure
gh pr create \
  --title "Architecture: Consolidate Package Structure" \
  --body "## Summary
This PR consolidates the mixed package structure into a single modern Python package under src/aysekai.

## Architecture Improvements  
- 🏗️ Single coherent package structure
- 🏗️ Proper Python packaging conventions
- 🏗️ Clear module boundaries and responsibilities
- 🏗️ Eliminates import confusion
- 🏗️ Better IDE support and navigation

## Changes
- ✅ Migrate DivineName to aysekai.core.models
- ✅ Migrate CSV handlers to aysekai.utils.csv_handler  
- ✅ Update all import statements throughout codebase
- ✅ Remove old asma_al_husna_cli and asma_core packages
- ✅ Add proper __init__.py exports
- ✅ Update data processing scripts
- ✅ Comprehensive test coverage

## Before/After Structure

### Before (CONFUSING):
\`\`\`
project/
├── asma_al_husna_cli/     # Old CLI package
├── asma_core/             # Old core package  
└── src/aysekai/           # New package (partial)
\`\`\`

### After (CLEAN):
\`\`\`
project/
├── src/aysekai/
│   ├── core/              # Models, business logic
│   ├── utils/             # Utilities, helpers
│   ├── cli/               # CLI components
│   └── config/            # Configuration
└── data/                  # Data files (unchanged)
\`\`\`

## Testing
- ✅ All new imports work correctly
- ✅ No old import references remain
- ✅ CLI functionality preserved
- ✅ Scripts updated and working
- ✅ Integration tests pass

## Checklist
- [x] Package structure consolidated
- [x] All imports updated
- [x] Old packages removed
- [x] Tests passing
- [x] CLI still functional
- [x] Scripts migrated"
```

## Success Criteria

- [x] Single aysekai package structure
- [x] All old imports removed/updated
- [x] DivineName model in aysekai.core.models
- [x] CSV handlers in aysekai.utils
- [x] CLI functionality preserved
- [x] Scripts use new imports
- [x] Comprehensive test coverage
- [x] No circular dependencies

## Next Steps

After PR approval and merge:
1. Update documentation with new import examples
2. Create migration guide for users
3. Update setup.py/pyproject.toml if needed
4. Continue with Phase 2 Task 2: Dependency Injection