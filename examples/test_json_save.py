import lastfm
import random

# this example is hardcoded for the JsonDatabaseHandler
database = lastfm.PylastSessionHandler(lastfm.JsonDatabaseHandler, 'test.json')

session = lastfm.Session(api_key, api_secret, SessionDatabaseHandler=database)

print(f"the authorization url, please open this in a browser and authorize it: {session.url}")
input("press enter when you are done >")

try:
    key = session.get_session_key() # AFTER the url is opened and authorized, we can get the key
except lastfm.PylastUrlNotAuthorized:
    print("you did not authorize the application with the url, exiting...")
    exit(0)
print("got the session key") # its been authorized, you can now save this key and use it
num = random.randint(10,50) # with discord, you would use the user's ID
print(f"saving under {num}")
database.data[num] = key
database.save()
print("saved key")
session.finalize()
# you can now use the session as normal
# the session class inherits the pylast network so no need to do session.network.get_track
# example below

session.search_for_track("suicideboys", "cerberus")