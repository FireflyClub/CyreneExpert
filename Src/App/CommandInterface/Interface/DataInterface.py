from Src.Import import *
from Src.Util import *


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


class Data(SettingCardGroup):
    command_update = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.giveallCard = Giveall(
            self.tr('给予全部')
        )
        self.clearCard = Clear(
            self.tr('清空物品')
        )
        self.worldLevelCard = WorldLevel(
            self.tr('设置世界等级')
        )
        self.avatarCard = Avatar(
            self.tr('设置角色属性')
        )
        self.genderCard = Gender(
            self.tr('设置开拓者性别')
        )

    def __initLayout(self):
        self.addSettingCard(self.giveallCard)
        self.addSettingCard(self.clearCard)
        self.addSettingCard(self.worldLevelCard)
        self.addSettingCard(self.genderCard)
        self.addSettingCard(self.avatarCard)

    def __connectSignalToSlot(self):
        self.giveallCard.giveall_clicked.connect(lambda itemid: self.handleGiveallClicked(itemid))
        self.clearCard.clear_clicked.connect(lambda itemid: self.handleClearClicked(itemid))
        self.worldLevelCard.set_world_level.connect(lambda index: self.handleWorldLevelClicked(index))
        self.genderCard.gender_male.connect(lambda: self.command_update.emit('/gender male'))
        self.genderCard.gender_female.connect(lambda: self.command_update.emit('/gender female'))
        self.avatarCard.avatar_set.connect(lambda index: self.handleAvatarClicked(index))

    def handleUnstuckClicked(self):
        stuck_uid = self.unstuckCard.stuck_uid.text()
        if stuck_uid != '':
            self.command_update.emit('/unstuck @' + stuck_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))

    def handleGiveallClicked(self, itemid):
        types = ['materials', 'avatars', 'lightcones', 'relics', 'icons']
        self.command_update.emit('/giveall ' + types[itemid])

    def handleClearClicked(self, itemid):
        types = ['relics', 'lightcones', 'lightcones', 'all']
        self.command_update.emit('/clear ' + types[itemid])

    def handleWorldLevelClicked(self, index):
        world_level = self.worldLevelCard.world_level.text()
        if world_level != '':
            if index == 0:
                self.command_update.emit('/traillevel ' + world_level)
            elif index == 1:
                self.command_update.emit('/worldlevel ' + world_level)
        else:
            self.command_update.emit('')

    def handleAvatarClicked(self, index):
        avatar_level = self.avatarCard.avatar_level.text()
        avatar_eidolon = self.avatarCard.avatar_eidolon.text()
        avatar_skill = self.avatarCard.avatar_skill.text()
        types = ['', ' lineup', ' all']
        command = '/avatar'
        if index > -1:
            command += types[index]
        if avatar_level != '':
            command += ' lv' + avatar_level
        if avatar_eidolon != '':
            command += ' r' + avatar_eidolon
        if avatar_skill != '':
            command += ' s' + avatar_skill
        if command != '/avatar':
            self.command_update.emit(command)
        else:
            self.command_update.emit('')
