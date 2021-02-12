"""fetch a remote repo and open in a local editor."""
import asyncio
import os
from pathlib import Path
import tarfile

import aiohttp
import aiofiles


GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/tarball/master"


async def make_repo_url(name: str) -> str:
    """convert github url to github api url."""
    owner, repo = name.split("/")
    url = GITHUB_API.format(owner=owner, repo=repo)
    return url


async def fetch_repo(name: str = "", tar_dirs: Path = Path("")):
    """fetch a remote repo."""
    repo_url = await make_repo_url(name)
    chunk_size = 1024
    print("repo url {}".format(repo_url))
    print("download to tar dir {}".format(tar_dirs))
    os.chdir(tar_dirs)
    async with aiohttp.ClientSession() as session:
        print(2)
        async with session.get(repo_url) as response:
            async with aiofiles.open(name.split("/")[-1], "wb") as fd:
                while True:
                    chunk = await response.content.read(chunk_size)
                    print("downloading chunks..")
                    if not chunk:
                        break
                    await fd.write(chunk)
                await fd.flush()


async def extract(tar_file: Path, to_path: Path):
    """extract tar file and return path."""
    with tarfile.open(tar_file) as tf:
        tf.extractall(path=to_path)


async def temp_file() -> str:
    """create a temp dir to download the repo."""
    pass


def init_dir(home_dir) -> Path:
    """create a dir to save the downloaded files."""
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir


async def delete_on_exit():
    pass


async def open_editor(editor="vim", path: Path = Path("")):
    """open editor with source."""
    process = await asyncio.create_subprocess_exec(editor, str(path))
    stdout, stderr = await process.communicate()
    # code = await process.wait()
    # print("exit code is : {}".format(code))


async def main():
    repo = "rahulunair/cloudstore"
    home_dir = Path.home() / ".githubkeep"
    home_dir = init_dir(home_dir)
    tar_dirs = init_dir(home_dir / "tars")
    repo_dir = init_dir(home_dir / "repos" / repo)
    await fetch_repo(repo, tar_dirs)
    await extract(tar_dirs, repo_dir)
    await open_editor(path=repo_dir)
    home_dir.rmdir()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
