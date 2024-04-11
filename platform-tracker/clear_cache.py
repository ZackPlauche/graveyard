# Clear all pycache files in the current directory tree using pathlib 
from pathlib import Path

for path in Path('.').rglob('*.pyc'):
    path.unlink()