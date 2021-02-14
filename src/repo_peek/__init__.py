__version__ = "0.1.0"

import os
from pathlib import Path

config_file = Path.home() / ".githubkeep.ini"
config_text = """
[DEFAULT]
editor = "vim"
cache_repos = 1
# how many minutes should each repo be kept in cache
cache_delta = 3
cache_loc = ""
github_token = ""
gitlab_token = ""

[proxy_settings]
https_proxy = ""
http_proxy = ""
"""
if not os.path.exists(config_file):
    with open(config_file, "w") as fh:
        fh.write(config_text)
