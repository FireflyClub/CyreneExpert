from Src.Import import *
from Src.Util import *


class Windy(SettingCard):
    signal = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/windy. A mysterious cmd.'):
        super().__init__(icon, title, content)
        self.button = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.signal)
