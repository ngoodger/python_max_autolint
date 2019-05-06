# python_max_autolint
Code autoformatting and linting using Python Black and Flake8.  Aims for maximum automation.

ASSUMPTIONS:
* Modifiers are configured in compatible way.
* Modifiers maintain the original Abstract Syntax Tree (AST)

1. Get file set for modification from git.
2. Run isort.
2. Run black.
3. Run checkers in parallel.
FileSet
