"""Core slugification logic — pure functions, no I/O."""
from __future__ import annotations

import os
import re
import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """Convert `text` into a lowercase, URL-safe slug.

    Accented characters are transliterated to their closest ASCII
    equivalent (e.g. "e" for "é"), everything that isn't a letter or
    digit becomes `separator`, runs of separators collapse into one, and
    leading/trailing separators are stripped.
    """
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9]+", separator, lowered)
    return slug.strip(separator)


def slugify_filename(name: str, separator: str = "-") -> str:
    """Slugify a filename, preserving its extension.

    The extension is lowercased and slugified on its own (so a name like
    "My Report (Final).PDF" becomes "my-report-final.pdf") and falls back
    to no extension if it doesn't contain any letters or digits.
    """
    stem, ext = os.path.splitext(name)
    new_stem = slugify(stem, separator) or "file"
    new_ext = ""
    if ext:
        ext_body = slugify(ext.lstrip("."), separator)
        if ext_body:
            new_ext = "." + ext_body
    return new_stem + new_ext


def plan_renames(names: list[str], separator: str = "-") -> list[tuple[str, str]]:
    """Given a list of filenames, return (old, new) pairs for those whose
    slugified form differs from the original, avoiding collisions with
    other filenames (existing or newly planned) by appending -2, -3, etc.
    """
    used = set(names)
    renames: list[tuple[str, str]] = []

    for name in names:
        candidate = slugify_filename(name, separator)
        if candidate == name:
            continue

        final = candidate
        counter = 2
        while final in used and final != name:
            stem, ext = os.path.splitext(candidate)
            final = f"{stem}{separator}{counter}{ext}"
            counter += 1

        used.discard(name)
        used.add(final)
        renames.append((name, final))

    return renames
