import os
import platform

import click
import mcmm

def find_mods_dir() -> str | None:
    """Checks if current directory is instance of mods/ or its neighbor. If not, searches for default or None"""
    system = platform.system()
    mods_dir = None
    cwd = os.getcwd()
    cwd_name = os.path.basename(cwd)
    candidate = os.path.join(cwd, "mods")

    if cwd_name == "mods":
        mods_dir = cwd
    elif os.path.isdir(candidate):
        mods_dir = candidate
    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            mods_dir = os.path.join(appdata, ".minecraft", "mods")
    elif system == "Darwin":
        mods_dir = os.path.expanduser("~/Library/Application Support/minecraft")
    elif system == "Linux":
        mods_dir = os.path.expanduser("~/.minecraft")

    return mods_dir

@click.group(invoke_without_command=True)
@click.option("--version", "-V", is_flag=True, help="Show version.")
@click.option("--mods-directory", "-d", is_flag=True, help="Show current mods path.")
@click.pass_context
def cli(ctx, version, mods_directory):
    """MCMM - MineCraft Mod Manager"""
    if version:
        click.echo(f"mcmm {mcmm.__version__} from {os.getcwd()}")
    if mods_directory:
        mods_dir = find_mods_dir()
        click.echo(mods_dir if mods_dir is not None else "Could not find mods directory")

    if not version and not mods_directory and ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command()
def list():
    """List all installed mods in current mods folder"""
    mods_dir = find_mods_dir()
    mods = os.listdir(mods_dir)
    for mod in mods:
        click.echo(mod)


if __name__ == "__main__":
    cli()
