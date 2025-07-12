# Contributing to Aysekai International

Thank you for your interest in contributing to the Aysekai International Islamic Meditation CLI! This project combines spiritual practice with modern technology, and we welcome contributions that maintain the highest standards of both technical excellence and respectful treatment of sacred content.

## 🙏 Sacred Content Guidelines

This project handles sacred Islamic content - the 99 Beautiful Names of Allah. All contributors must:

- **Treat content with reverence**: Maintain respectful handling of Arabic text and Islamic concepts
- **Verify accuracy**: Ensure transliterations and meanings are accurate
- **Preserve authenticity**: Don't modify sacred content without proper Islamic scholarly guidance
- **Cultural sensitivity**: Be mindful of Islamic practices and traditions

## 🏗️ Architecture Standards

This project follows enterprise-grade architecture patterns. Please familiarize yourself with:

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Comprehensive technical architecture guide
- **Dependency Injection**: All services use DI patterns
- **Clean Architecture**: Clear separation of concerns
- **Test-Driven Development**: Tests drive design decisions

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/aysekai-international.git
   cd aysekai-international
   ```

2. **Set up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   pytest tests/ -v
   
   # Run linting
   ruff check src/
   mypy src/ --ignore-missing-imports
   
   # Test CLI
   python -m src.aysekai.cli.main about
   ```

### Development Tools

- **Linting**: `ruff` for code formatting and style
- **Type Checking**: `mypy` for static type analysis
- **Testing**: `pytest` with comprehensive test suite
- **Coverage**: `pytest-cov` for test coverage reporting

## 🧪 Test-Driven Development

We follow strict TDD practices:

### TDD Cycle

1. **RED**: Write a failing test that defines the desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Clean up code while maintaining tests

### Example TDD Workflow

```bash
# 1. RED - Write failing test
echo "def test_new_feature():
    assert new_feature() == expected_result" >> tests/unit/test_new_feature.py

# Run test (should fail)
pytest tests/unit/test_new_feature.py -v

# 2. GREEN - Implement minimal solution
# Add implementation to make test pass

# 3. REFACTOR - Clean up while keeping tests green
# Improve code quality, add error handling, etc.
```

### Test Standards

- **95%+ Coverage**: Maintain high test coverage
- **All Scenarios**: Test both success and failure paths
- **Mock External Dependencies**: Use DI for clean test isolation
- **Clear Test Names**: Descriptive test method names
- **Arrange-Act-Assert**: Follow AAA pattern

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src/aysekai --cov-report=term-missing

# Run specific test categories
pytest tests/unit/test_di/ -v           # Dependency injection
pytest tests/unit/test_cli/ -v          # CLI tests
pytest tests/integration/ -v           # Integration tests

# Run tests for specific file
pytest tests/unit/test_cli/test_error_handler.py -v

# Run single test
pytest tests/unit/test_di/test_container.py::TestDIContainer::test_container_creation -v
```

## 🏗️ Code Standards

### Architecture Patterns

- **Dependency Injection**: Use DI container for all service dependencies
- **Protocol-Based Interfaces**: Define clear contracts using Protocol classes
- **Error Boundaries**: Wrap operations with proper error handling
- **Single Responsibility**: Each class/function has one clear purpose

### Code Quality

- **Type Hints**: All functions must have complete type annotations
- **Docstrings**: Public APIs require comprehensive docstrings
- **Error Handling**: Graceful error handling with user-friendly messages
- **Security**: Input validation, no hardcoded secrets, secure file operations

### Style Guidelines

```python
# Good: Type hints, clear naming, proper error handling
def process_divine_name(
    name: DivineName, 
    validator: InputValidator = Depends()
) -> ProcessedName:
    """Process a divine name with validation and formatting.
    
    Args:
        name: The divine name to process
        validator: Injected validation service
        
    Returns:
        Processed name with formatting applied
        
    Raises:
        ValidationError: If name data is invalid
    """
    try:
        validated_name = validator.validate_name(name)
        return ProcessedName(validated_name)
    except ValidationError as e:
        log_error(f"Name validation failed: {e}")
        raise

# Bad: No types, unclear naming, poor error handling
def process(n):
    return ProcessedName(n)
```

### Linting and Formatting

```bash
# Run all quality checks
ruff check src/                    # Linting
mypy src/ --ignore-missing-imports # Type checking
pytest tests/ --cov=src/aysekai   # Test coverage
```

**Pre-commit Checklist:**
- [ ] All tests pass
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Coverage maintained above 95%
- [ ] Documentation updated

## 📝 Pull Request Process

### Before Creating PR

1. **Branch Naming**
   ```bash
   git checkout -b feature/meaningful-feature-name
   git checkout -b fix/specific-bug-description
   git checkout -b docs/documentation-update
   ```

2. **Commit Standards**
   ```bash
   # Good commit messages
   git commit -m "feat: add dependency injection for meditation services"
   git commit -m "fix: handle empty CSV files gracefully"
   git commit -m "docs: update architecture documentation for DI system"
   git commit -m "test: add comprehensive error handling tests"
   ```

3. **Quality Checks**
   ```bash
   # Ensure all checks pass
   pytest tests/ -v --cov=src/aysekai --cov-report=term-missing
   ruff check src/
   mypy src/ --ignore-missing-imports
   ```

### PR Requirements

- [ ] **Tests**: All new functionality has comprehensive tests
- [ ] **Documentation**: Architecture docs updated for significant changes
- [ ] **Backwards Compatibility**: No breaking changes without major version bump
- [ ] **Performance**: No significant performance regressions
- [ ] **Security**: All inputs validated, no hardcoded secrets
- [ ] **Sacred Content**: Respectful treatment of Islamic content maintained

### PR Template

```markdown
## Summary
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to not work)
- [ ] Documentation update

## Testing
- [ ] Added tests for new functionality
- [ ] All existing tests pass
- [ ] Coverage maintained above 95%

## Architecture Impact
- [ ] Follows dependency injection patterns
- [ ] Maintains clean architecture principles
- [ ] Updates ARCHITECTURE.md if needed

## Sacred Content
- [ ] Respectful treatment of Islamic content maintained
- [ ] Accuracy of translations/transliterations verified
- [ ] No modifications to sacred text without proper guidance

## Checklist
- [ ] Self-review completed
- [ ] Code follows project style guidelines
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Documentation updated
```

## 🐛 Bug Reports

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Go to...
2. Click on...
3. Scroll down to...
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. macOS 13.0]
- Python Version: [e.g. 3.11]
- Application Version: [e.g. 2.0.0]

**Additional Context**
Any other context about the problem.

**Sacred Content Impact**
Does this bug affect Islamic content display or accuracy?
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the requested feature.

**Use Case**
Why would this feature be valuable?

**Proposed Implementation**
How might this feature work?

**Alternatives Considered**
Other approaches you've thought about.

**Sacred Content Considerations**
How does this feature relate to Islamic content?

**Architecture Impact**
How might this affect the current architecture?
```

## 🔧 Development Workflow

### Feature Development

1. **Planning**
   - Discuss feature in issue before implementation
   - Consider architecture impact
   - Plan test strategy

2. **Implementation**
   ```bash
   # Create feature branch
   git checkout -b feature/new-meditation-mode
   
   # TDD cycle
   # 1. Write failing tests
   pytest tests/unit/test_new_feature.py -v  # Should fail
   
   # 2. Implement feature
   # Add minimal code to pass tests
   
   # 3. Refactor
   # Clean up code while keeping tests green
   
   # Quality checks
   ruff check src/
   mypy src/ --ignore-missing-imports
   pytest tests/ --cov=src/aysekai
   ```

3. **Integration**
   ```bash
   # Update from main
   git checkout main
   git pull origin main
   git checkout feature/new-meditation-mode
   git rebase main
   
   # Final testing
   pytest tests/ -v
   
   # Create PR
   git push origin feature/new-meditation-mode
   ```

### Debugging

```bash
# Run specific failing test with verbose output
pytest tests/unit/test_cli/test_error_handler.py::TestErrorHandler::test_validation_error -v -s

# Run with debugger
pytest tests/unit/test_cli/test_error_handler.py --pdb

# Check type issues
mypy src/aysekai/cli/main.py

# Lint specific file
ruff check src/aysekai/cli/main.py
```

## 📚 Documentation Standards

### Code Documentation

- **Public APIs**: Complete docstrings with examples
- **Complex Logic**: Inline comments explaining why, not what
- **Architecture Changes**: Update ARCHITECTURE.md
- **New Features**: Update README.md

### Example Documentation

```python
class MeditationSession:
    """Represents a meditation session with a divine name.
    
    This class encapsulates all information about a meditation session,
    including the selected divine name, user intention, and session metadata.
    
    Attributes:
        divine_name: The selected divine name for meditation
        start_time: ISO format timestamp when session started
        user_intention: Optional user-provided intention
        session_id: Unique identifier for the session
        
    Example:
        >>> name = DivineName(number=1, arabic="الرحمن", ...)
        >>> session = MeditationSession(
        ...     divine_name=name,
        ...     start_time="2024-01-01T10:00:00",
        ...     user_intention="seeking peace"
        ... )
        >>> print(session.divine_name.transliteration)
        Ar-Rahman
    """
```

## 🔒 Security Guidelines

### Input Validation

- **All Inputs**: Validate and sanitize all user inputs
- **File Paths**: Prevent path traversal attacks
- **Error Messages**: Don't expose sensitive information

### Secrets Management

- **No Hardcoded Secrets**: Use environment variables
- **Configuration**: Secure defaults for all settings
- **Logging**: Exclude sensitive data from logs

### Example Secure Code

```python
# Good: Proper validation and error handling
def validate_user_intention(intention: str) -> str:
    """Validate and sanitize user intention input."""
    if not intention:
        raise ValidationError("Intention cannot be empty")
    
    # Remove control characters
    cleaned = re.sub(r'[\x00-\x1f\x7f]', '', intention)
    
    # Limit length
    if len(cleaned) > MAX_INTENTION_LENGTH:
        raise ValidationError(f"Intention too long (max {MAX_INTENTION_LENGTH})")
    
    return cleaned.strip()

# Bad: No validation
def process_intention(intention):
    return intention
```

## 🌍 Community Guidelines

- **Respectful Communication**: Professional and kind interactions
- **Inclusive Environment**: Welcome contributors from all backgrounds
- **Islamic Sensitivity**: Respect for Islamic practices and traditions
- **Constructive Feedback**: Focus on code improvement, not personal criticism
- **Learning Mindset**: Help others learn and grow

## ❓ Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: Through pull request process
- **Architecture Questions**: Reference ARCHITECTURE.md first

## 🏆 Recognition

Contributors who make significant contributions will be:
- Listed in the project's contributors section
- Recognized in release notes
- Invited to participate in architectural decisions

---

## 📞 Contact

For questions about contributing:
- Open a GitHub issue
- Start a GitHub discussion
- Review existing documentation

Thank you for contributing to this meaningful intersection of technology and spirituality! 🌙

---

*"And whoever does righteous deeds, whether male or female, while being a believer - those will enter Paradise and will not be wronged, [even as much as] the speck on a date seed."* - Quran 4:124