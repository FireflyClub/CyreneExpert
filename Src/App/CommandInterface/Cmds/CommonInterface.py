from Src.Import import *
from Src.Util import *


class Help(SettingCard):
    signal = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/help [cmd]'):
        super().__init__(icon, title, content)
        self.line = LineEdit(self)
        self.line.setPlaceholderText(self.tr("命令"))
        self.button = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.line, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.signal)


class Lineup(SettingCard):
    lineup_signal = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/lineup {mp | sp | heal}'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('秘技点'), self.tr('能量'), self.tr('治疗')]
        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText(self.tr('选择物品'))
        self.comboBox.addItems(self.texts)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.lineup_signal)


class Unstuck(SettingCard):
    unstuck_signal = Signal()

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
        self.button_unstuck.clicked.connect(self.unstuck_signal)


class Common(SettingCardGroup):
    command_update = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.helpCard = Help(
            self.tr('命令帮助')
        )
        self.lineupCard = Lineup(
            self.tr('队伍数据修改')
        )
        self.unstuckCard = Unstuck(
            self.tr('解除场景未加载卡死')
        )

    def __initLayout(self):
        self.addSettingCard(self.helpCard)
        self.addSettingCard(self.lineupCard)
        self.addSettingCard(self.unstuckCard)

    def __connectSignalToSlot(self):
        self.helpCard.signal.connect(self.handleHelpClicked)
        self.lineupCard.lineup_signal.connect(self.handleLineupClicked)
        self.unstuckCard.unstuck_signal.connect(self.handleUnstuckClicked)

    def handleHelpClicked(self):
        cmd = self.helpCard.line.text()
        if (cmd != ''): cmd = ' ' + cmd
        self.command_update.emit('/help' + cmd)

    def handleLineupClicked(self):
        itemid = self.lineupCard.comboBox.currentIndex()
        types = ['mp', 'sp', 'heal']
        self.command_update.emit('/lineup ' + types[itemid])

    def handleUnstuckClicked(self):
        stuck_uid = self.unstuckCard.stuck_uid.text()
        if stuck_uid != '':
            self.command_update.emit('/unstuck @' + stuck_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))
