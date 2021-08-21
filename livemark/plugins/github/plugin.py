from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    priority = 100
    profile = {
        "type": "object",
        "required": ["user", "repo"],
        "properties": {
            "user": {"type": "string"},
            "repo": {"type": "string"},
        },
    }

    def process_document(self, document):
        self.__user = self.config.get("user")
        self.__repo = self.config.get("repo")

        # Infer locally
        if not self.config:
            try:
                repo = Repo()
                data = parse(repo.remote().url)
                self.__user = data.owner
                self.__repo = data.repo
            except Exception:
                pass

    # Context

    @Plugin.property
    def user(self):
        return self.__user

    @Plugin.property
    def repo(self):
        return self.__repo

    @Plugin.property
    def base_url(self):
        if self.user and self.repo:
            return f"https://github.com/{self.user}/{self.repo}"

    @Plugin.property
    def report_url(self):
        if self.base_url:
            return f"{self.base_url}/issues"

    @Plugin.property
    def fork_url(self):
        if self.base_url:
            return f"{self.base_url}/fork"

    @Plugin.property
    def edit_url(self):
        if self.base_url:
            return f"{self.base_url}/edit/main/{self.document.source}"
