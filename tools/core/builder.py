from __future__ import annotations

from datetime import datetime

from .models import ComicMetadata


class Builder:

    def build(self, comics: list[ComicMetadata]) -> dict:

        comics.sort(
            key=lambda c: (
                c.series.lower(),
                c.title.lower(),
                c.uid,
            )
        )

        library = {
            "schema": 1,
            "builder": "0.1.0",
            "generated": datetime.now().isoformat(timespec="seconds"),
            "stats": {
                "entries": len(comics),
                "pages": sum(c.page_count for c in comics),
                "languages": len(
                    {
                        c.language
                        for c in comics
                        if c.language
                    }
                ),
                "formats": len(
                    {
                        c.format
                        for c in comics
                        if c.format
                    }
                ),
                "tags": len(
                    {
                        tag
                        for comic in comics
                        for tag in comic.tags
                    }
                ),
            },
            "library": [],
        }

        for comic in comics:

            entry = {
                "uid": comic.uid,
                "cover": str(comic.uid),
                "file": comic.filename,
                "title": {
                    "display": comic.title,
                    "english": comic.english_title,
                    "japanese": comic.japanese_title,
                },
                "metadata": {
                    "series": comic.series,
                    "translator": comic.translator,
                    "format": comic.format,
                    "language": comic.language,
                    "pages": comic.page_count,
                    "favorites": comic.favorites,
                    "upload_date": comic.upload_date,
                    "year": comic.year,
                    "month": comic.month,
                    "day": comic.day,
                },
                "tags": {
                    "tag": sorted(comic.tags),
                    "parody": sorted(comic.parody),
                    "category": sorted(comic.category),
                    "artist": sorted(comic.artists),
                },
                "search": self._build_search(comic),
            }

            library["library"].append(entry)

        return library

    def _build_search(self, comic: ComicMetadata) -> list[str]:

        values = set()

        def add(value: str):

            if value:
                values.add(value.strip().lower())

        add(comic.title)
        add(comic.english_title)
        add(comic.japanese_title)
        add(comic.series)
        add(comic.translator)

        for tag in comic.tags:
            add(tag)

        for tag in comic.parody:
            add(tag)

        for tag in comic.category:
            add(tag)

        for tag in comic.artists:
            add(tag)

        return sorted(values)