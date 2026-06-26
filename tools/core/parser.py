from __future__ import annotations

import json
import xml.etree.ElementTree as ET
import zipfile

from .models import ComicFile
from .models import ComicMetadata


class Parser:

    def parse(self, comic: ComicFile) -> ComicMetadata:

        with zipfile.ZipFile(comic.filepath, "r") as archive:

            meta = self._read_meta(archive)

            info = self._read_comicinfo(archive)

        return self._merge(comic, meta, info)

    def _read_meta(self, archive: zipfile.ZipFile) -> dict:

        with archive.open("meta.json") as fp:
            return json.load(fp)

    def _read_comicinfo(self, archive: zipfile.ZipFile) -> dict:

        with archive.open("ComicInfo.xml") as fp:

            root = ET.parse(fp).getroot()

        data = {}

        for child in root:

            tag = child.tag.split("}")[-1]

            data[tag] = child.text or ""

        return data

    def _merge(
        self,
        comic: ComicFile,
        meta: dict,
        info: dict,
    ) -> ComicMetadata:

        metadata = ComicMetadata(

            uid=meta["id"],

            filename=comic.filename,

            filepath=str(comic.filepath),

            english_title=meta["title"].get("english", ""),

            japanese_title=meta["title"].get("japanese", ""),

            title=info.get("Title", ""),

            series=info.get("Series", ""),

            translator=info.get("Translator", ""),

            format=info.get("Format", ""),

            language=info.get("LanguageISO", ""),

            page_count=int(info.get("PageCount", 0) or 0),

            favorites=meta.get("num_favorites", 0),

            upload_date=meta.get("upload_date", 0),

            year=int(info.get("Year", 0) or 0),

            month=int(info.get("Month", 0) or 0),

            day=int(info.get("Day", 0) or 0),

            web=info.get("Web", ""),
        )

        for tag in meta.get("tags", []):

            name = tag["name"]

            match tag["type"]:

                case "tag":
                    metadata.tags.append(name)

                case "parody":
                    metadata.parody.append(name)

                case "category":
                    metadata.category.append(name)

                case "artist":
                    metadata.artists.append(name)

        return metadata