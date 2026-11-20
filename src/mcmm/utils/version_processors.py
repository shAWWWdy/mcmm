def __compare_versions(v1: str, v2: str):
    v1, v2 = [int(i) for i in v1.split('.')], [int(i) for i in v2.split('.')]
    n, m = len(v1), len(v2)
    if n > m:
        return -1
    elif m > n:
        return 1
    else:
        for i in range(n):
            if v1[i] > v2[i]:
                return 1
            elif v1[i] < v2[i]:
                return -1
    return 0


def process_forge_client(raw_version: str) -> str:
    parts = raw_version.split('-')
    return "Minecraft " + parts[0]


def process_forge_loader(raw_version: str) -> str:
    parts = raw_version.split('-')
    if __compare_versions(parts[0], "1.13.0") == -1:
        return "Forge " + parts[1].lower().replace('forge', ' ')
    else:
        return "Forge " + parts[-1]


def process_fabric_client(raw_version: str) -> str:
    parts = raw_version.split('-')
    if 'loader' in raw_version:
        return "Minecraft " + parts[-1]
    else:
        return "Minecraft " + parts[0]


def process_fabric_loader(raw_version: str) -> str:
    parts = raw_version.split('-')
    if 'loader' in raw_version.split('-'):
        return "Fabric " + parts[-2]
    else:
        return "Fabric " + parts[-1]


def process_neoforge_client(raw_version: str) -> str | None:
    parts = raw_version.split('-')
    if parts[0] == 'neoforge':
        return None
    else:
        return "Minecraft " + parts[0]


def process_neoforge_loader(raw_version: str) -> str:
    parts = raw_version.split('-')
    return "Neoforge " + parts[-1]


def process_vanilla_client(raw_version: str) -> str:
    return "Minecraft " + raw_version


def process_vanilla_loader(raw_version: str) -> str:
    return "Vanilla Minecraft " + raw_version


def process_quilt_client(raw_version: str) -> str:
    parts = raw_version.split('-')
    if 'loader' in raw_version:
        return "Minecraft " + parts[-1]
    else:
        return "Minecraft " + parts[0]


def process_quilt_loader(raw_version: str) -> str:
    parts = raw_version.split('-')
    if 'loader' in raw_version:
        return "Quilt " + parts[-2]
    else:
        return "Quilt " + parts[-1]
