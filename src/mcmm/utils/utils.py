import json
import os
import platform
from .version_processors import *

def __find_default_minecraft_dir() -> str | None:
    system = platform.system()
    minecraft_dir = None

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            minecraft_dir = os.path.join(appdata, ".minecraft")
    elif system == "Darwin":
        minecraft_dir = os.path.expanduser("~/Library/Application Support/minecraft")
    elif system == "Linux":
        minecraft_dir = os.path.expanduser("~/.minecraft")

    return minecraft_dir


def __get_latest_version() -> str:
    minecraft_dir = __find_default_minecraft_dir()
    if minecraft_dir is None:
        return ""
    latest = ""
    try:
        with open(os.path.join(minecraft_dir, "versions", "version_manifest_v2.json"), 'r') as file:
            vers = json.load(file)
            latest = vers['latest']['release']
    except Exception:
        pass
    return latest


def __process_raw_client_version(raw_version: str) -> str | None:
    actual_version = None
    if raw_version == 'latest-release':
        actual_version = "Minecraft " + __get_latest_version()
    elif 'fabric' in raw_version.lower():
        actual_version = process_fabric_client(raw_version)
    elif 'forge' in raw_version.lower():
        actual_version = process_forge_client(raw_version)
    elif 'neoforge' in raw_version.lower():
        actual_version = process_neoforge_client(raw_version)
    elif 'quilt' in raw_version.lower():
        actual_version = process_quilt_client(raw_version)
    else:
        actual_version = process_vanilla_client(raw_version)

    return actual_version


def __process_raw_modloader_version(raw_version: str) -> str | None:
    actual_version = None
    if 'fabric' in raw_version.lower():
        actual_version = process_fabric_loader(raw_version)
    elif 'forge' in raw_version.lower():
        actual_version = process_forge_loader(raw_version)
    elif 'neoforge' in raw_version.lower():
        actual_version = process_neoforge_loader(raw_version)
    elif 'quilt' in raw_version.lower():
        actual_version = process_quilt_loader(raw_version)
    else:
        actual_version = process_vanilla_loader(raw_version)

    return actual_version


def find_mods_dir(target_path: str | None = None) -> str | None:
    """
    Returns mods/ directory. If run in minecraft profile folder, return its folder.
    If not, searches for .minecraft/mods/ or provides None
    """
    mods_dir = None
    cwd = target_path if target_path is not None else os.getcwd()
    cwd_name = os.path.basename(cwd)
    candidate = os.path.join(cwd, "mods")
    minecraft_dir = __find_default_minecraft_dir()

    if cwd_name == "mods":
        mods_dir = cwd
    elif os.path.isdir(candidate):
        mods_dir = candidate
    elif minecraft_dir:
        mods_dir = minecraft_dir

    return mods_dir


def detect_client(target_path: str | None = None) -> str | None:
    """
    Return current Minecraft instance version.
    If not defined, then None.
    """
    current_dir:str|None = target_path if target_path is not None else find_mods_dir(target_path)
    if current_dir is None:
        return None
    raw_version = None
    minecraft_dir = __find_default_minecraft_dir()
    if minecraft_dir is None:
        return None
    try:
        with open(os.path.join(minecraft_dir, "launcher_profiles.json"), 'r') as file:
            profiles = json.load(file)['profiles']
            for profile in profiles.values():
                if profile['gameDir'] in current_dir:
                    raw_version: str = profile['lastVersionId']
                    break
    except Exception:
        pass

    if raw_version:
        return __process_raw_client_version(raw_version)
    return raw_version


def detect_modloader(target_path: str | None = None) -> str | None:
    """
    Return current modloader and its version.
    If not defined, then None.
    """
    current_dir: str | None = target_path if target_path is not None else find_mods_dir(target_path)
    if current_dir is None:
        return None
    raw_version = None
    minecraft_dir = __find_default_minecraft_dir()
    if minecraft_dir is None:
        return None
    try:
        with open(os.path.join(minecraft_dir, "launcher_profiles.json"), 'r') as file:
            profiles = json.load(file)['profiles']
            for profile in profiles.values():
                if profile['gameDir'] in current_dir:
                    raw_version: str = profile['lastVersionId']
                    break
    except Exception:
        pass

    if raw_version:
        return __process_raw_modloader_version(raw_version)
    return raw_version
