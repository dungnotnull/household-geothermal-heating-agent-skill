# Contributing to household-geothermal-heating

Thank you for your interest in contributing to the `household-geothermal-heating` skill! This document provides guidelines for contributing to this bulletproof, production-grade project.

## Project Overview

`household-geothermal-heating` is a professional-grade Claude Code harness for **Small-Scale Geothermal Heat Pump Engineering**. It features a modular architecture with production-grade logging, configuration management, and comprehensive testing.

## Code of Conduct

- Be respectful and constructive
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Bug Report Template**:
```markdown
**Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. Execute skill with '...'
3. Scroll to '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- Claude Code Version: [e.g., 1.0.0]
- Skill Version: [e.g., 1.1.0]

**Logs**
Attach relevant logs from `logs/skill_execution.log` with sensitive data redacted.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Enhancement Request Template**:
```markdown
**Problem Description**
A clear description of what the problem is.

**Proposed Solution**
A clear description of what you want to happen.

**Alternatives Considered**
A clear description of any alternative solutions or features you've considered.

**Additional Context**
Any other context, screenshots, or examples about the feature request.
```

### Pull Requests

**Workflow**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python tools/run_test_scenarios.py --all`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**PR Checklist**:
- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] PR description explains the change

### Code Style

**Python Code**:
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Add docstrings for functions and classes
- Keep functions under 50 lines when possible
- Use descriptive variable names

**Markdown Documentation**:
- Use proper heading hierarchy (# ## ###)
- Add tables for structured data
- Include code examples with syntax highlighting
- Link to related documentation

### Testing

**Running Tests**:
```bash
# Run all tests
python tools/run_test_scenarios.py --all

# Run specific test section
python tools/run_test_scenarios.py --section files

# Run with verbose output
python tools/run_test_scenarios.py --all --verbose

# Test knowledge updater
python tools/test_knowledge_updater.py
```

**Writing Tests**:
- Add test scenarios to `tests/test-scenarios.md`
- Update `tools/run_test_scenarios.py` for new validation checks
- Ensure 100% gate coverage
- Test both success and failure cases

### Documentation

**Documentation Files**:
- `README.md` - User-facing documentation
- `PROJECT-detail.md` - Technical specification
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - This file

**When to Update Documentation**:
- Adding new features → Update README.md
- Changing architecture → Update PROJECT-detail.md
- Releasing version → Update CHANGELOG.md
- Changing contribution process → Update CONTRIBUTING.md

## Development Setup

### Environment Setup

```bash
# Clone repository
git clone https://github.com/your-org/248-household-geothermal-heating.git
cd 248-household-geothermal-heating

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Configuration

```bash
# Copy example configuration
cp config/config.json config/config.local.json

# Edit for local development
# Edit config/config.local.json
```

### Running Locally

```bash
# Via Python harness
python tools/harness.py --location "Denver, CO" --area 186 --type design

# Via Claude Code (after skill installation)
/household-geothermal-heating Design a system for my house in Denver

# Test knowledge update
python tools/knowledge_updater.py --dry-run
```

## Project Structure

```
248-household-geothermal-heating/
├── config/           # Configuration management
├── scripts/          # Automation & utilities
├── references/       # Documentation
├── assets/          # Diagrams & schemas
├── skills/          # Skill definitions
├── tools/           # Python utilities
├── tests/           # Test suite
└── logs/            # Runtime logs (created on first run)
```

## Release Process

1. Update version in `config/config.json`
2. Update `CHANGELOG.md` with new version
3. Update `README.md` with new features
4. Run full test suite and ensure all tests pass
5. Create Git tag (`git tag v1.x.x`)
6. Push to GitHub (`git push && git push --tags`)
7. Create GitHub Release
8. Update `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`

## Community Guidelines

### Getting Help

- GitHub Issues: For bugs and feature requests
- GitHub Discussions: For questions and ideas
- Documentation: Check `PROJECT-detail.md` for technical details

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation for major contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Skill Library Standards](../SKILL-STANDARD.md)
- [Project Technical Spec](PROJECT-detail.md)
- [Development Tracking](PROJECT-DEVELOPMENT-PHASE-TRACKING.md)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-07-27
