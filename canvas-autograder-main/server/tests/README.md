# Canvas Autograder - Test Suite

This directory contains the comprehensive test suite for the Canvas Autograder backend.

## Overview

The test suite covers all major components of the autograder:
- **grader.py**: Tests for Python, Java, and C++ code grading
- **repo_utils.py**: Tests for Git repository cloning
- **github_utils.py**: Tests for GitHub API integration
- **server.py**: Tests for Flask API endpoints

## Setup

### Install Testing Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking utilities
- `responses` - HTTP mocking for API tests

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

### Run Specific Test Files

```bash
# Test only grader functionality
pytest tests/test_grader.py

# Test only server endpoints
pytest tests/test_server.py

# Test only repo utilities
pytest tests/test_repo_utils.py

# Test only GitHub utilities
pytest tests/test_github_utils.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_grader.py::TestGradePython

# Run a specific test function
pytest tests/test_grader.py::TestGradePython::test_grade_python_all_pass
```

### Run Tests with Different Verbosity

```bash
# Minimal output
pytest -q

# Verbose output (default)
pytest -v

# Very verbose output
pytest -vv
```

### Skip Slow Tests

Some tests (like large repo cloning) are marked as slow:

```bash
# Skip slow tests
pytest -m "not slow"

# Run only slow tests
pytest -m "slow"
```

## Test Organization

```
tests/
├── __init__.py           # Makes tests a package
├── conftest.py           # Shared fixtures and test configuration
├── test_grader.py        # Tests for grading functions
├── test_repo_utils.py    # Tests for repository utilities
├── test_github_utils.py  # Tests for GitHub API integration
├── test_server.py        # Tests for Flask endpoints
└── fixtures/             # Test data and sample files
```

## Fixtures

Common test fixtures are defined in `conftest.py`:

- `temp_dir` - Temporary directory for test files
- `sample_python_script` - Sample Python script that echoes input
- `sample_python_add_script` - Sample Python script that adds numbers
- `sample_java_script` - Sample Java program
- `sample_cpp_script` - Sample C++ program
- `sample_test_cases` - Standard test cases for grading
- `sample_add_test_cases` - Test cases for addition programs

## Test Coverage

Current test coverage includes:

### Grader Tests (test_grader.py)
- ✅ Python grading with all passing tests
- ✅ Python grading with partial passing tests
- ✅ Python grading with all failing tests
- ✅ Java compilation and grading
- ✅ C++ compilation and grading
- ✅ Timeout handling
- ✅ Syntax error handling
- ✅ Runtime error handling
- ✅ Edge cases (zero points, missing fields, whitespace)

### Repository Tests (test_repo_utils.py)
- ✅ Cloning valid repositories
- ✅ Removing existing directories before cloning
- ✅ Invalid URL handling
- ✅ Malformed URL handling
- ✅ Nested path handling
- ✅ Commit history preservation
- ✅ Special characters in paths
- ✅ Idempotency (cloning same repo twice)

### GitHub Utils Tests (test_github_utils.py)
- ✅ Fetching last commit date
- ✅ Handling .git extension in URLs
- ✅ Handling trailing slashes
- ✅ Empty repository handling
- ✅ API error handling (404, 403)
- ✅ Rate limit handling
- ✅ Multiple commits (returns most recent)
- ✅ Invalid URL formats
- ✅ Connection error handling

### Server Tests (test_server.py)
- ✅ Hello endpoint
- ✅ Submit URL with Python code
- ✅ Submit URL with Java code
- ✅ Submit URL with C++ code
- ✅ Missing URL error handling
- ✅ Invalid test cases error handling
- ✅ Clone failure handling
- ✅ Main file not found handling
- ✅ Grading exception handling
- ✅ Partial test pass scenarios
- ✅ Zero points handling
- ✅ Default language (Python)
- ✅ Invalid endpoint handling

## Writing New Tests

### Example Test Structure

```python
import pytest
from utils.grader import grade_python

class TestNewFeature:
    """Tests for new feature."""

    def test_basic_functionality(self, sample_python_script):
        """Test that basic functionality works."""
        # Arrange
        test_cases = [{"input": "test", "expected_output": "test", "points": 10}]

        # Act
        results, total, earned = grade_python(sample_python_script, test_cases)

        # Assert
        assert earned == 10
        assert results[0]["passed"] is True
```

### Using Mocks

```python
from unittest.mock import patch

@patch('server.clone_repo')
def test_with_mock(mock_clone, client):
    """Test using mocked dependencies."""
    mock_clone.return_value = None
    # ... rest of test
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Example GitHub Actions workflow:

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=. --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Java/C++ Tests Failing

Ensure you have Java JDK and g++ installed:

```bash
# Check Java
javac -version

# Check g++
g++ --version
```

### Tests Taking Too Long

Skip slow tests during development:

```bash
pytest -m "not slow"
```

### Import Errors

Make sure you're running pytest from the `server/` directory:

```bash
cd canvas-autograder-main/server
pytest
```

## Best Practices

1. **Keep tests independent** - Each test should be able to run in isolation
2. **Use descriptive names** - Test names should clearly describe what they test
3. **Test edge cases** - Don't just test the happy path
4. **Mock external dependencies** - Use mocks for network calls, file system, etc.
5. **Clean up resources** - Use fixtures to ensure cleanup happens
6. **Keep tests fast** - Mark slow tests with `@pytest.mark.slow`
7. **Maintain good coverage** - Aim for >80% code coverage

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure all tests pass: `pytest`
3. Check coverage: `pytest --cov=.`
4. Add any new fixtures to `conftest.py`
5. Update this README if adding new test categories

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Responses Library](https://github.com/getsentry/responses)
