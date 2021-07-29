import os
from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    priority = 20
    profile = {
        "type": "object",
        "required": ["user", "repo"],
        "properties": {
            "user": {"type": "string"},
            "repo": {"type": "string"},
        },
    }

    def process_document(self, document):

        # Update config
        try:
            repo = Repo(os.path.dirname(document.source))
            data = parse(repo.remote().url)
            user = self.config.setdefault("user", data.owner)
            repo = self.config.setdefault("repo", data.repo)
            url = f"https://github.com/{user}/{repo}"
            self.config["report_url"] = f"{url}/issues"
            self.config["edit_url"] = f"{url}/edit/main/{document.source}"
        except Exception:
            pass
