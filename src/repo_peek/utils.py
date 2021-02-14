"""utilities."""
import os
from pathlib import Path
import tarfile

import aiofiles
import aiohttp

from .config import GITHUB_API
from .logging import logger


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
