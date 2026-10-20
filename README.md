# conflict-marker

A small, zero-dependency command-line tool that scans a directory tree for leftover Git conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) that sometimes survive a botched merge or rebase.

## Features

- Recursively scans files for unresolved conflict markers.
- Reports each finding as `path:line: marker`.
- Skips common binary file types and noisy directories (`.git`, `node_modules`, virtualenvs, caches).
- Supports ignore patterns and extension filters.
- Optional JSON output for CI integration.
- Non-zero exit code when markers are found, so it can gate commits or pipelines.

## Install

No external dependencies are required. Python 3.8+ is enough.

```sh
# Run directly
git clone https://github.com/example/conflict-marker.git
cd conflict-marker
python3 conflict_marker.py .

# Or install as a script
pip install .
```

## Usage

```sh
# Scan current directory
python3 conflict_marker.py .

# Scan a specific path
python3 conflict_marker.py src/

# Ignore directories or globs
python3 conflict_marker.py . --ignore tests --ignore '*.min.js'

# Only scan certain extensions
python3 conflict_marker.py . --ext .py --ext .js

# JSON output for tooling
python3 conflict_marker.py . --json
```

Example output:

```
src/app.py:12: <<<<<<< HEAD
src/app.py:13: =======
src/app.py:14: >>>>>>> feature-branch
```

Exit status is `1` when any marker is found and `0` otherwise.

## License

MIT
