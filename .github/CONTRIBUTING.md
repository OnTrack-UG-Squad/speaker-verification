# Contributing to speaker-verification 

## Pull Requests

- [GitHub Flow](https://guides.github.com/introduction/flow/index.html)
- [Strive for Schemantic/Conventional Commits](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
  - Like labels for your commits to help contextualise the contents of the commits.
- [Code Reviews](https://google.github.io/eng-practices/review/reviewer/)
  - Each Pull Request must have merging approval of at least one (ideally multiple) senior members before merging to main branch.
  - Do not delete branches until the end of assessment each trimester.

## Continuous Integration (CI)

- [GitHub Actions](https://github.com/features/actions)
  - Our CI is currently running tests with `pytest` and `codeQL` for security checks.
- [pytest](https://docs.pytest.org/en/stable/)
  - We develop our tests with pytest and use pytest-cov to generate coverage reports.
  - Tests in the repository should be passing to be merged into `main` or `development`.
  - Added functionality or methods should have tests in order to keep coverage consistant.

## Auto-formatting

- [Black code formatter](https://black.readthedocs.io/en/stable/)
  - Use the `--line-length` argument to format to 90 characters per line.
- [PEP8 guide](https://www.python.org/dev/peps/pep-0008/)
  - Python style guide to follow to create readable and maintainable code.

## Environment

- pip/conda
  - Follow the install guide [README](../README.md#installation).

## Development Principles

- [Dry vs Wet](https://medium.com/@nrk25693/dry-or-wet-and-why-867ac3096483)
- [What is DRY code?](https://codinglead.github.io/javascript/what-is-DRY-code)
- [Simplicity Over Complexity](https://en.wikipedia.org/wiki/Zen_of_Python)
- [Readability Over Optimisation](https://en.wikiquote.org/wiki/Donald_Knuth#Computer_Programming_as_an_Art_(1974))

