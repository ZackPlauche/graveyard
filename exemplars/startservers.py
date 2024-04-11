from pathlib import Path
import os
import subprocess

frontend = Path('frontend').resolve()
backend = Path('backend').resolve()

# Change directory to frontend and start nuxt dev server
os.chdir(frontend)
subprocess.Popen('yarn dev', shell=True)

# Change directory back to the original directory and start Django server
os.chdir(backend)
subprocess.Popen('python manage.py runserver', shell=True)
