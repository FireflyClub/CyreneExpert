from Src.Import import *
from Src.Util import *


class Reload(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/reload { all | config | res}'):
        super().__init__(icon, title, content)
        pass


class Announce(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/anno [text]. Sends a message to all players on the server.'):
        super().__init__(icon, title, content)
        pass


class Account(SettingCard):
    create_account = Signal()
    delete_account = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/account {create | delete} [username]'):
        super().__init__(icon, title, content)
        self.account_name = LineEdit(self)
        self.account_uid = LineEdit(self)
        self.button_create = PrimaryPushButton(self.tr('添加'), self)
        self.button_delete = PrimaryPushButton(self.tr('删除'), self)
        self.account_name.setPlaceholderText(self.tr("名称"))
        self.account_uid.setPlaceholderText("UID")
        self.account_uid.setValidator(QIntValidator(self))
        self.hBoxLayout.addWidget(self.account_name, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.account_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_create, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_delete, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_create.clicked.connect(self.create_account)
        self.button_delete.clicked.connect(self.delete_account)


class Permission(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/permission {add ( player | vip | admin ) | remove | clear} [permission]'):
        super().__init__(icon, title, content)
        pass


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


class Ban(SettingCard):
    signal = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/ban {add | delete}'):
        super().__init__(icon, title, content)
        pass


class Windy(SettingCard):
    signal = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/windy. A mysterious cmd.'):
        super().__init__(icon, title, content)
        self.button = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.signal)

class Admin(SettingCardGroup):
    command_update = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.accountCard = Account(
            self.tr('管理账号')
        )
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
        self.accountCard.create_account.connect(lambda: self.handleAccountClicked('create'))
        self.accountCard.delete_account.connect(lambda: self.handleAccountClicked('delete'))
        self.kickCard.kick_player.connect(self.handleKickClicked)
        self.windyCard.signal.connect(lambda: self.command_update.emit('/windy'))

    def handleKickClicked(self):
        account_uid = self.kickCard.account_uid.text()
        if account_uid != '':
            self.command_update.emit('/kick @' + account_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))

    def handleAccountClicked(self, types):
        account_name = self.accountCard.account_name.text()
        account_uid = self.accountCard.account_uid.text()
        if account_name != '':
            account = f'/account {types} {account_name}'
            if types == 'create' and account_uid != '':
                account += ' ' + account_uid
            self.command_update.emit(account)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的用户名!'))
