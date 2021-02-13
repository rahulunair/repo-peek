import os
from pathlib import Path

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/tarball/master"
EDITORS = ["vim", "vi", "nvim", "nano", "code", "emacs"]


def config(cfg_file=".githubkeep.conf"):
    """set global config setting"""
    # TODO(unrahul): change to ini logger
    config_file = Path.home() / cfg_file
    template = "{}={}"
    exists = os.path.isfile(config_file)
    if exists:
        with open(config_file, "r") as rh:
            line = rh.readline()
            count = int(line.split("=")[1])
            count -= 1
    else:
        count = 5
    with open(config_file, "w") as fh:
        fh.writelines(template.format("count_till_cache_delete", count))
        fh.flush()
    return config_file
