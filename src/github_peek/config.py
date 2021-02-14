import configparser
from datetime import datetime
from datetime import timedelta
from pathlib import Path

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/tarball/master"
EDITORS = ["vim", "vi", "nvim", "nano", "code", "emacs"]


class Config:
    def __init__(self, cfg_file=".githubkeep.ini"):
        self.config_file = Path.home() / cfg_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def cache_repo(self, name):
        """update repo with name, url and remove_by info."""
        if not self.config.has_section(name):
            self.config.add_section(name)
            self.config.set(
                name,
                "remove_by",
                (
                    datetime.now()
                    + timedelta(minutes=self.config["DEFAULT"].getint("CACHE_DELTA"))
                ).strftime("%Y%m%d-%H%M%S"),
            )
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def is_repo_stale(self, name):
        """check if the repo is ready to be deleted."""
        if self.config.has_section(name):
            remove_by = self.config[name].get("remove_by")
            remove_by = datetime.strptime(remove_by, "%Y%m%d-%H%M%S")
            if remove_by < datetime.now():
                return True
            else:
                return False
        else:
            return False


def init_dir(home_dir) -> Path:
    """create a dir to save the downloaded files."""
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir
