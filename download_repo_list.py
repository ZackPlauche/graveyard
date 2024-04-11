import time
import os
from pathlib import Path


temp_file = Path('temp.txt')
output_file = Path('repos.txt')

# List repo names and write to file in format of only their name, not in json, just text
os.system('gh repo list > temp.txt')

time.sleep(2)

repo_names = []
for line in temp_file.read_text().splitlines():
    repo_names.append(line.split()[0])

output_file.write_text('\n'.join(repo_names))
temp_file.unlink()

