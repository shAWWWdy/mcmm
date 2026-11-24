import click
import mcmm
from mcmm.utils.installers import *
from mcmm.utils.utils import *

@click.group(invoke_without_command=True)
@click.option("--version", "-V", is_flag=True, help="Show version.")
@click.option("--dir", "-d", "target_dir", type=click.Path(exists=True, file_okay=False),
              default=None, help="Execute in provided directory.")
@click.pass_context
def cli(ctx, version, target_dir):
    """MCMM - MineCraft Mod Manager"""
    ctx.obj = dict()
    ctx.obj['dir'] = target_dir

    if version:
        click.echo(f"mcmm {mcmm.__version__} from {os.getcwd()}")
    if not version and ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.pass_context
def list(ctx):
    """List all installed mods in current mods folder"""
    mods_dir = find_mods_dir(ctx.obj['dir'])
    mods = [entry.name for entry in os.scandir(mods_dir) if entry.is_file() and entry.name.endswith(".jar")]
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


@cli.command()
@click.argument("modloader",
                type=click.Choice(["fabric", "forge", "neoforge", "quilt"], case_sensitive=False))
@click.option("--mc-version", default=None,
              help="Specify minecraft instance version if it can't be defined automatically.")
@click.option("--loader-version", help="Specify modloader version if needed. Will choose latest otherwise.")
@click.option("--silent", is_flag=True, help="Will pass arguments without opening the installer GUI")
@click.pass_context
def setup(ctx, modloader, mc_version, loader_version, silent):
    """Install specified modloader"""
    if not mc_version:
        mc_version = detect_client(ctx.obj['dir'])
    if not mc_version:
        click.echo("Could not define current Minecraft instance version. Specify with --mc-version.")
        return

    click.echo(f"Installing {modloader} loader for {mc_version} ({loader_version if loader_version else "latest"})")

    setup_modloader(modloader, mc_version, loader_version, silent)


if __name__ == "__main__":
    cli()
