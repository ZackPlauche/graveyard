# Wyzant API
A Wyzant (currently) selenium api to interact with the Wyzant website. 

https://github.com/ZackPlauche/wyzantapi

## Installation
```cmd
pip install git+https://github.com/ZackPlauche/wyzantapi.git#egg=wyzantapi
```

Upgrade:
```cmd
pip install --upgrade git+https://github.com/ZackPlauche/wyzantapi.git#egg=wyzantapi
```


## Features Include
- Collecting job data
- Applying to jobs
- Structured OOP 

## MVP Requirements
1. [x] Be able to login
2. [x] Be able to get a list of all fully detailed jobs
    1. [x] Be able to get data from all of the job cards as you're going through them.
        1. [ ] Add published_at time calculation
    2. [ ] Be able to update the job details even more by visiting the job details page.
        - [ ] Collect card_info_on_file
3. [x] Be able to apply for a job

## Improvements to make
- [ ] Learn how to use `requests` instead to be more efficient.