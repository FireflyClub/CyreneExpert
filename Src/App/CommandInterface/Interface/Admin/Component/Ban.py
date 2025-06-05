from Src.Import import *
from Src.Util import *


class Ban(SettingCard):
    signal = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/ban {add | delete}'):
        super().__init__(icon, title, content)
        pass
