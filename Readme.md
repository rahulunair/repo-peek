## repo-peek

A command line tool to peek a remote repo hosted on github or gitlab locally and view it in your favorite editor. The tool handles cleanup of the repo once you exit your editor. 

[![asciicast](https://asciinema.org/a/uLoPyrNwus5yY2SgyRuJ2qCyq.svg)](https://asciinema.org/a/uLoPyrNwus5yY2SgyRuJ2qCyq)

Default editor is chosen by looking at the `EDITOR` environment variable, if it is not set, vim is chosen as the default editor.

### install repo-peek

```bash
pip install repo-peek
```

### usage:

ask repo-peek (`repk`) to checkout a github or gitlab repo using the subcommands `gh` or `gl`.

command usage:

```bash
Usage: repk COMMAND <repo>...

Commands:
  gh    open a github repo.
  gl    open a gitlab repo.
  info  information about the tool.

```

example:

```bash
repk gh rahulunair/repo-peek
```
### configuration:

The tool sets writes default config to `~/.repk.ini`, the initial settings are:

```ini
[DEFAULT]
editor = "vim"
cache_repos = 1
cache_delta = 3
cache_loc = ""
github_token = ""
gitlab_token = ""

[proxy_settings]
https_proxy = ""
http_proxy = ""

[rahulunair/syntribos]
remove_by = 20210213-185716
```

description of keys:

default settings:

editor - editor of choice (default=vim)
cache_repos - should repos be cached (default=1, set 0 if caching is not required)
cache_delta - mintues for which repos should be cached
cache_loc - directory where cached repos should be stored (default=~/.repk)
github_token - for handling throlling limits (not implemented)
gitlab_token - for handling throlling limits (not implemented)

proxy_settings - if you are inside a proxy set these

The configs after these have the format:
[repo_name]
remove_by - time till the cache would be kept

### more information

The tool creates 2 files and a directory, a config file `~/.repk.ini`, a log file `~/.repk.log` and a directory `~/.repk`. repo-peek downloads the tar:gz of the repo, extracts it and saves it to `~/.repk`. There is a naive caching mechanism, where the tool deletes each repo if it is older than 3 minutes. 

I got influenced to build this tool after i saw: [git peek](https://github.com/Jarred-Sumner/git-peek)


