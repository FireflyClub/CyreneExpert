from Src.Import import *
from Src.Util import *


class Kick(SettingCard):
    kick_player = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/kick @[player id]'):
        super().__init__(icon, title, content)
        self.account_uid = LineEdit(self)
        self.account_uid.setPlaceholderText("UID")
        self.account_uid.setValidator(QIntValidator(self))
        self.button_kick = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.account_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_kick, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_kick.clicked.connect(self.kick_player)
