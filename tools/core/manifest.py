from __future__ import annotations

import json

from .config import config
from .models import ComicFile


class Manifest:

    FILE_NAME = "build-manifest.json"

    def __init__(self):

        self.path = config.data_dir / self.FILE_NAME

        self.data = {}

        self.load()

    def load(self):

        if not self.path.exists():
            self.data = {}
            return

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as fp:

            self.data = json.load(fp)

    def save(self):

        config.data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                self.data,
                fp,
                indent=2,
                ensure_ascii=False,
            )

    def is_changed(
        self,
        comic: ComicFile,
    ) -> bool:

        old = self.data.get(comic.filename)

        if old is None:
            return True

        if old["size"] != comic.filesize:
            return True

        if old["modified"] != comic.modified:
            return True

        return False

    def update(
        self,
        comic: ComicFile,
    ):

        self.data[comic.filename] = {

            "size": comic.filesize,

            "modified": comic.modified,

        }
