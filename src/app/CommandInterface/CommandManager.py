from .Cmds import *
from src.util import *
from src.head import *
# from src.app.remote.common import handleCommandSend

class CommandManager(ScrollArea):
    command_update = Signal(str)

    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.AdminInterface = SettingCardGroup(self.scrollWidget)
        self.statusCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('服务端状态'),
            '/status'
        )
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
        self.tagCard = Tag(
            self.tr('设置标签')
        )
        self.reloadCard = Reload(
            self.tr('重载服务端数据')
        )
        self.announceCard = Announce(
            self.tr('发送公告')
        )
        self.CommonInterface = SettingCardGroup(self.scrollWidget)
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
        self.WorldInterface = SettingCardGroup(self.scrollWidget)
        self.teleportCard = Teleport(
            self.tr('传送配置')
        )
        self.unstuckCard = Unstuck(
            self.tr('解除场景未加载卡死')
        )
        self.multiCard = Multi(
            self.tr('多人模式配置'),
        )
        self.DataInterface = SettingCardGroup(self.scrollWidget)
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

        self.pager = HorizontalPipsPager(self.AdminInterface)
        self.pager.setPageNumber(2)
        self.pager.setVisibleNumber(2)
        self.pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        self.pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        self.pager.setCurrentIndex(0)

        self.updateText = LineEdit()
        self.updateText.setFixedSize(740, 35)
        self.clearButton = PrimaryPushButton(self.tr('清空'))
        self.saveButton = PrimaryPushButton(self.tr('保存'))
        self.copyButton = PrimaryPushButton(self.tr('复制'))
        self.actionButton = PrimaryPushButton(self.tr('执行'))
        self.clearButton.setFixedSize(80, 35)
        self.saveButton.setFixedSize(80, 35)
        self.copyButton.setFixedSize(80, 35)
        self.actionButton.setFixedSize(80, 35)
        self.updateContainer = QWidget()

    def __initLayout(self):
        self.page_components = {
            0: [self.statusCard,
                self.accountCard,
                self.permissionCard,
                self.kickCard,
                self.banCard,
                self.tagCard],
            1: [self.reloadCard,
                self.announceCard],
        }
        for cur_index in self.page_components:
            for card in self.page_components[cur_index]:
                self.AdminInterface.addSettingCard(card)

        self.CommonInterface.addSettingCard(self.helpCard)
        self.CommonInterface.addSettingCard(self.refillCard)
        self.CommonInterface.addSettingCard(self.energyCard)
        self.CommonInterface.addSettingCard(self.healCard)
        self.CommonInterface.addSettingCard(self.unlockfpsCard)

        self.WorldInterface.addSettingCard(self.teleportCard)
        self.WorldInterface.addSettingCard(self.unstuckCard)
        self.WorldInterface.addSettingCard(self.multiCard)

        self.DataInterface.addSettingCard(self.giveallCard)
        self.DataInterface.addSettingCard(self.clearCard)
        self.DataInterface.addSettingCard(self.worldLevelCard)
        self.DataInterface.addSettingCard(self.genderCard)
        self.DataInterface.addSettingCard(self.avatarCard)

        InitUI.addSubInterface(self, self.AdminInterface, 'AdminInterface', self.tr('管理'), icon=FluentIcon.COMMAND_PROMPT)
        InitUI.addSubInterface(self, self.CommonInterface, 'CommonInterface', self.tr('常用'), icon=FluentIcon.COMMAND_PROMPT)
        InitUI.addSubInterface(self, self.WorldInterface, 'WorldInterface', self.tr('世界'), icon=FluentIcon.COMMAND_PROMPT)
        InitUI.addSubInterface(self, self.DataInterface, 'DataInterface', self.tr('数据'), icon=FluentIcon.COMMAND_PROMPT)

        self.CustomInterface = Custom('CustomInterface', self)
        InitUI.addSubInterface(self, self.CustomInterface, 'CustomInterface', self.tr('自定义'), icon=FluentIcon.COMMAND_PROMPT)
        self.SceneInterface = Scene('SceneInterface', self)
        InitUI.addSubInterface(self, self.SceneInterface, 'SceneInterface', self.tr('场景'), icon=FluentIcon.COMMAND_PROMPT)
        self.GiveInterface = Give('GiveInterface', self)
        InitUI.addSubInterface(self, self.GiveInterface, 'GiveInterface', self.tr('给予'), icon=FluentIcon.COMMAND_PROMPT)
        self.RelicInterface = Relic('RelicInterface', self)
        InitUI.addSubInterface(self, self.RelicInterface, 'RelicInterface', self.tr('遗器'), icon=FluentIcon.COMMAND_PROMPT)

        InitUI.initPivotLayout(self, self.CommonInterface, False, True)

        self.AdminInterface.vBoxLayout.addSpacing(10)
        self.pagerLayout = QHBoxLayout()
        self.pagerLayout.addWidget(self.pager, alignment=Qt.AlignCenter)
        self.handleAdminPageChanged(0)
        self.AdminInterface.vBoxLayout.addLayout(self.pagerLayout)

        self.updateLayout = QHBoxLayout(self.updateContainer)
        self.updateLayout.addWidget(self.updateText, alignment=Qt.AlignCenter)
        self.updateLayout.addStretch(1)
        self.updateLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.saveButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.copyButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.actionButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.updateContainer)

    def __connectSignalToSlot(self):
        self.command_update.connect(self.handleCommandUpdate)
        self.clearButton.clicked.connect(lambda: self.updateText.clear())
        self.saveButton.clicked.connect(self.handleSaveClicked)
        self.copyButton.clicked.connect(lambda: self.handleCopyToClipboard('show'))
        self.actionButton.clicked.connect(self.handleActionClicked)

        # AdminInterface
        self.pager.currentIndexChanged.connect(lambda index: self.handleAdminPageChanged(index))
        self.statusCard.clicked.connect(lambda: self.command_update.emit('/status'))
        self.accountCard.create_account.connect(lambda: self.handleAccountClicked('create'))
        self.accountCard.delete_account.connect(lambda: self.handleAccountClicked('delete'))
        self.kickCard.kick_player.connect(self.handleKickClicked)

        # CommonInterface
        self.helpCard.clicked.connect(lambda: self.command_update.emit('/help'))
        self.refillCard.clicked.connect(lambda: self.command_update.emit('/refill'))
        self.energyCard.clicked.connect(lambda: self.command_update.emit('/energy'))
        self.healCard.clicked.connect(lambda: self.command_update.emit('/heal'))
        self.unstuckCard.unstuck_player.connect(self.handleUnstuckClicked)

        # WorldInterface
        self.unlockfpsCard.clicked.connect(lambda: self.command_update.emit('/unlockfps'))

        # DataInterface
        self.giveallCard.giveall_clicked.connect(lambda itemid: self.handleGiveallClicked(itemid))
        self.clearCard.clear_clicked.connect(lambda itemid: self.handleClearClicked(itemid))
        self.worldLevelCard.set_world_level.connect(lambda index: self.handleWorldLevelClicked(index))
        self.genderCard.gender_male.connect(lambda: self.command_update.emit('/gender male'))
        self.genderCard.gender_female.connect(lambda: self.command_update.emit('/gender female'))
        self.avatarCard.avatar_set.connect(lambda index: self.handleAvatarClicked(index))

        # Alone Interfaces
        self.SceneInterface.scene_id_signal.connect(lambda scene_id: self.command_update.emit('/scene ' + scene_id))
        self.GiveInterface.item_id_signal.connect(lambda item_id, index: self.handleGiveClicked(item_id, index))
        self.RelicInterface.relic_id_signal.connect(lambda relic_id: self.handleRelicClicked(relic_id))
        self.RelicInterface.custom_relic_signal.connect(lambda command: self.command_update.emit(command))

    def handleCommandUpdate(self, text):
        self.updateText.clear()
        self.updateText.setText(text)
        if cfg.get(cfg.autoCopy): self.handleCopyToClipboard('hide')

    def handleSaveClicked(self):
        text = self.updateText.text()
        current_widget = self.stackedWidget.currentWidget()
        if text != '' and current_widget != self.CustomInterface:
            formatted_text = f"自定义命令 : {text}\n"
            with open(cfg.MYCOMMAND, 'a', encoding='utf-8') as file:
                file.write(formatted_text)
            
            Info(self.parent, 'S', 1000, self.tr('保存成功!'))

            self.CustomInterface.handleMycommandLoad()

    def handleActionClicked(self):
        if not cfg.get(cfg.usePRemote):
            remote_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('远程执行未启用!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )
            remote_error_button = PrimaryPushButton(self.tr('前往开启'))
            remote_error_button.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(2))
            remote_error.addWidget(remote_error_button)
            remote_error.show()
            return

        return # TODO Temp disable remote
        if cfg.get(cfg.uid) != '' and cfg.get(cfg.pKey) != '' and self.updateText.text() != '':
            try:
                status, response = handleCommandSend(cfg.get(cfg.uid), cfg.get(cfg.pKey), self.updateText.text())
                if status == 'success':
                    display_time = 1000 if len(str(response)) < 30 else 3000 if len(str(response)) < 100 else 15000
                    Info(self.parent, 'S', display_time, self.tr('执行成功!'), str(response))
                else:
                    Info(self.parent, 'E', 3000, self.tr('执行失败!'), str(response))
            except Exception as e:
                Info(self.parent, 'E', 3000, self.tr('执行失败!'), str(e))
        else:
            Info(self.parent, 'E', 3000, self.tr('执行失败!'))

    def handleCopyToClipboard(self, status):
        text = self.updateText.text()
        app = QApplication.instance()
        if text != '':
            clipboard = app.clipboard()
            clipboard.setText(text)
            if status == 'show':
                Info(self.parent, 'S', 1000, self.tr('已复制到剪贴板!'))

    def handleAdminPageChanged(self, index):
        for cur_index in self.page_components:
            for card in self.page_components[cur_index]:
                if index != cur_index:
                    card.setVisible(False)
                else:
                    card.setVisible(True)

    # 命令处理
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

    def handleKickClicked(self):
        account_uid = self.kickCard.account_uid.text()
        if account_uid != '':
            self.command_update.emit('/kick @' + account_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))

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

    def handleGiveClicked(self, item_id, index):
        give_level_edit = self.GiveInterface.give_level_edit.text()
        give_eidolon_edit = self.GiveInterface.give_eidolon_edit.text()
        give_num_edit = self.GiveInterface.give_num_edit.text()
        command = '/give ' + item_id
        if index == 0:
            if give_level_edit != '':
                command += ' lv' + give_level_edit
            if give_eidolon_edit != '':
                command += ' r' + give_eidolon_edit
        elif index == 1:
            if give_num_edit != '':
                command += ' x' + give_num_edit
            if give_level_edit != '':
                command += ' lv' + give_level_edit
            if give_eidolon_edit != '':
                command += ' r' + give_eidolon_edit
        elif index == 2 or index == 3:
            if give_num_edit != '':
                command += ' x' + give_num_edit
        self.command_update.emit(command)

    def handleRelicClicked(self, relic_id):
        relic_level = self.RelicInterface.level_edit.text()
        main_entry_name = self.RelicInterface.main_now_edit.text()
        now_list_nozero = {k: v for k, v in self.RelicInterface.now_list.items() if v > 0}
        entry_table = self.RelicInterface.entry_table
        command = '/give ' + relic_id

        if relic_level != '':
            command += ' lv' + relic_level

        if main_entry_name != '':
            entry_index = 0
            for i in range(entry_table.rowCount()):
                if entry_table.item(i, 0).text() == main_entry_name and entry_table.item(i, 1).text() != self.tr(
                        '通用'):
                    entry_index = i
                    break
            main_entry = entry_table.item(entry_index, 2).text()
            command += ' s' + main_entry

        for entry_name, entry_num in now_list_nozero.items():
            if entry_name != '':
                entry_index = 0
                for i in range(entry_table.rowCount()):
                    if entry_table.item(i, 0).text() == entry_name and entry_table.item(i, 1).text() == self.tr('通用'):
                        entry_index = i
                        break
                side_entry = entry_table.item(entry_index, 2).text()
                command += ' ' + side_entry + ':' + str(entry_num)

        self.command_update.emit(command)
