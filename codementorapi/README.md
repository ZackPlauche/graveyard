# Codementor API

## Purpose
The purpose of this api is to be a simple web controller to implement into other projects.

It will provide be able to:
1. Interact with the website as a user
    - [x] Login
    - [ ] Send responses to job posts as the logged in profile.
    - [ ] Send messages to users as the logged in profile.
    - [ ] Update the logged in account's rate
2. Collect and scrape data from the website
    - [ ] Collect logged in User data
        - [ ] Collect all reviews of the logged in User
        - [ ] Collect all sessions of the logged in User
    - [ ] Collect all current job postings
    - [ ] Read messages from chats
3. Adapt to different popups and provide feedback loops
    - [ ] Notice when a user messages you back
    - [ ] New Post popup
    - [ ] New Live Session popup



### OOP Design Rules
- Boolean flags start with is_
- Class methods that are made from something start with from_
- Class methods or methods that are to something else start with to_

### Notes
- It was a good decision to keep this somewhat separate from the automation functionality. It's purely the WebAPI.
- BeautifulSoup is faster for parsing / scraping data. It's good to have an API that can do both.

## Usage
Get open_requests
```python
codementor = CodementorAPI.start()
open_requests = codementor.get_open_requests()
```

## Robustify
- [ ] Make the script not close on losing wifi, make it handle the exception and continue running on a while loop.
- [ ] 

## Problems / Bugs
- Human Verification
    - When using a driver with a default profile, Codementor added a bot detection challenge.
    - [x] Can potentially be solved if you do it once and the script DOESN'T stop working after that.
        - [x] Solution: All in the default profile. Kill the current driver instance. Open Codementor in a new window not in headless mode. Solve the puzzle. Close it. And open it again. This will make the script semi-automatic. Implemented.
2. [ ] Occasionally the reCaptcha will trigger when logging in, typically this can be fixed by either refreshing the page or killing that instance of the webdriver and creating a new one, running the process again. 
3. [ ] The human verification popup is coming even before that...

# Resolved
- [x] Headless browser doesn't load login page results at all. 
    - [ ] Solution: Make a login loop for that situation.



## Next Project Steps
- Automation
    - [ ] Follow ups
- Data & Stats
    - [ ] Market share based on tag


### Misc Endpoints
- List: https://api.codementor.io/api/v2/requests/search?search_type=related
- Next step in list: https://api.codementor.io/api/v2/requests/search?before_timestamp=1692428770&search_type=related
- Next step in list: https://api.codementor.io/api/v2/requests/search?before_timestamp=1692352896&search_type=related
- Detail: https://api.codementor.io/api/v2/requests/<request-id>?access_as=mentor
- Interest: https://api.codementor.io/api/v2/requests/<request-id>?access_as=mentor
- Message: https://api.codementor.io/api/v2/chats/messages/<username>