from Src.Import import *
from Src.Util import *


class Announce(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/anno [text]. Sends a message to all players on the server.'):
        super().__init__(icon, title, content)
        pass
