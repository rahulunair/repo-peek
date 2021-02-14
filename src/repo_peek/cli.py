"""cli to github peek."""

import typer

from repo_peek.fetch import main
from . import __version__

app = typer.Typer()


@app.command()
def gh(repo: str):
    """open a github repo."""
    try:
        typer.secho(f"opening repo: {repo}...", fg=typer.colors.GREEN)
        main(repo)
    except Exception:
       typer.echo(f"failed to peek {repo}")
       raise typer.Abort()

def gl(repo: str):
    """open a gitlab repo."""
    try:
        typer.secho(f"opening repo: {repo}...", fg=typer.colors.GREEN)
        main(repo)
    except Exception:
       typer.echo(f"failed to peek {repo}")
       raise typer.Abort()

@app.command()
def info():
    typer.secho("a tool to peek into a github repo.")
    typer.secho("version: {}".format(__version__))


if __name__ == "__main__":
    app()
