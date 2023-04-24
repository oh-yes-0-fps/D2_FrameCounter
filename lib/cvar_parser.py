from __future__ import annotations
import xmltodict
from typing import Any, Iterable, Optional
import platform


class Namespace:
    """Duck typed abstraction of a namespace in the cvars.xml file"""
    def __init__(self, vars: dict) -> None:
        self.vars = vars

    def __repr__(self) -> str:
        return f"<Namespace {self.vars}>"

    def __dir__(self) -> Iterable[str]:
        return list(self.vars.keys())

    def __getattribute__(self, __name: str) -> Any:
        if __name == "vars":
            return super().__getattribute__(__name)
        if __name in self.vars.keys():
            return self.vars[__name]
        return super().__getattribute__(__name)


class Cvar:
    """Duck typed abstraction of the cvars.xml file"""
    def __init__(self, xml_file_path: str) -> None:
        self.xml_file = xml_file_path
        self.cvars = {}
        with open(self.xml_file, "r") as f:
            xml = xmltodict.parse(f.read())["body"]["namespace"]
            for namespace in xml:
                name = namespace["@name"]
                var_dict = {}
                for var in namespace["cvar"]:
                    if type(var) == str:
                        continue
                    var_dict[var["@name"]] = var["@value"]
                self.cvars[name] = var_dict

    def __dir__(self) -> Iterable[str]:
        return list(self.cvars.keys())

    def __repr__(self) -> str:
        return f"<CvarParser {self.cvars}>"

    def __getattribute__(self, __name: str) -> Any:
        if __name == "cvars":
            return super().__getattribute__(__name)
        if __name in self.cvars.keys():
            return Namespace(self.cvars[__name])
        return super().__getattribute__(__name)


class CvarSingleton:
    instance: Optional[Cvar] = None

    @classmethod
    def get_instance(cls) -> Cvar:
        if cls.instance is None:
            if platform.system().lower() != "windows":
                raise NotImplementedError("Only windows is supported")
            import os
            appdata = os.getenv("APPDATA")
            if appdata is None:
                raise Exception("Could not find appdata path")
            cls.instance = Cvar(
                appdata+"\\Bungie\\DestinyPC\\prefs\\cvars.xml")
        return cls.instance