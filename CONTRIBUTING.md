# Contributing to Confy Addons

Thank you for considering contributing to **Confy Addons**! This project was developed with dedication by Brazilian students 🇧🇷 and we value all contributions, whether they are bug fixes, new features, documentation improvements, or tests.

To ensure an organized workflow and a good experience for everyone, please follow the guidelines below.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Environment Setup](#development-environment-setup)
4. [Project Structure](#project-structure)
5. [Contribution Workflow](#contribution-workflow)
6. [Code Standards](#code-standards)
7. [Quality Tools](#quality-tools)
8. [Testing](#testing)
9. [Running the Project Locally](#running-the-project-locally)
10. [Creating a Pull Request](#creating-a-pull-request)
11. [Review Process](#review-process)
12. [Reporting Security Issues](#reporting-security-issues)

## Code of Conduct

We are committed to maintaining a welcoming, safe, and collaborative environment. Everyone should be treated with respect, regardless of age, gender identity, sexual orientation, ethnicity, religion, or experience level.

**Unacceptable behaviors include:**

- Harassment, discrimination, or insults
- Sexualized language or content
- Threats or personal attacks
- Unauthorized disclosure of private information

To report violations, contact: [confy@henriquesebastiao.com](mailto:confy@henriquesebastiao.com)

## Getting Started

### Prerequisites

Before you begin, make sure you have:

- **Git** installed and configured
- **Python 3.9.2 or higher** (we support up to Python 3.14)
- **Poetry** for dependency management (recommended)
- A **GitHub** account

### Verify Your Installation

```bash
python --version
poetry --version
git --version
```

## Development Environment Setup

### 1. Fork the Repository

1. Go to [github.com/confy-security/confy-addons](https://github.com/confy-security/confy-addons)
2. Click the **"Fork"** button in the top right corner
3. This will create a copy of the repository in your account

### 2. Clone Your Fork Locally

```bash
git clone https://github.com/YOUR-USERNAME/confy-addons.git
cd confy-addons
```

### 3. Add the Original Repository as a Remote

```bash
git remote add upstream https://github.com/confy-security/confy-addons.git
git remote -v  # Verify you have 'origin' and 'upstream'
```

### 4. Install Dependencies with Poetry

```bash
poetry install
```

This command will:

- Create a virtual environment (if it doesn't exist)
- Install all main and development dependencies
- Automatically activate the virtual environment

### 5. Activate the Virtual Environment

If the environment was not activated automatically:

```bash
poetry shell
```

Or execute commands within the environment with:

```bash
poetry run <command>
```

## Project Structure

```txt
confy-addons/
├── .github/
│   ├── CODEOWNERS              # Code owners
│   ├── dependabot.yml          # Dependabot configuration
│   └── workflows/
│       ├── test.yml            # Test pipeline
│       ├── publish.yml         # Publishing pipeline
│       └── smokeshow.yml       # Test coverage
├── confy_addons/
│   ├── __init__.py             # Main exports
│   ├── core/
│   │   ├── abstract.py         # Abstract classes
│   │   ├── constants.py        # Project constants
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── mixins.py           # Reusable mixins
│   ├── encryption/
│   │   ├── __init__.py
│   │   ├── aes.py              # AES implementation
│   │   └── rsa.py              # RSA implementation
│   └── prefixes.py             # Message prefixes
├── tests/
│   ├── __init__.py
│   ├── test_abstract.py
│   ├── test_aes.py
│   ├── test_encryption_mixin.py
│   ├── test_prefizes.py
│   └── test_rsa.py
├── pyproject.toml              # Poetry and project config
├── CONTRIBUTING.md             # This file
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── README.md
└── LICENSE
```

## Contribution Workflow

### 1. Create a Branch for Your Changes

Always create a separate branch for each contribution:

```bash
# Update from the main branch
git checkout main
git pull upstream main

# Create and switch to a new branch
git checkout -b type/short-description

# Example branch names:
# - feature/add-aes-validation
# - bugfix/fix-decryption-error
# - docs/improve-readme
# - test/increase-rsa-coverage
```

**Branch naming conventions:**

- `feature/` - For new features
- `bugfix/` - For bug fixes
- `docs/` - For documentation improvements
- `test/` - For adding/improving tests
- `refactor/` - For code refactoring

### 2. Make Your Changes

Make changes to the code following the project standards (see [Code Standards](#code-standards) section).

```bash
# Edit files as needed
vim confy_addons/encryption/aes.py

# See the status of changes
git status

# Stage changes
git add .
```

### 3. Commit with Clear Messages

Write descriptive commit messages:

```bash
git commit -m "Add AES key size validation"
```

**Best practices for commit messages:**

- Use the imperative mood ("add" instead of "added")
- Start with a capital letter
- Don't use a period at the end
- Limit the first line to 50 characters
- Add a more detailed description after a blank line if needed

**Complete example:**

```txt
Fix decryption error in CFB mode

- Validate minimum IV size
- Improve error messages
- Add edge case test
```

## Code Standards

The Confy Addons project follows rigorous quality and style standards. Understanding these standards is essential.

### Style and Formatting - Ruff

The project uses **Ruff** for static analysis and code formatting.

**Active rules:**

- `I` - Import sorting
- `F` - Pyflakes errors
- `E` - PEP 8 style errors
- `W` - PEP 8 style warnings
- `PL` - Pylint
- `PT` - Pytest
- `D` - Docstrings (Pydocstyle)
- `UP` - Syntax updates
- `PERF` - Performance optimizations

**Main configurations:**

- Maximum line length: **99 characters**
- Quote style: **Single quotes** (`'`)
- Preview: Enabled (uses experimental Ruff features)

### Style Examples

**✅ Correct:**

```python
"""Module docstring explaining the module."""

from confy_addons.core.constants import AES_KEY_SIZE
from confy_addons.core.exceptions import EncryptionError


class MyEncryption:
    """Docstring for the class."""

    def __init__(self, key: bytes) -> None:
        """Initialize encryption handler.

        Args:
            key: The encryption key.

        Raises:
            TypeError: If key is not bytes.

        """
        if not isinstance(key, bytes):
            raise TypeError('key must be bytes')
        self._key = key

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext string.

        Args:
            plaintext: The text to encrypt.

        Returns:
            str: The encrypted text.

        """
        try:
            # implementation
            return encrypted_text
        except Exception as e:
            raise EncryptionError('Encryption failed') from e
```

**❌ Incorrect:**

```python
# Missing module docstring
from confy_addons.core.exceptions import EncryptionError
from confy_addons.core.constants import AES_KEY_SIZE  # Wrong order

class MyEncryption:
    # Missing class docstring

    def __init__(self, key: bytes) -> None:  # Missing method docstring
        if not isinstance(key, bytes):
            raise TypeError("key must be bytes")  # Double quotes instead of single
        self._key = key

    def encrypt(self, plaintext: str) -> str:  # Missing docstring
        try:
            return encrypted_text
        except Exception as e:
            raise EncryptionError("Encryption failed") from e  # Double quotes
```

### Type Hints

Use type hints in all public methods:

```python
def encrypt(self, plaintext: str) -> str:
    """Encrypt plaintext."""
    ...

def decrypt(self, b64_ciphertext: str) -> str:
    """Decrypt ciphertext."""
    ...

@property
def key(self) -> bytes:
    """Return the encryption key."""
    return self._key
```

### Docstrings

Follow the **Google Style** standard for docstrings:

```python
def method(self, arg1: str, arg2: int) -> bool:
    """Brief description of what the method does.

    Longer description if needed, explaining the behavior
    and any important details.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2.

    Returns:
        bool: Description of return value.

    Raises:
        ValueError: When X condition happens.
        TypeError: When Y type is invalid.

    """
```

### Constants

Use constants for magic values (already defined in `confy_addons/core/constants.py`):

```python
from confy_addons.core.constants import AES_KEY_SIZE, AES_IV_SIZE

# ✅ Correct
key_size = AES_KEY_SIZE

# ❌ Incorrect
key_size = 32  # Magic number!
```

### Logging

Use the `logging` module for messages:

```python
import logging

logger = logging.getLogger(__name__)

# Log at appropriate levels
logger.debug('Debug information')
logger.info('Important information')
logger.warning('Important warning')
logger.error('An error occurred')
```

## Quality Tools

The project uses several tools to ensure quality. All are automatically executed by Taskipy commands.

### Ruff - Code Analysis and Formatting

**Check code:**

```bash
task lint
# or manually:
poetry run ruff check .
```

**Format code automatically:**

```bash
task format
# or manually:
poetry run ruff format .
poetry run ruff check . --fix
```

### MyPy - Type Checking

Checks the correctness of type hints:

```bash
task mypy
# or manually:
poetry run mypy -p confy_addons -p tests
```

**Example of detected error:**

```python
# MyPy will complain about this:
x: int = "string"  # Invalid type
```

### Radon - Code Complexity

Analyzes cyclomatic complexity:

```bash
task radon
# or manually:
poetry run radon cc ./confy_addons -a -na
```

**A** = average | **NA** = non-aggregated (shows details per function)

### Bandit - Security

Checks for security issues:

```bash
task bandit
# or manually:
poetry run bandit -r ./confy_addons
```

## Testing

Tests are fundamental. All pull requests should maintain or increase test coverage.

### Testing Framework - Pytest

The project uses **Pytest** with coverage plugin.

**Test structure:**

- Tests are in `tests/`
- File names: `test_*.py`
- Function names: `test_*`
- One test per aspect/functionality

### Run Tests

**Run all tests:**

```bash
task test
# or manually:
poetry run pytest -s -x --cov=confy_addons -vv
```

**Run tests from a specific file:**

```bash
poetry run pytest tests/test_aes.py -v
```

**Run a specific test:**

```bash
poetry run pytest tests/test_aes.py::test_aes_key_generation_length -v
```

**Run with HTML coverage report:**

```bash
task test
# Coverage HTML will be in: htmlcov/index.html
```

**Useful flags:**

- `-v` or `--verbose` - Verbose mode (shows each test)
- `-s` - Show prints (without capturing stdout)
- `-x` - Stop at first failure
- `--cov=confy_addons` - Measure module coverage
- `--cov-report=html` - Generate HTML report

### Write Tests

**Example of a good test:**

```python
import pytest
from confy_addons import AESEncryption
from confy_addons.core.exceptions import EncryptionError


def test_aes_encrypt_decrypt_roundtrip():
    """Test that encrypt followed by decrypt returns original text."""
    aes = AESEncryption()
    original = 'Hello, World!'
    
    encrypted = aes.encrypt(original)
    decrypted = aes.decrypt(encrypted)
    
    assert decrypted == original


def test_aes_encrypt_invalid_type_raises_error():
    """Test that encrypt raises TypeError with non-string input."""
    aes = AESEncryption()
    
    with pytest.raises(TypeError, match='plaintext must be a str'):
        aes.encrypt(b'bytes-not-allowed')


def test_aes_init_invalid_key_length_raises_error():
    """Test that initializing with wrong key length raises ValueError."""
    with pytest.raises(ValueError, match='AES key must be 32 bytes'):
        AESEncryption(key=b'short-key')
```

**Best practices for tests:**

- One behavior per test
- Descriptive names that explain the test
- Use docstrings to explain the test
- Arrange → Act → Assert
- Test both normal and edge cases
- Test exceptions

## Running the Project Locally

### Pre-test Mode (Before Committing)

Run all checks before committing:

```bash
task pre_test
```

This executes:

1. Ruff (linting)
2. Ruff (format check)
3. MyPy (type checking)

### Complete Development Cycle

```bash
# 1. Make changes to the code
vim confy_addons/encryption/aes.py

# 2. Check style (will be auto-corrected)
task format

# 3. Run tests locally
task test

# 4. Check types
task mypy

# 5. Check security
task bandit

# 6. If all passes, commit
git add .
git commit -m "Your commit message"

# 7. Push to your fork
git push origin feature/your-feature
```

### Troubleshooting

Error: Poetry not found

```bash
pip install poetry
poetry --version
```

Error: Virtual environment not activated

```bash
poetry shell
# or use 'poetry run' before each command
```

## Creating a Pull Request

### 1. Update with the Main Branch

Before pushing, synchronize with the main branch:

```bash
git fetch upstream
git rebase upstream/main
```

If there are conflicts, resolve them and continue:

```bash
git add .
git rebase --continue
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature
```

### 3. Create the Pull Request

1. Go to your fork on GitHub
2. You will see a "Compare & pull request" suggestion
3. Click and fill in the PR template

**PR Template:**

```markdown
## 📝 Description

Brief and clear description of what was changed.

## 🎯 Type of Change

- [ ] Bug fix (fix that doesn't break existing functionality)
- [ ] New feature (adds functionality that doesn't break existing features)
- [ ] Breaking change (alters existing functionality)
- [ ] Documentation
- [ ] Test

## 🔍 Checklist

- [ ] I ran `task format` and the code is formatted
- [ ] I ran `task lint` and there are no errors
- [ ] I ran `task mypy` and there are no type errors
- [ ] I ran `task test` and all tests pass
- [ ] I added tests for new functionality
- [ ] I updated documentation if necessary
- [ ] My PR has no conflicts with the main branch

## 🖼️ Screenshots (if applicable)

If relevant, add screenshots or usage examples.

## 📚 References

Links to related issues or relevant documentation.

Closes #123
```

### 4. Respond to Reviews

Keep the conversation professional and constructive:

- Answer all questions from reviewers
- Make requested changes with new commits
- If you disagree, explain your viewpoint educatedly
- Ask for clarification if you don't understand

## Review Process

### What We Expect

1. **Code follows standards** - Ruff, MyPy, Bandit, Radon
2. **Tests with good coverage** - Minimum 85% coverage
3. **Documentation updated** - Docstrings, README if necessary
4. **Well-structured commits** - Clear and atomic messages
5. **No breaking changes** - Unless intentional

### Review Cycle

1. Submit the PR
2. Automated tests run in CI/CD
3. Team members review the code
4. Changes are requested (if necessary)
5. You make adjustments
6. After approval, the PR is merged

### Respectful Conversation

- Receive feedback as a learning opportunity
- Review others' code constructively
- Use professional and courteous tone
- Focus on the code, not the person

## Reporting Security Issues

⚠️ **DO NOT** report vulnerabilities in public issues.

To report a security vulnerability:

1. **Send an email to:** [confy@henriquesebastiao.com](mailto:confy@henriquesebastiao.com)
2. **Include:**
   - Detailed description of the issue
   - Steps to reproduce
   - Code example if possible
   - Affected version

The team will respond within 48 hours.

## Frequently Asked Questions

### How do I get started?

1. Fork the repository
2. Clone your fork
3. Create a branch (`git checkout -b feature/my-feature`)
4. Make changes and commits
5. Push to your fork
6. Create a Pull Request

### Which Python should I use?

Use **Python 3.9.2 or higher** for development. The project supports up to Python 3.14.

### How many tests should I write?

Write tests for:

- New functionality (normal and edge cases)
- Bug fixes (reproduce the bug before fixing)
- Changes to existing code

Try to maintain coverage above 85%.

### Is my code too slow?

Run Radon to check complexity:

```bash
task radon
```

Refactor if necessary. PRs with very high complexity may be rejected.

### What does each Ruff rule mean?

Check the [Ruff documentation](https://docs.astral.sh/ruff/).

## Useful Resources

- 🔧 [Ruff Documentation](https://docs.astral.sh/ruff/)
- 🧪 [Pytest Documentation](https://docs.pytest.org/)
- 📝 [Poetry Documentation](https://python-poetry.org/docs/)
- 🔐 [Cryptography Library](https://cryptography.io/)

## Thank You!

Your contribution makes this project better. If you have questions, open an issue or contact us through the email above.

**Built with ❤️ by Brazilian students**
