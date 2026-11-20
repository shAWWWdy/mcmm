import json
import os
import platform


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


def __get_latest_version() -> str | None:
    minecraft_dir = __find_default_minecraft_dir()
    if minecraft_dir is None:
        return None
    latest = None
    try:
        with open(os.path.join(minecraft_dir, "versions", "version_manifest_v2.json"), 'r') as file:
            vers = json.load(file)
            latest = vers['latest']['release']
    except Exception:
        pass
    return latest


def __process_raw_minecraft_version(raw_version: str) -> str | None:
    actual_version = None
    if raw_version == 'latest-release':
        actual_version = __get_latest_version()
    elif 'fabric' in raw_version.lower():
        actual_version = raw_version.split('-')[-1]
    elif 'forge' in raw_version.lower():
        actual_version = raw_version.split('-')[0]
    elif 'neoforge' in raw_version.lower():
        actual_version = None

    return actual_version


def __process_raw_modloader_version(raw_version: str) -> str | None:
    actual_version = None
    if 'fabric' in raw_version.lower():
        actual_version = "Fabric " + raw_version.split('-')[-2]
    elif 'forge' in raw_version.lower():
        actual_version = "Forge " + raw_version.split('-')[-1]
    elif 'neoforge' in raw_version.lower():
        actual_version = "Neoforge"

    return actual_version


def find_mods_dir(target_path: str | None = None) -> str | None:
    """Returns mods/ directory. If run in minecraft profile folder, return its folder. If not, searches for .minecraft/mods/ or provides None"""
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
        return __process_raw_minecraft_version(raw_version)
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
