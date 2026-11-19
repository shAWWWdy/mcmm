import click
import mcmm

@click.command()
def hello():
    """Приветствие пользователя"""
    click.echo("Привет мир!")

@click.command()
def version():
    """Версия продукта"""
    click.echo(mcmm.__version__)

if __name__ == "__main__":
    pass