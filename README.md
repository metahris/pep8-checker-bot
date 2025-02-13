# Pep8 Checker Bot

`pep8-checker-bot` is a GitHub bot that checks PEP 8 compliance for Python files in pull requests.

### 1. Add the Bot to your dependencies

`git+https://github.com/metahris/pep8-bot-checker.git`

### 2. Set Up GitHub Actions

Example of a Workflow file `.github/workflows/pep8-check.yml`:

```yaml
name: PEP8 Check

on:
  pull_request:
    paths:
      - '**/*.py'  # Trigger the action only for Python files

jobs:
  check-pep8:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout the repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'  # Specify the Python version needed

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run PEP8 Bot
        run: |
          export GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}  # GitHub automatically provides this token
          export GITHUB_REPO=${{ github.repository }}
          export PR_NUMBER=${{ github.event.pull_request.number }}
          python -m pep8_checker_bot.checker  # Runs the checker script
```