"""cli to github peek."""

import typer

from github_peek.fetch import main

app = typer.Typer()


@app.command()
def peek(repo: str):
    try:
        typer.secho(f"opening repo: {repo}...", fg=typer.colors.GREEN)
        main(repo)
    except Exception:
        typer.echo(f"failed to peek {repo}")
        raise typer.Abort()


@app.command()
def info():
    typer.secho("a tool to peek into a github repo.")


if __name__ == "__main__":
    app()
