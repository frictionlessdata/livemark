import os
from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    priority = 20

    def process_document(self, document):
        try:
            repo = Repo(os.path.dirname(document.source))
            data = parse(repo.remote().url)
            user = document.plugin_config.setdefault("user", data.owner)
            repo = document.plugin_config.setdefault("repo", data.repo)
            url = f"https://github.com/{user}/{repo}"
            document.plugin_config["report_url"] = f"{url}/issues"
            document.plugin_config["edit_url"] = f"{url}/edit/main/{document.source}"
        except Exception:
            pass
