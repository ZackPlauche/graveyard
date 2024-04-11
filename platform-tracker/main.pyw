import os
from time import sleep

scripts = [
    'codementor_autopilot.py',
    'wyzant_autopilot.py',
]

for script in scripts:
    os.system(f'start {script}')
    sleep(3)