"""Core scanning logic for leftover Git conflict markers."""
import fnmatch
import os

DEFAULT_IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf",
    ".zip", ".gz", ".tar", ".tgz", ".bin", ".exe", ".so",
    ".dylib", ".dll", ".woff", ".woff2", ".ttf", ".otf",
}


def _is_marker(line):
    s = line.strip()
    return (
        s.startswith("<<<<<<<")
        or s == "======="
        or s.startswith(">>>>>>>")
    )


def scan_file(path):
    """Return list of (path, lineno, marker_text) tuples for a single file."""
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                if _is_marker(line):
                    findings.append((str(path), lineno, line.rstrip("\r\n")))
    except OSError:
        return findings
    return findings


def _ignored(path, ignore):
    name = os.path.basename(path)
    for pat in ignore:
        if fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(path, pat):
            return True
    return False


def scan_dir(root, ignore=None, extensions=None):
    """Walk root and collect conflict-marker findings."""
    ignore = list(ignore or [])
    extensions = [e.lower() for e in (extensions or [])]
    results = []

    for dirpath, dirnames, filenames in os.walk(root):
        kept_dirs = []
        for d in dirnames:
            full = os.path.join(dirpath, d)
            if d in DEFAULT_IGNORED_DIRS or _ignored(full, ignore):
                continue
            kept_dirs.append(d)
        dirnames[:] = kept_dirs

        for name in filenames:
            full = os.path.join(dirpath, name)
            if _ignored(full, ignore):
                continue
            if name.lower() in BINARY_EXTENSIONS or any(
                name.lower().endswith(ext) for ext in BINARY_EXTENSIONS
            ):
                continue
            if extensions and not any(name.lower().endswith(e) for e in extensions):
                continue
            results.extend(scan_file(full))

    return results
