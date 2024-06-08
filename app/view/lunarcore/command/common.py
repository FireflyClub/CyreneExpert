from app.importer import *
from app.module import *


# AdminInterface
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
    clicked_ban = Signal()
    clicked_unban = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/ban @[player id] || /unban @[player id]'):
        super().__init__(icon, title, content)
        pass


class Tag(SettingCard):
    clicked_add_tag = Signal()
    clicked_remove_tag = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/tag @[player id] {add | remove} [tag]'):
        super().__init__(icon, title, content)
        pass


# WorldInterface
class Teleport(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/pos || /tp [x] [y] [z]'):
        super().__init__(icon, title, content)
        pass


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


class Multi(SettingCard):

    def __init__(self, title, icon=FluentIcon.TAG, content='/multi { join | quit | fps [Multi Display FPS] } @[player id]'):
        super().__init__(icon, title, content)
        pass


# DataInterface
class Giveall(SettingCard):
    giveall_clicked = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG,
                 content='/giveall {materials | avatars | lightcones | relics | icons}'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('材料'), self.tr('角色'), self.tr('光锥'), self.tr('遗器'), self.tr('图标')]
        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText(self.tr('选择物品'))
        self.comboBox.addItems(self.texts)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.onSignalEmit)

    def onSignalEmit(self, index: int):
        self.giveall_clicked.emit(index)


class Clear(SettingCard):
    clear_clicked = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/clear {relics | lightcones | materials | all}'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('遗器'), self.tr('光锥'), self.tr('材料'), self.tr('全部')]
        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText(self.tr('选择物品'))
        self.comboBox.addItems(self.texts)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.onSignalEmit)

    def onSignalEmit(self, index: int):
        self.clear_clicked.emit(index)


class WorldLevel(SettingCard):
    set_world_level = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/level [trailblaze level] || /worldlevel [world level]'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('开拓'), self.tr('均衡')]
        self.world_types = ComboBox(self)
        self.world_types.setPlaceholderText(self.tr('类型'))
        self.world_types.addItems(self.texts)
        self.world_types.setCurrentIndex(-1)

        self.world_level = LineEdit(self)
        self.world_level.setPlaceholderText(self.tr("世界等级"))
        validator = QIntValidator(1, 99, self)
        self.world_level.setValidator(validator)

        self.hBoxLayout.addWidget(self.world_types, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.world_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.world_level.textChanged.connect(self.onSignalEmit)
        self.world_types.currentIndexChanged.connect(self.onSignalEmit)

    def onSignalEmit(self):
        index = self.world_types.currentIndex()
        self.set_world_level.emit(index)


class Gender(SettingCard):
    gender_male = Signal()
    gender_female = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/gender {male | female}'):
        super().__init__(icon, title, content)
        self.button_male = PrimaryPushButton(self.tr('穹'), self)
        self.button_female = PrimaryPushButton(self.tr('星'), self)
        self.hBoxLayout.addWidget(self.button_male, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_female, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_male.clicked.connect(self.gender_male)
        self.button_female.clicked.connect(self.gender_female)


class Avatar(SettingCard):
    avatar_set = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/avatar [lv(level)] [r(eidolon)] [s(skill level)]'):
        super().__init__(icon, title, content)
        self.avatar_level = LineEdit(self)
        self.avatar_eidolon = LineEdit(self)
        self.avatar_skill = LineEdit(self)
        self.avatar_level.setPlaceholderText(self.tr("等级"))
        self.avatar_eidolon.setPlaceholderText(self.tr("星魂"))
        self.avatar_skill.setPlaceholderText(self.tr("行迹"))
        validator = QIntValidator(1, 99, self)
        self.avatar_level.setValidator(validator)
        self.avatar_eidolon.setValidator(validator)
        self.avatar_skill.setValidator(validator)

        self.texts = [self.tr('当前'), self.tr('队伍'), self.tr('全部')]
        self.avatar_types = ComboBox(self)
        self.avatar_types.setPlaceholderText(self.tr('应用范围'))
        self.avatar_types.addItems(self.texts)
        self.avatar_types.setCurrentIndex(-1)

        self.hBoxLayout.addWidget(self.avatar_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_eidolon, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_skill, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_types, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.avatar_level.textChanged.connect(lambda: self.onSignalEmit(-1))
        self.avatar_eidolon.textChanged.connect(lambda: self.onSignalEmit(-1))
        self.avatar_skill.textChanged.connect(lambda: self.onSignalEmit(-1))
        self.avatar_types.currentIndexChanged.connect(lambda index: self.onSignalEmit(index))

    def onSignalEmit(self, index: int):
        self.avatar_set.emit(index)
