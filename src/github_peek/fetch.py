"""fetch a remote repo and open in a local editor."""
import asyncio
import os
from pathlib import Path
import shutil
import tarfile

import aiohttp
import aiofiles
from loguru import logger


GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/tarball/master"
EDITORS = ["vim", "vi", "nvim", "nano", "code", "emacs"]


async def make_repo_url(name: str) -> str:
    """convert github url to github api url."""
    owner, repo = name.split("/")
    url = GITHUB_API.format(owner=owner, repo=repo)
    return url


async def fetch_repo(name: str = "", tar_dirs: Path = Path("")):
    """fetch a remote repo."""
    repo_url = await make_repo_url(name)
    chunk_size = 1024
    logger.info("repo url {}".format(repo_url))
    logger.debug("download to tar dir {}".format(tar_dirs))
    os.chdir(tar_dirs)
    async with aiohttp.ClientSession() as session:
        async with session.get(repo_url) as response:
            async with aiofiles.open(name.split("/")[-1], "wb") as fd:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    await fd.write(chunk)
                await fd.flush()
    return tar_dirs / name.split("/")[-1]


async def extract(tar_file: Path, to_path: Path):
    """extract tar file and return path."""
    with tarfile.open(tar_file) as tf:
        tf.extractall(path=to_path)


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


def logger_conf():
    logger.remove()
    logger.add(
        Path.home() / ".githubkeep.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )


async def peek_repo(repo: str):
    logger_conf()
    config_file = config(".githubkeep.conf")
    home_dir = Path.home() / ".githubkeep"
    tar_dirs = init_dir(home_dir / "tars")
    repo_dir = init_dir(home_dir / "repos" / repo)

    if not os.listdir(repo_dir):
        logger.info("fetching repo: {}".format(repo))
        repo_name = await fetch_repo(repo, tar_dirs)
        logger.info("extracting repo: {} to {}".format(repo_name, repo_dir))
        await extract(repo_name, repo_dir)
    await open_editor(path=repo_dir)
    if is_old(config_file):
        rm_stored_repos(home_dir)


def main(repo="rahulunair/cloudstore"):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(peek_repo(repo))
