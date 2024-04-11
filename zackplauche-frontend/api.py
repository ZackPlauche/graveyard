import os
import sys
from pathlib import Path

api_server_dir = Path.home() / 'Code/zackplauche-backend'
command = ' '.join(sys.argv[1:]) if sys.argv[1:] else 'runserver'

if api_server_dir.exists():
    os.chdir(api_server_dir)
    os.system(f'pipenv run python manage.py {command}')