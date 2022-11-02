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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf, path=to_path)
