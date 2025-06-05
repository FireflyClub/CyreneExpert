from Src.Import import *
from Src.Util import *


class Reload(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/reload { all | config | res}'):
        super().__init__(icon, title, content)
        pass
