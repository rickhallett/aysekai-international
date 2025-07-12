# Phase 2 Task 2: Dependency Injection Implementation

## Overview
Implement proper dependency injection to improve testability, reduce coupling, and make the application more maintainable. This task addresses the tight coupling between CLI commands, data loading, and file access.

## Current Problems
1. **Hard Dependencies**: CLI commands directly instantiate services (DataLoader, RandomSelector)
2. **Difficult Testing**: Hard to mock dependencies for unit testing
3. **Tight Coupling**: CLI layer knows too much about implementation details
4. **Configuration Scattered**: File paths and configuration spread across modules

## Solution Design

### 1. Dependency Container
Create a simple DI container that manages service lifecycle and dependencies.

```python
class DIContainer:
    """Simple dependency injection container"""
    
    def register_singleton(self, interface: Type, implementation: Type)
    def register_factory(self, interface: Type, factory: Callable)
    def get(self, interface: Type) -> Any
    def create_scope(self) -> 'DIContainer'
```

### 2. Service Interfaces
Define clear interfaces for all major services:

```python
# Protocols for dependency injection
class DataReader(Protocol):
    def read_all_names(self) -> List[DivineName]: ...
    def get_name_by_number(self, number: int) -> DivineName: ...

class RandomSelector(Protocol):
    def select_random_name(self, names: List[DivineName], intention: str) -> DivineName: ...

class PathResolver(Protocol):
    def get_data_path(self) -> Path: ...
    def list_csv_files(self) -> List[Path]: ...
```

### 3. Service Implementations
Create concrete implementations that can be easily swapped:

```python
class CSVDataReader:
    def __init__(self, csv_handler: AsmaCSVReader, path_resolver: PathResolver): ...

class UltraRandomSelector:
    def __init__(self, entropy_sources: List[EntropySource]): ...

class ConfigurablePathResolver:
    def __init__(self, settings: Settings): ...
```

### 4. CLI Integration
Inject dependencies into CLI commands rather than creating them:

```python
@app.command()
@inject_dependencies
def meditate(
    data_reader: DataReader = Depends(),
    random_selector: RandomSelector = Depends(),
    session_logger: SessionLogger = Depends(),
    ...
): ...
```

## Implementation Plan

### Phase 1: Core DI Infrastructure
1. Create `src/aysekai/di/` package
2. Implement `DIContainer` class
3. Define service protocols/interfaces
4. Add dependency registration system

### Phase 2: Service Refactoring
1. Extract service interfaces from existing code
2. Create service implementations that accept dependencies
3. Register services in container
4. Add factory functions for complex services

### Phase 3: CLI Integration
1. Create dependency injection decorator for CLI commands
2. Refactor CLI commands to use injected dependencies
3. Remove direct instantiation from CLI layer
4. Add CLI-specific service configurations

### Phase 4: Testing Infrastructure
1. Create test container with mock services
2. Add dependency override capabilities for testing
3. Create test utilities for easy mocking
4. Update existing tests to use DI

## Benefits

### 1. Improved Testability
- Easy to mock dependencies in unit tests
- Can test components in isolation
- Faster test execution with mocked file I/O

### 2. Better Separation of Concerns
- CLI layer only handles user interaction
- Business logic separated from infrastructure
- Configuration centralized in DI container

### 3. Enhanced Flexibility
- Easy to swap implementations (e.g., different data sources)
- Support for different environments (dev, test, prod)
- Plugin architecture possibility

### 4. Reduced Coupling
- Services depend on interfaces, not concrete classes
- Easier to refactor internal implementations
- Better code organization and maintainability

## Testing Strategy

### Unit Tests
```python
def test_meditate_command_with_mocked_dependencies():
    # Arrange
    mock_reader = Mock(spec=DataReader)
    mock_selector = Mock(spec=RandomSelector)
    container = create_test_container({
        DataReader: mock_reader,
        RandomSelector: mock_selector
    })
    
    # Act
    with container.scope():
        result = meditate_command(intention="test")
    
    # Assert
    mock_reader.read_all_names.assert_called_once()
    mock_selector.select_random_name.assert_called_once()
```

### Integration Tests
```python
def test_full_meditation_flow():
    # Test with real implementations but test data
    test_container = create_integration_test_container()
    # ... test full flow
```

## File Structure
```
src/aysekai/
├── di/
│   ├── __init__.py
│   ├── container.py        # DI container implementation
│   ├── interfaces.py       # Service protocols/interfaces
│   ├── decorators.py      # Dependency injection decorators
│   └── registry.py        # Service registration utilities
├── services/
│   ├── __init__.py
│   ├── data_reader.py     # Data reading service
│   ├── random_selector.py # Random selection service
│   ├── session_logger.py  # Session logging service
│   └── path_resolver.py   # Path resolution service
└── cli/
    ├── main.py            # Updated with DI
    └── dependencies.py    # CLI-specific DI setup
```

## Success Criteria
1. ✅ All CLI commands use dependency injection
2. ✅ No direct instantiation in CLI layer
3. ✅ Easy to mock dependencies for testing
4. ✅ Clean separation between interfaces and implementations
5. ✅ All existing functionality preserved
6. ✅ Improved test coverage possible
7. ✅ Code is more maintainable and flexible

## Implementation Notes
- Keep DI simple - avoid over-engineering
- Focus on the most problematic dependencies first
- Maintain backward compatibility during transition
- Add comprehensive tests for DI infrastructure
- Document service contracts clearly