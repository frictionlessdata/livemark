import os
from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    def prepare_document(self, document):
        try:
            repo = Repo(os.path.dirname(document.source))
            data = parse(repo.remote().url)
            document.plugin_config.setdefault("user", data.owner)
            document.plugin_config.setdefault("repo", data.repo)
        except Exception:
            pass
