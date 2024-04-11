import inquirer

# Kill instances of chrome.exe for chrome and chrome beta.
import subprocess

browser_map = {
    'chrome': 'chrome.exe',
    'chrome beta': 'chrome.exe',
    'brave': 'brave.exe',
}

choice_map = {
    'all': list(browser_map.values()),
    'chromes': [browser_map['chrome'], browser_map['chrome beta']],
    **browser_map,
}

response = inquirer.prompt([
    inquirer.List(
        'browser', 
        message='Which browser would you like to kill?',
        choices=list([key.title() for key in choice_map.keys()])
    )
])

while True:
    browser = response['browser'].lower()
    choice = choice_map[browser]
    if isinstance(choice, list):
        for browser_path in choice:
            subprocess.call(f'taskkill /f /im {browser_path}', shell=True)
    else:
        browser_path = choice
        subprocess.call(f'taskkill /f /im {browser_path}', shell=True)
    break