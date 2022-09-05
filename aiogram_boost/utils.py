from pathlib import Path


def is_dir_empty(path: Path) -> bool:
    return not list(path.glob('*'))
