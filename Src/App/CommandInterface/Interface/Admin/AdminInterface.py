from Src.Import import *
from Src.Util import *
from .Component import *


class Admin(SettingCardGroup):
    command_update = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.accountCard = Account()
        self.permissionCard = Permission(
            self.tr('管理权限')
        )
        self.kickCard = Kick(
            self.tr('踢出玩家')
        )
        self.banCard = Ban(
            self.tr('封禁玩家'),
        )
        self.reloadCard = Reload(
            self.tr('重载服务端数据')
        )
        self.announceCard = Announce(
            self.tr('发送公告')
        )
        self.windyCard = Windy(
            self.tr('Windy!')
        )

    def __initLayout(self):
        self.addSettingCard(self.accountCard)
        self.addSettingCard(self.permissionCard)
        self.addSettingCard(self.kickCard)
        self.addSettingCard(self.banCard)
        self.addSettingCard(self.reloadCard)
        self.addSettingCard(self.announceCard)
        self.addSettingCard(self.windyCard)

    def __connectSignalToSlot(self):
        self.accountCard.command_update.connect(self.command_update.emit)
        self.kickCard.kick_player.connect(self.handleKickClicked)
        self.windyCard.signal.connect(lambda: self.command_update.emit('/windy'))

    def handleKickClicked(self):
        account_uid = self.kickCard.account_uid.text()
        if account_uid != '':
            self.command_update.emit('/kick @' + account_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))
