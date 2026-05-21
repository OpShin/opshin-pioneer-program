from pathlib import Path

from src.utils.paths import get_week_paths

assets_dir, _, _ = get_week_paths(__file__)
on_chain_dir = Path(__file__).parent.joinpath("on_chain")
