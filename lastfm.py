import pylast, json
import pathlib
#from ..other import insert_pylast_info
#SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")

# Errors

class PylastUrlNotAuthorized(Exception):
    def __init__(self) -> None:
        super().__init__("URL has not been authorized, please prompt the user to authorize the application from the URL")

# Database Handlers

class JsonDatabaseHandler(object):
    def __init__(self, file_path: str | pathlib.Path) -> None:
        self.file_path = file_path
        self._data = None

    @property
    def data(self):
        return self._data

    # TODO: fix this, it straight up doesnt work
    #@data.setter
    #def data(self, data, data2):
    #    print(f'data 1: {data}\n data 2: {data2}')

    def load(self, path: str = None):
        if path == None: path = self.file_path
        if path == None: return None
            
        data = json.loads(open(path, 'r').read())
        self._data = data

    def save(self):
        with open(self.file_path, 'w+') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
            f.close()
        return True

class SQLiteDatabaseHandler(object):
    pass

class InMemoryDatabaseHandler(object):
    pass


# Session handler

class PylastSessionHandler:
    def __init__(self, database_handler: JsonDatabaseHandler | SQLiteDatabaseHandler, db_path: str = None):
        self._handler = database_handler(db_path)
        self.backup = None
        if db_path != None:
            self.load(db_path)

    @property
    def data(self):
        return self._handler.data

    def json_data_set(self, data: dict):
        """ Only for use with the JsonDatabaseHandler handler, sets the internal db"""
        if self._handler == JsonDatabaseHandler:
            self._handler._data = data

    def save(self, data: dict = None):
        """ Saves all the data in the SessionHandler, or optionally, saves data from a dict (json only)"""
        if self._backup() == True:
            if data != None:
                if self._handler == JsonDatabaseHandler:
                    self._handler.data = data
                else:
                    raise Exception("Tried save data with non-json database handler")
            if self._handler.save() == True:
                return True
        else:
            pass # TODO: Create custom error 

    def load(self, file_path: str | pathlib.Path):
        if self._handler.data != None:
            self._backup()
        self._handler.load(file_path)

    def _backup(self):
        """ Internal function for backing up self.data """
        if self._handler.data != None:
            self.backup == self.data
        return True

class PylastSessionCreator(object):
    def __init__(self, api_key: str, api_secret: str,  network: pylast.LastFMNetwork = None):
        """ Takes pylast.LastFMNetwork and gives an object to work with, example below:
                session = PylastSessionCreator(pylast_network_object)
                print(session.url) # the url to authenticate the application (first time only, or when it expires)
                session_key = session.get_session_key() # returns None if the url was not authenticated, or if it was, it returns the session key.
                session_skg = session.skg 

        """
        if network == None:
            self.network = pylast.LastFMNetwork(api_key, api_secret)
        else:
            self.network = network
        self.skg = pylast.SessionKeyGenerator(self.network)
        self.url = self.skg.get_web_auth_url()

    def get_session_key(self):
        try:
            return self.skg.get_web_auth_session_key(self.url)
        except pylast.WSError:
            raise PylastUrlNotAuthorized()


class Session(PylastSessionCreator, pylast.LastFMNetwork):
    """ Works ontop of Pylast, working the same as pylast.network, leaving all the hard work related to key sessions already done, though you can still access everything as normal.
        If you want to use the PylastSessionHandler, please create the object with needed arguments/etc.
    """
    def __init__(self, api_key: str, api_secret: str, network: pylast.LastFMNetwork = None, session_key: str = None, SessionDatabaseHandler: PylastSessionHandler = None): 
        super().__init__(api_key, api_secret, network)
        if session_key != None:
            self.network.session_key = session_key
        if SessionDatabaseHandler != None:
            self.database_handler = SessionDatabaseHandler

    def finalize(self):
        """ After the user authorizes with the URL, run this function to set the key, or do it yourself. Errors if the user has not authorized yet, returns True if they have. """
        try:
            self.network.session_key = self.get_session_key()
        finally:
            return True





### MPL // example usage
## Ignore this

class PylastTerminal:
    def __init__(self, key: str = None, username: str = None, api_key: str = None, api_secret: str = None):
        if api_key or api_secret == None:
            self.first_run()
        else:
            self.network = pylast.LastFMNetwork()

    def _create_url(self):
        temp = PylastSessionCreator(self.network)
        print(f"\n{temp.url}")
        prompt = input("Please authorize the application you created on Last.FM with the URL above, then press enter.")
        session_key = temp.get_session_key()
        if session_key == None:
            print("You did not authorize the application, please redo this.")
        else:
            print("Your session key has been created.")
        username = input("If you would like to set your username (we cannot access your username), please set one now. >")
        if username == None or username == "":
            username = "None"
            print("Username has been set to 'None'")
        print("Creating lastfm network.")
        self.network = pylast.LastFMNetwork(session_key=session_key, api_key=self.api_key, api_secret=self.api_secret)
        print("Set the session key.")
        #insert_pylast_info(session_key, username)
        print("Saved username/session key.")
        input("To automatically scrobble what you play, please enable auto scrobble in the config.json.\nPlease note that this works best with songs you have locally and saved/manually put the metadata in for, as with any music without metadata will have the song name ran through a 3rd party site to get EXACT metadata as Last.FM requires.")


    def first_run(self):
        print("First run detected, please create a last.fm application, put the key and secret in the config file.")
        input("Press enter when you have created it.")
        print("Starting Auth process.")
        self._create_url(self.network)
