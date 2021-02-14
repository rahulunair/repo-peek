"""cli to github peek."""

import typer

from repo_peek.fetch import main
from . import __version__

app = typer.Typer()


@app.command()
def gh(repo: str):
    """open a github repo."""
    try:
        typer.secho(f"opening github repo: {repo}...", fg=typer.colors.GREEN)
        main(repo, service="github")
    except Exception:
        typer.echo(f"failed to peek {repo}")
        raise typer.Abort()


@app.command()
def gl(repo: str):
    """open a gitlab repo."""
    # try:
    typer.secho(f"opening gitlab repo: {repo}...", fg=typer.colors.YELLOW)
    main(repo, service="gitlab")
    # except Exception:
    #    typer.echo(f"failed to peek {repo}")
    #    raise typer.Abort()


@app.command()
def info():
    """information about the tool."""
    typer.secho("a tool to peek into a github repo.")
    typer.secho("version: {}".format(__version__))


if __name__ == "__main__":
    app()
