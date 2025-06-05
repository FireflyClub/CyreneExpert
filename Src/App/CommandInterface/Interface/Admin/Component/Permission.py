from Src.Import import *
from Src.Util import *


class Permission(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/permission {add ( player | vip | admin ) | remove | clear} [permission]'):
        super().__init__(icon, title, content)
        pass
