from collections import ChainMap

config_default: dict[str, str] = {"font": "arial", "size": "12pt", "color": "#000000"}

config_user: dict[str, str] = {"font": "roboto", "size": "10pt"}

config: ChainMap[str, str] = ChainMap(config_user, config_default)


print(config["font"])
print(config["size"])
print(config["color"])
