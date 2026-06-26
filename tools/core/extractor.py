from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from .config import config
from .models import ComicFile
from .models import ComicMetadata


class CoverExtractor:

    IMAGE_EXTENSIONS = (
        ".webp",
        ".jpg",
        ".jpeg",
        ".png",
        ".avif",
    )

    def extract(
        self,
        comic: ComicFile,
        metadata: ComicMetadata,
    ) -> Path:

        config.covers_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with zipfile.ZipFile(comic.filepath) as archive:

            image = self._find_first_image(
                archive.namelist()
            )

            if image is None:

                raise RuntimeError(
                    "No image found."
                )

            extension = Path(image).suffix.lower()

            output = (
                config.covers_dir
                / f"{metadata.uid}{extension}"
            )

            if output.exists():
                return output

            with archive.open(image) as src:

                with output.open("wb") as dst:

                    shutil.copyfileobj(
                        src,
                        dst,
                    )

            return output

    def _find_first_image(
        self,
        files: list[str],
    ):

        images = []

        for file in files:

            suffix = Path(file).suffix.lower()

            if suffix in self.IMAGE_EXTENSIONS:

                images.append(file)

        if not images:

            return None

        images.sort()

        return images[0]