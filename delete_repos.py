import os
from pathlib import Path

repo_names = Path('delete.txt').read_text().splitlines()

for repo_name in repo_names:
    os.system(f'gh repo delete {repo_name} --yes')