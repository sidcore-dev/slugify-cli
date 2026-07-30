# slugify-cli

A small, dependency-free command-line tool that converts text into
URL-safe slugs, or slugifies every filename in a directory.

## Why

Slugs show up everywhere — blog post URLs, branch names, export
filenames — and hand-rolling the conversion (lowercase, strip accents,
collapse punctuation) is a small chore that's easy to get wrong on edge
cases like accented characters or repeated punctuation. `slugify-cli`
handles that once, consistently, from the command line.

## Install

```bash
pip install .
```

This installs a `slugify-cli` command on your PATH.

## Usage

### Slugify text

```bash
$ slugify-cli "Hello, World!" "Café  Society"
hello-world
cafe-society
```

Or pipe lines in from stdin:

```bash
$ printf 'First Post!\nÉlan Vital\n' | slugify-cli
first-post
elan-vital
```

### Slugify filenames in a directory

```bash
$ slugify-cli --rename ./exports
My Report (Final).PDF -> my-report-final.pdf
Q3 Notes.txt -> q3-notes.txt

Dry run: 2 file(s) would be renamed. Re-run with --apply to rename them.
```

`--rename` defaults to a dry run — it only prints what it *would* do.
Nothing is renamed on disk until you pass `--apply`:

```bash
slugify-cli --rename ./exports --apply
```

Only files directly inside the given directory are considered
(subdirectories are not recursed into or renamed). If two files would
slugify to the same name, later ones get `-2`, `-3`, etc. appended so no
file is silently overwritten.

### Options

| Flag           | Description                                                        |
|----------------|----------------------------------------------------------------------|
| `--rename DIR` | Slugify filenames in `DIR` instead of slugifying text               |
| `--apply`      | Actually perform the renames planned by `--rename` (default: dry run) |
| `--separator`  | Separator character to use in slugs (default: `-`)                  |

### Exit codes

- `0` — completed successfully (including a clean dry run)
- `2` — `--rename` target isn't a directory, or a rename failed

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
