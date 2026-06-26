from __future__ import annotations

from pathlib import Path

PROJECT_NAME = "ComicReader"
PROJECT_VERSION = "0.1.0"

ROOT_DIR = Path(__file__).resolve().parents[2]

COMICS_DIR = ROOT_DIR / "comics"
COVERS_DIR = ROOT_DIR / "covers"
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = ROOT_DIR / "cache"

SUPPORTED_ARCHIVES = (".cbz",)

META_JSON = "meta.json"
COMICINFO_XML = "ComicInfo.xml"