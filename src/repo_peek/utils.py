"""utilities."""
import os
from pathlib import Path
import tarfile

import aiofiles
import aiohttp
import asyncio

from .config import GITHUB_API
from .config import GITLAB_API
from .logging import logger


def make_repo_url(name: str, service="github") -> str:
    """make valid repo url."""
    owner, repo = name.split("/")
    url = ""
    if service == "github":
        url = GITHUB_API.format(owner=owner, repo=repo)
    elif service == "gitlab":
        url = GITLAB_API.format(owner=owner, repo=repo)
    return url


async def clone_repo(name: str, to_dir: Path):
    """git clone to a dir."""
    repo_url = make_repo_url(name, service="gitlab")
    logger.debug(f"clone {repo_url} to {to_dir}")
    git_cmd = [
        "git",
        "clone",
        "--filter=blob:none",
        "--single-branch",
        "--depth=1",
        f"{repo_url}",
        f"{to_dir}",
    ]
    process = await asyncio.create_subprocess_exec(*git_cmd)
    await process.communicate()


async def fetch_repo(name: str = "", tar_dirs: Path = Path("")):
    """fetch a remote repo."""
    repo_url = make_repo_url(name)
    chunk_size = 1024
    logger.debug("download to tar dir {} from repo {}".format(tar_dirs, repo_url))
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
    logger.debug("extracting repo tar: {} to {}".format(tar_file, to_path))
    with tarfile.open(tar_file) as tf:
        tf.extractall(path=to_path)
