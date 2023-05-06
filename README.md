# Pylast Wrapper
 Wrapper for pylast to make some things easier
 
 
# Main focus 
 Key based sessions\
 Simple pre-made database(s) to save session keys
 
# Installation 
 For now, all you do is add `lastfm.py` to your project folder, then import it and use it based on the examples or (future) documentation.

# For now
 Everything is in one file, that will change.\
 Naming might not be right, classes are prone to name changes, function naming might be changed, etc.\
 Documentation is **zero**, please look at the examples (test_*). i will work on it when the project is in a publishable state, please be patient.\
 (No garuntees on pylast documentation itself, i will try to make this project as simple to use as possible, even without knowing how to use pylast)

# Console Key Creation Example
```py
import lastfm

session = lastfm.Session(api_key, api_secret)

print(f"the authorization url, please open this in a browser and authorize it: {session.url}")
input("press enter when you are done >")

try:
    key = session.get_session_key() # AFTER the url is opened and authorized, we can get the key
except lastfm.PylastUrlNotAuthorized:
    print("you did not authorize the application with the url, exiting...")
    exit(0)

session.finalize()


data = session.search_for_track("songname", "artist") # away we go, you would work from here
```
