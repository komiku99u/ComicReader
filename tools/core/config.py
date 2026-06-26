from __future__ import annotations

from dataclasses import dataclass

from . import constants


@dataclass(slots=True)
class Config:
    project_name: str = constants.PROJECT_NAME
    version: str = constants.PROJECT_VERSION

    comics_dir = constants.COMICS_DIR
    covers_dir = constants.COVERS_DIR
    data_dir = constants.DATA_DIR
    cache_dir = constants.CACHE_DIR


config = Config()