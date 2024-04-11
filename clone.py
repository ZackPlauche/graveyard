import os
from pathlib import Path

repos = Path('delete.txt').read_text().splitlines()
for repo in repos:
    os.system(f'gh repo clone {repo}')