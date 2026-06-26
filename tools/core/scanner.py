from __future__ import annotations

from pathlib import Path

from .config import config
from .models import ComicFile


class Scanner:

    def scan(self) -> list[ComicFile]:

        comics: list[ComicFile] = []

        if not config.comics_dir.exists():
            return comics

        for file in sorted(config.comics_dir.rglob("*")):

            if not file.is_file():
                continue

            if file.suffix.lower() != ".cbz":
                continue

            stat = file.stat()

            comics.append(
                ComicFile(
                    filename=file.name,
                    filepath=file,
                    filesize=stat.st_size,
                    modified=stat.st_mtime,
                )
            )

        return comics