import importlib
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    identity = "github"
    validity = {
        "type": "object",
        "required": ["user", "repo"],
        "properties": {
            "user": {"type": "string"},
            "repo": {"type": "string"},
        },
    }

    def __init__(self, document):
        super().__init__(document)

        # Infer data
        try:
            git = importlib.import_module("git")
            repo = git.Repo()
            pack = parse(repo.remote().url)
            self.__data = {"user": pack.owner, "repo": pack.repo}
        except Exception:
            self.__data = {}

    # Context

    @property
    def user(self):
        return self.config.get("user", self.__data.get("user"))

    @property
    def repo(self):
        return self.config.get("repo", self.__data.get("repo"))

    @property
    def base_url(self):
        if self.user and self.repo:
            return f"https://github.com/{self.user}/{self.repo}"

    @property
    def report_url(self):
        if self.base_url:
            return f"{self.base_url}/issues"

    @property
    def fork_url(self):
        if self.base_url:
            return f"{self.base_url}/fork"

    @property
    def edit_url(self):
        if self.base_url:
            return f"{self.base_url}/edit/main/{self.document.source}"
