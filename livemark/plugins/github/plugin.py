import os
from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    def prepare_document(self, document):
        try:
            repo = Repo(os.path.dirname(document.source))
            data = parse(repo.remote().url)
            # TODO: rebase on bound document and merge with provided config
            document.config.setdefault("github", {"user": data.owner, "repo": data.repo})
        except Exception:
            pass
