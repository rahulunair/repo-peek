import typer

app = typer.Typer()


@app.command()
def peek(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def info():
    print("info")


if __name__ == "__main__":
    app()
