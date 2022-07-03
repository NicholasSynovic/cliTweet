import toml


def writeTOML(data: dict) -> str:
    with open(".htconfig.toml", "w") as tomlFile:
        data: str = toml.dump(data, tomlFile)
        tomlFile.close()
    return data


def readTOML() -> dict:
    return toml.load(".htconfig.toml")
