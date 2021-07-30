from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    profile = {
        "type": "object",
        "required": ["user", "repo", "edit_url", "report_url"],
        "properties": {
            "user": {"type": "string"},
            "repo": {"type": "string"},
            "edit_url": {"type": "string"},
            "report_url": {"type": "string"},
        },
    }

    def process_config(self, config):

        # Infer github
        if not self.config:
            try:
                repo = Repo()
                data = parse(repo.remote().url)
                self.config["user"] = data.owner
                self.config["repo"] = data.repo
            except Exception:
                pass

        # Update config
        if self.config:
            url = f"https://github.com/{self.config['user']}/{self.config['repo']}"
            self.config["edit_url"] = f"{url}/edit/main/{self.document.source}"
            self.config["fork_url"] = f"{url}/fork"
            self.config["report_url"] = f"{url}/issues"
