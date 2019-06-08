from __future__ import annotations

import logging
from typing import List, Optional, Union, overload
from pathlib import Path

from .paths import Paths


logger = logging.getLogger(__name__)

@overload
def get() -> List[Map]: ...
@overload
def get(name: str) -> Map: ...

def get(name: Optional[str]=None) -> Union[List[Map], Map]:
    maps = []
    for mapdir in (p for p in Paths.MAPS.iterdir()):
        if mapdir.is_dir():
            for mapfile in (p for p in mapdir.iterdir() if p.is_file()):
                if mapfile.suffix == ".SC2Map":
                    maps.append(Map(mapfile))
        elif mapdir.is_file():
            if mapdir.suffix == ".SC2Map":
                maps.append(Map(mapdir))

    if name is None:
        return maps

    for m in maps:
        if m.matches(name):
            return m

    raise KeyError(f"Map '{name}' was not found. Please put the map file in \"/StarCraft II/Maps/\".")

class Map:
    def __init__(self, path: Path):
        self.path = path

        if self.path.is_absolute():
            try:
                self.relative_path = self.path.relative_to(Paths.MAPS)
            except ValueError:  # path not relative to basedir
                logging.warning(f"Using absolute path: {self.path}")
                self.relative_path = self.path
        else:
            self.relative_path = self.path

    @property
    def name(self) -> str:
        return self.path.stem

    @property
    def data(self) -> bytes:
        with open(self.path, "rb") as f:
            return f.read()

    def matches(self, name) -> bool:
        return self.name.lower().replace(" ", "") == name.lower().replace(" ", "")

    def __repr__(self):
        return f"Map({self.path})"
