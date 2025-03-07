from src.head import *
from src.util import *


class Unstuck(SettingCard):
    unstuck_player = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/unstuck @[player id]'):
        super().__init__(icon, title, content)
        self.stuck_uid = LineEdit(self)
        self.stuck_uid.setPlaceholderText("UID")
        self.stuck_uid.setValidator(QIntValidator(self))
        self.button_unstuck = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.stuck_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_unstuck, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_unstuck.clicked.connect(self.unstuck_player)


class Common(SettingCardGroup):
    command_update = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.helpCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('命令帮助'),
            '/help'
        )
        self.refillCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('秘技点补充'),
            '/refill'
        )
        self.energyCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('能量恢复'),
            '/energy'
        )
        self.healCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('治疗角色'),
            '/heal'
        )
        self.unlockfpsCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('解锁帧率'),
            '/unlockfps'
        )
        self.unstuckCard = Unstuck(
            self.tr('解除场景未加载卡死')
        )

    def __initLayout(self):
        self.addSettingCard(self.helpCard)
        self.addSettingCard(self.refillCard)
        self.addSettingCard(self.energyCard)
        self.addSettingCard(self.healCard)
        self.addSettingCard(self.unlockfpsCard)
        self.addSettingCard(self.unstuckCard)

    def __connectSignalToSlot(self):
        self.helpCard.clicked.connect(lambda: self.command_update.emit('/help'))
        self.refillCard.clicked.connect(lambda: self.command_update.emit('/refill'))
        self.energyCard.clicked.connect(lambda: self.command_update.emit('/energy'))
        self.healCard.clicked.connect(lambda: self.command_update.emit('/heal'))
        self.unlockfpsCard.clicked.connect(lambda: self.command_update.emit('/unlockfps'))
        self.unstuckCard.unstuck_player.connect(self.handleUnstuckClicked)

    def handleUnstuckClicked(self):
        stuck_uid = self.unstuckCard.stuck_uid.text()
        if stuck_uid != '':
            self.command_update.emit('/unstuck @' + stuck_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))
