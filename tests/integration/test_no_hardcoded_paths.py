import pytest
import ast
import re
from pathlib import Path


class TestNoHardcodedPaths:
    """Integration tests to ensure no hardcoded paths exist"""
    
    def get_python_files(self):
        """Get all Python files in the project"""
        src_dir = Path(__file__).parent.parent.parent / "src"
        return list(src_dir.rglob("*.py"))
    
    def test_no_hardcoded_home_paths(self):
        """Test no hardcoded home directory paths"""
        forbidden_patterns = [
            r"Path\.home\(\)\s*/\s*[\"']Library",
            r"[\"']/Users/",
            r"[\"']~/Library",
            r"com~apple~CloudDocs",
            r"Mobile Documents",
            r"Manual Library",
        ]
        
        pattern = re.compile("|".join(forbidden_patterns))
        
        violations = []
        for py_file in self.get_python_files():
            with open(py_file, 'r') as f:
                content = f.read()
                if pattern.search(content):
                    violations.append(py_file)
        
        assert len(violations) == 0, f"Hardcoded paths found in: {violations}"
    
    def test_path_construction_uses_config(self):
        """Test all path construction uses configuration"""
        required_imports = [
            "from aysekai.config import get_settings",
            "from ..config import get_settings",  # Relative import
            "from aysekai.cli.path_resolver import PathResolver",
            "from ..cli.path_resolver import PathResolver",  # Relative import
        ]
        
        files_using_paths = []
        for py_file in self.get_python_files():
            with open(py_file, 'r') as f:
                content = f.read()
                
                # Skip test files, config, validators, and secure_logger (takes paths as params)
                skip_files = ["settings.py", "validators.py", "secure_logger.py", "path_resolver.py"]
                if "test_" in py_file.name or py_file.name in skip_files:
                    continue
                
                # Check if file constructs absolute paths (not relative)
                hardcoded_patterns = [
                    r'Path\s*\(\s*["\'][^"\']*[/\\]',  # Path("/absolute/path") or Path("C:\\path")
                    r'["\'][/\\][^"\']*["\']',         # "/absolute/path" or "\\absolute\\path"
                ]
                
                has_hardcoded = False
                for pattern in hardcoded_patterns:
                    if re.search(pattern, content):
                        has_hardcoded = True
                        break
                
                if has_hardcoded:
                    files_using_paths.append((py_file, content))
        
        # Verify files using paths import configuration
        for py_file, content in files_using_paths:
            has_config = any(imp in content for imp in required_imports)
            assert has_config, f"{py_file} constructs paths without config import"