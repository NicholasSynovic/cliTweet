import toml

def writeTOML(data: dict)   ->  str:
    return toml.dump(data, ".htconfig.toml")

def readTOML()  ->  dict:
    return toml.load(".htconfig.toml")
