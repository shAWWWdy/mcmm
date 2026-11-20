import click

import mcmm
from mcmm.utils.utils import *


@click.group(invoke_without_command=True)
@click.option("--version", "-V", is_flag=True, help="Show version.")
@click.option("--dir", "-d", type=click.Path(exists=True, file_okay=False),
              default=None, help="Execute in provided directory.")
@click.pass_context
def cli(ctx, version, dir):
    """MCMM - MineCraft Mod Manager"""
    ctx.obj = dict()
    ctx.obj['dir'] = dir

    if version:
        click.echo(f"mcmm {mcmm.__version__} from {os.getcwd()}")
    if not version and ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.pass_context
def list(ctx):
    """List all installed mods in current mods folder"""
    mods_dir = find_mods_dir(ctx.obj)
    mods = os.listdir(mods_dir)
    for mod in mods:
        click.echo(mod)


@cli.command()
@click.pass_context
def dir(ctx):
    """Show current mods path"""
    mods_dir = find_mods_dir(ctx.obj['dir'])
    click.echo(mods_dir if mods_dir is not None else "Could not find mods directory")


@cli.command()
@click.pass_context
def client(ctx):
    """Show current client version"""
    client_v = detect_client(ctx.obj['dir'])
    click.echo(client_v if client_v is not None else "Could not define Minecraft client version.")


@cli.command()
@click.pass_context
def loader(ctx):
    """Show current modloader and its version"""
    loader_v = detect_modloader(ctx.obj['dir'])
    click.echo(loader_v if loader_v is not None else "Could not define modloader version. Consider downloading one.")


if __name__ == "__main__":
    cli()
