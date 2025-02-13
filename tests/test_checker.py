from unittest.mock import patch, MagicMock

import pytest

from pep8_checker_bot.checker import PEP8CheckerBot


@pytest.fixture
def mock_github():
    # Mock the GitHub client
    with patch('github.Github') as mock_github:
        yield mock_github


@pytest.fixture
def mock_subprocess_run():
    # Mock subprocess.run
    with patch('subprocess.run') as mock_run:
        yield mock_run


def test_check_pep8_no_violations(mock_github, mock_subprocess_run):
    # Mock GitHub API
    mock_repo = MagicMock()
    mock_pr = MagicMock()
    mock_pr.get_files.return_value = [MagicMock(filename="file1.py"), MagicMock(filename="file2.py")]
    mock_repo.get_pull.return_value = mock_pr
    mock_github.return_value.get_repo.return_value = mock_repo

    # Mock subprocess.run to simulate no PEP 8 violations
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = ""

    # Initialize the bot with a mock GitHub client
    bot = PEP8CheckerBot("repo_name", mock_github.return_value)
    bot.check_pep8(1)

    # Assertions
    mock_pr.create_issue_comment.assert_called_once_with("✅ PR follows PEP 8! Well done! 🎉")
    mock_subprocess_run.assert_called_once_with(
        ["flake8", "file1.py", "file2.py", "--statistics"], capture_output=True, text=True
    )


def test_check_pep8_with_violations(mock_github, mock_subprocess_run):
    # Mock GitHub API
    mock_repo = MagicMock()
    mock_pr = MagicMock()
    mock_pr.get_files.return_value = [MagicMock(filename="file1.py"), MagicMock(filename="file2.py")]
    mock_repo.get_pull.return_value = mock_pr
    mock_github.return_value.get_repo.return_value = mock_repo

    # Mock subprocess.run to simulate PEP 8 violations
    mock_subprocess_run.return_value.returncode = 1
    mock_subprocess_run.return_value.stdout = "file1.py:1:1: E302 expected 2 blank lines, found 1"

    # Initialize the bot with a mock GitHub client
    bot = PEP8CheckerBot("repo_name", mock_github.return_value)
    bot.check_pep8(1)

    # Assertions
    mock_pr.create_issue_comment.assert_called_once_with(
        "❌ PEP 8 violations found:\n```\nfile1.py:1:1: E302 expected 2 blank lines, found 1\n```"
    )
    mock_subprocess_run.assert_called_once_with(
        ["flake8", "file1.py", "file2.py", "--statistics"], capture_output=True, text=True
    )
