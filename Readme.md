## github-peek

A command line tool to peek a remote repo locally and view it in your favorite editor. The tool handles cleanup of the repo once you exit your editor. 

The tool creates 2 files and a directory, a config file `~/.githubkeep.conf`, a log file `~/.githubkeep.log` and a directory `~/.githubkeep`. Github-peek downloads the tar:gz of the repo, extracts it and saves it to `~/.githubkeep`. There is a naive caching mechanism, where the tool deletes all repos after 5 times of using the app.

Default editor is chosen by looking at the `EDITOR` environment variable, if it is not set, vim is chosen as the default editor.

### install github-peek

```bash
pip install github-peek
```

### usage:

github-peek only has only subcommand `peek`, which takes a repo as the argument.


command usage:

```bash
ghub peek <repo>
```

example:

```bash
ghub peek rahulunair/github-peek
```

### todo

- enable for gitlab


