# Contributing to Omni-Sentinel

Thank you for your interest in contributing to Omni-Sentinel! We welcome contributions from the community to help make this project better.

## How to Contribute

1.  **Report Bugs**: If you find a bug, please open an issue on GitHub. Include a detailed description of the bug and steps to reproduce it.
2.  **Suggest Features**: If you have an idea for a new feature, please open an issue to discuss it.
3.  **Submit Pull Requests**:
    - Fork the repository.
    - Create a new branch for your changes (e.g., `feature/awesome-feature` or `bugfix/fix-issue`).
    - Use DCO sign-off: `git commit -s -m "Commit message"`.
    - Write tests for your changes.
    - Ensure all tests pass.
    - Submit a pull request with a clear description of your changes.

## Security-Sensitive Modules

Changes to PQC (Post-Quantum Cryptography) or cryptographic modules require specialized security review. Please highlight any changes to files in `src/infrastructure/` that involve signing or attestation.

## Coding Standards

- Follow PEP 8 for Python code.
- Ensure all functions and classes have descriptive docstrings.
- Keep security and integrity at the forefront of any infrastructure changes.

## Testing

Always run the full test suite before submitting a pull request:

```bash
PYTHONPATH=. python3 tests/test_governance.py
```

## Community

Join our community discussions and help us build a safer environment for cognitive agents!
