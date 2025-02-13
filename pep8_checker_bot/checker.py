import os
import subprocess

from github import Github


class PEP8CheckerBot:
    def __init__(self, repo_name, github_client):
        """
        Initialize the bot with a repo name and a GitHub client.
        :param repo_name: The name of the repository (e.g., "owner/repo").
        :param github_client: An instance of the GitHub client.
        """
        self.repo_name = repo_name
        self.github_client = github_client
        self.repo = self.github_client.get_repo(repo_name)

    def check_pep8(self, pr_number):
        """Runs flake8 on PR files and comments on violations"""
        pr = self.repo.get_pull(pr_number)
        files = [f.filename for f in pr.get_files()]

        # Run PEP 8 check only on changed files
        result = subprocess.run(["flake8", *files, "--statistics"], capture_output=True, text=True)

        if result.returncode == 0:
            pr.create_issue_comment("✅ PR follows PEP 8! Well done! 🎉")
        else:
            pr.create_issue_comment(f"❌ PEP 8 violations found:\n```\n{result.stdout}\n```")


if __name__ == "__main__":
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    REPO_NAME = os.getenv("GITHUB_REPO")
    PR_NUMBER = int(os.getenv("PR_NUMBER"))

    # Initialize the GitHub client and bot
    client = Github(GITHUB_TOKEN)
    bot = PEP8CheckerBot(REPO_NAME, client)
    bot.check_pep8(PR_NUMBER)
