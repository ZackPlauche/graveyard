import os
from globals import repos

git_count = 0

for repo in repos:
    for path in repo.iterdir():
        if path.name == '.git' and path.is_dir():
            git_count += 1
            os.system(f'rmdir /S/q {path}')
            print(f'Deleted .git folder at location {path}')

print('Total .git folders deleted:', git_count)
