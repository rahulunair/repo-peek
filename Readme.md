## repo-peek

A command line tool to peek a remote repo locally and view it in your favorite editor. The tool handles cleanup of the repo once you exit your editor. 

<a href="https://asciinema.org/a/3EyUeIwGTYxTJFceBbJNLln8t" target="_blank"><img src="https://asciinema.org/a/3EyUeIwGTYxTJFceBbJNLln8t.svg" /></a>
Default editor is chosen by looking at the `EDITOR` environment variable, if it is not set, vim is chosen as the default editor.

### install repo-peek

```bash
pip install repo-peek
```

### usage:

repo-peek (`repk`) has a subcommand to tell it if you want to checkout a github (`gh`) or a gitlab (`gl`) repo. That is all that is needed.


command usage:

```bash
repk gh <repo>
```

example:

```bash
repk gh rahulunair/repo-peek
```

### todo

- enable for gitlab

### more information

The tool creates 2 files and a directory, a config file `~/.githubkeep.conf`, a log file `~/.githubkeep.log` and a directory `~/.githubkeep`. Github-peek downloads the tar:gz of the repo, extracts it and saves it to `~/.githubkeep`. There is a naive caching mechanism, where the tool deletes all repos after 5 times of using the app.


