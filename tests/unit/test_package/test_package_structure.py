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