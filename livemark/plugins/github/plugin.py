from git import Repo
from giturlparse import parse
from ...plugin import Plugin


class GithubPlugin(Plugin):
    code = "github"
    profile = {
        "type": "object",
        "required": ["user", "repo"],
        "properties": {
            "user": {"type": "string"},
            "repo": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def user(self):
        return self.config.get("user", self.parsed_data.get("user"))

    @Plugin.property
    def repo(self):
        return self.config.get("repo", self.parsed_data.get("repo"))

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

    @Plugin.property
    def parsed_data(self):
        try:
            repo = Repo()
            pack = parse(repo.remote().url)
            return {"user": pack.owner, "repo": pack.repo}
        except Exception:
            return {}
