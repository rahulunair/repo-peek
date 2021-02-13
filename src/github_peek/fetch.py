"""fetch a remote repo and open in a local editor."""
import asyncio
import os
from pathlib import Path
import shutil

from github_peek.logging import logger
from github_peek.config import config
from github_peek.config import EDITORS
from github_peek.utils import fetch_repo
from github_peek.utils import extract


def init_dir(home_dir) -> Path:
    """create a dir to save the downloaded files."""
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir


async def open_editor(editor="vim", path: Path = Path("")):
    """open editor with source."""
    editor = os.getenv("EDITOR", editor)
    if not editor in EDITORS:
        editor = "vim"
        logger.info("EDITOR not support, defaulting to vim")
    logger.info("opening in : {}".format(editor))
    process = await asyncio.create_subprocess_exec(editor, str(path))
    await process.communicate()


def is_old(config_file: Path) -> bool:
    """if count is zero, return True, else False"""
    with open(config_file, "r") as fh:
        line = fh.readline()
        count = int(line.split("=")[1])
        if count == 0:
            return True
        else:
            return False


def rm_stored_repos(home_dir):
    logger.info("removing cached dir: {}".format(home_dir))
    shutil.rmtree(home_dir, ignore_errors=True)
    os.remove(Path.home() / ".githubkeep.conf")


async def peek_repo(repo: str, caching=True):
    config_file = config(".githubkeep.conf")
    home_dir = Path.home() / ".githubkeep"
    tar_dirs = init_dir(home_dir / "tars")
    repo_dir = init_dir(home_dir / "repos" / repo)

    await open_editor(path=repo_dir)
    if not (os.listdir(repo_dir) or caching):
        logger.info("fetching repo: {}".format(repo))
        repo_name = await fetch_repo(repo, tar_dirs)
        logger.info("extracting repo: {} to {}".format(repo_name, repo_dir))
        await extract(repo_name, repo_dir)
    if is_old(config_file):
        rm_stored_repos(home_dir)

# open editor first
# download readme from cdn to the dir in which editor is openend
# extract files to the same dir

# use gitlab api to clone
# types
# profile and imporve loading time

def main(repo="rahulunair/cloudstore"):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(peek_repo(repo))
