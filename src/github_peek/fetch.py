"""fetch a remote repo and open in a local editor."""
import asyncio

import aiohttp
import aiofiles


GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/tarball/master"


async def make_repo_url(name: str) -> str:
    """convert github url to github api url."""
    owner, repo = name.split("/")
    url = GITHUB_API.format(owner=owner, repo=repo)
    return url


async def fetch_repo(name: str = ""):
    """fetch a remote repo."""
    repo_url = await make_repo_url(name)
    chunk_size = 1024
    print("repo url {}".format(repo_url))
    async with aiohttp.ClientSession() as session:
        async with session.get(repo_url) as response:
            async with aiofiles.open("sample.tar", "wb") as fd:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    await fd.write(chunk)
                await fd.flush()


async def extract(tar_file: str) -> str:
    """extract tar file and return path."""
    pass


async def temp_file() -> str:
    """create a temp dir to download the repo."""
    pass


async def delete_on_exit():
    pass


async def open_editor(editor="vim", path: str = "cli.py"):
    """open editor with source."""
    command = f"{editor} {path}"
    process = await asyncio.create_subprocess_exec(
        command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE
    )
    # await process.communicate()
    code = await process.wait()
    print("exit code is : {}".format(code))


async def main():
    # await fetch_repo("rahulunair/cloudstore")
    await fetch_repo()
    path = await extract_repo()
    await open_editor(path=path)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
