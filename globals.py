from pathlib import Path


repos = [path for path in Path(__file__).parent.iterdir() if path.name != '.git' and path.is_dir()]