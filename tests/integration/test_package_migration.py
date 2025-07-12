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