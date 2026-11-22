import json
import subprocess
import urllib.request
from pathlib import Path

import click

CACHE_DIR = Path.home() / ".mcmm" / "cache" / "installers"


def setup_modloader(modloader: str, mc_version: str, modloader_version: str | None = None, silent: bool | None = None):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    match modloader.lower():
        case "fabric":
            __setup_fabric(mc_version, modloader_version, silent)
        case "forge":
            pass
        case "neoforge":
            pass
        case "quilt":
            pass


def __download_file(url: str, save_path: str | Path) -> bool:
    try:
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception as e:
        return False


def __setup_fabric(mc_version: str, modloader_version: str | None, silent):
    url = "https://meta.fabricmc.net/v2/versions/installer"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            url = data[0]['url']
            installer_version = data[0]['version']
    except Exception as e:
        click.echo(f"Could not get installer URL: {e}")
        return

    filename = f"fabric-{installer_version}.jar"
    installer_path = CACHE_DIR / filename

    if installer_path.is_file():
        click.echo(f"Requirement already satisfied: fabric installer in {installer_path}")
    elif not __download_file(url, installer_path):
        click.echo("Could not download fabric installer")
    else:
        click.echo(f"Installer downloaded successfully to {installer_path}")

    command = ["java", "-jar", str(installer_path)]
    if silent:
        command += ["client", "-mcversion", mc_version]
        if modloader_version:
            command += ["-loader", modloader_version]
    subprocess.run(command)
