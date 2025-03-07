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
        self.AdminInterface = Admin(self.scrollWidget)
        InitUI.addSubInterface(self, self.AdminInterface, 'AdminInterface', self.tr('管理'), icon=FluentIcon.COMMAND_PROMPT)

        self.CommonInterface = Common(self.scrollWidget)
        InitUI.addSubInterface(self, self.CommonInterface, 'CommonInterface', self.tr('常用'), icon=FluentIcon.COMMAND_PROMPT)

        self.DataInterface = Data(self.scrollWidget)
        InitUI.addSubInterface(self, self.DataInterface, 'DataInterface', self.tr('数据'), icon=FluentIcon.COMMAND_PROMPT)

        self.CustomInterface = Custom('CustomInterface', self)
        InitUI.addSubInterface(self, self.CustomInterface, 'CustomInterface', self.tr('自定义'), icon=FluentIcon.COMMAND_PROMPT)

        self.SceneInterface = Scene('SceneInterface', self)
        InitUI.addSubInterface(self, self.SceneInterface, 'SceneInterface', self.tr('场景'), icon=FluentIcon.COMMAND_PROMPT)

        self.GiveInterface = Give('GiveInterface', self)
        InitUI.addSubInterface(self, self.GiveInterface, 'GiveInterface', self.tr('给予'), icon=FluentIcon.COMMAND_PROMPT)

        self.RelicInterface = Relic('RelicInterface', self)
        InitUI.addSubInterface(self, self.RelicInterface, 'RelicInterface', self.tr('遗器'), icon=FluentIcon.COMMAND_PROMPT)

        InitUI.initPivotLayout(self, self.AdminInterface, False, True)

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

        self.AdminInterface.command_update.connect(self.handleCommandUpdate)
        self.CommonInterface.command_update.connect(self.handleCommandUpdate)
        self.DataInterface.command_update.connect(self.handleCommandUpdate)
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
        return # TODO Temp disable remote
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

    # 命令处理
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
