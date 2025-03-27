from .Cmds import *
from src.util import *
from src.head import *
# from src.app.remote.common import handleCommandSend

class CommandManager(ScrollArea):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.updateText = LineEdit()
        self.updateText.setFixedSize(800, 35)

        self.uidText = LineEdit()
        self.uidText.setFixedSize(120, 35)
        self.uidText.setValidator(QIntValidator())
        self.uidText.setPlaceholderText(self.tr('UID'))

        self.copyButton = PrimaryToolButton(FluentIcon.COPY)
        self.clearButton = PrimaryToolButton(FluentIcon.DELETE)
        self.actionButton = PrimaryToolButton(FluentIcon.LINK)
        self.saveButton = PrimaryToolButton(FluentIcon.SAVE)
        self.copyButton.setFixedSize(35, 35)
        self.clearButton.setFixedSize(35, 35)
        self.actionButton.setFixedSize(35, 35)
        self.saveButton.setFixedSize(35, 35)

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

        InitUI.initPivotLayout(self, self.AdminInterface)

        self.updateLayout = QHBoxLayout()
        self.updateLayout.addWidget(self.updateText, alignment=Qt.AlignCenter)
        self.updateLayout.addStretch(1)
        self.updateLayout.addWidget(self.uidText, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.copyButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.actionButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.saveButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(15)
        self.vBoxLayout.addLayout(self.updateLayout)

    def __initInfo(self):
        self.uidText.setText(cfg.get(cfg.targetUid))

    def __connectSignalToSlot(self):
        self.uidText.textChanged.connect(lambda: cfg.set(cfg.targetUid, self.uidText.text()))
        self.clearButton.clicked.connect(lambda: self.updateText.clear())
        self.saveButton.clicked.connect(self.handleSaveClicked)
        self.copyButton.clicked.connect(lambda: self.handleCopyToClipboard('show'))
        self.actionButton.clicked.connect(self.handleActionClicked)

        self.AdminInterface.command_update.connect(self.handleCommandUpdate)
        self.CommonInterface.command_update.connect(self.handleCommandUpdate)
        self.DataInterface.command_update.connect(self.handleCommandUpdate)
        self.CustomInterface.command_update.connect(self.handleCommandUpdate)
        self.SceneInterface.command_update.connect(self.handleCommandUpdate)
        self.GiveInterface.command_update.connect(self.handleCommandUpdate)
        self.RelicInterface.command_update.connect(self.handleCommandUpdate)

    def handleCommandUpdate(self, text, hasUid = True):
        if hasUid: text += f" @{self.uidText.text()}"
        self.updateText.clear()
        self.updateText.setText(text)
        if cfg.get(cfg.autoCopy): self.handleCopyToClipboard('hide')

    def handleSaveClicked(self):
        text = self.updateText.text()
        current_widget = self.stackedWidget.currentWidget()
        if text != '' and current_widget != self.CustomInterface:
            formatted_text = f"{self.tr('未命名')} : {text}\n"
            with open(cfg.MYCOMMAND, 'a', encoding='utf-8') as f:
                f.write(formatted_text)

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
