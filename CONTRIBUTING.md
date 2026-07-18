# Contributing to azure-mcp-platform

Thank you for your interest in contributing! This project is a read-only MCP server for Azure infrastructure, built for platform engineers.

## How to Contribute

### Reporting Issues
- Use [GitHub Issues](https://github.com/akkireddy-challa/azure-mcp-platform/issues)
- Include: Python version, OS, Azure SDK version, error message, steps to reproduce

### Proposing New Tools

Open an issue with:
- Tool name and description
- Azure SDK call(s) it would use
- Example use case (especially for platform/AI workloads)
- Read-only guarantee (tools should never mutate Azure state)

### Development Setup

```bash
git clone https://github.com/akkireddy-challa/azure-mcp-platform
cd azure-mcp-platform
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/ -v --cov=server
```

### Code Style

```bash
ruff check . --fix
mypy server.py
```

### Pull Request Guidelines

1. Fork the repo and create a feature branch from `main`
2. Add tests for any new tools
3. Ensure all tools remain read-only
4. Update `README.md` tool table if adding a new tool
5. Run `ruff` and `mypy` before submitting
6. Reference any related issues in the PR description

## Code of Conduct

Be respectful and professional. Harassment of any kind is not tolerated.

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
