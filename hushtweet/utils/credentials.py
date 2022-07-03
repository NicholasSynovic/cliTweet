import toml
from pathlib import Path

def writeTOML(data: dict, filepath: str) -> str:
    fn: Path = Path(filepath).expanduser().resolve()

    with open(fn, "w") as tomlFile:
        data: str = toml.dump(data, tomlFile)
        tomlFile.close()
    return data


def readTOML(filepath: str) -> dict:
    fn: Path = Path(filepath).expanduser().resolve()
    return toml.load(fn)
