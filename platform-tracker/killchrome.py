
# Kill all instances of chrome

import os 

exes = ['chrome.exe', 'brave.exe']

def killchrome():
    for exe in exes:
        os.system(f'taskkill /f /im {exe}')

killchrome()