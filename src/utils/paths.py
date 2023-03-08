from pathlib import Path


def get_week_paths(path):
    """
    To be called in `__init__.py` with the `__file__` argument in the week## directory.
    """
    assets_dir = Path(path).parent.joinpath("assets")
    homework_dir = Path(path).parent.joinpath("homework")
    lecture_dir = Path(path).parent.joinpath("lecture")
    return assets_dir, homework_dir, lecture_dir
