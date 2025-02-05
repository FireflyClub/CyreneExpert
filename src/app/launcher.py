from src.head import *
from src.util import *


class PrimaryPushSettingCard_StartGame(SettingCard):
    combobox_changed = Signal(str)
    clicked_start = Signal(str)

    def __init__(self, title, content=None, icon=FluentIcon.GAME):
        super().__init__(icon, title, content)
        self.button_start = PrimaryPushButton(self.tr('启动游戏'), self)
        self.select_combobox = ComboBox()
        self.refreshComboBox(cfg.get(cfg.gamePathList))

        self.hBoxLayout.addWidget(self.select_combobox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_start, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.button_start.clicked.connect(lambda: self.clicked_start.emit(self.select_combobox.currentText()))
        self.select_combobox.currentIndexChanged.connect(self.handleComboBoxChanged)

    def refreshComboBox(self, lists):
        self.select_combobox.clear()
        self.select_combobox.addItems(lists)
        self.select_combobox.setCurrentText(cfg.get(cfg.currentGamePath))
    
    def handleComboBoxChanged(self, index):
        self.gamePath = self.select_combobox.itemText(index)
        cfg.set(cfg.currentGamePath, self.gamePath)
        self.combobox_changed.emit(self.gamePath)


class Launcher(ScrollArea):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.LauncherInterface = SettingCardGroup(self.scrollWidget)
        self.startGameCard = PrimaryPushSettingCard_StartGame(
            self.tr('启动游戏'),
            self.tr('选取游戏版本并启动游戏')
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.LauncherRepoCard = HyperlinkCard(
            'https://github.com/letheriver2007/Firefly-Launcher',
            'Firefly-Launcher',
            FluentIcon.LINK,
            self.tr('项目仓库'),
            self.tr('打开Firefly-Launcher项目仓库')
        )
        self.gameListCard = ListSettingCard(
            FluentIcon.GAME,
            cfg.gamePathList,
            self.tr('选择游戏路径'),
            self.tr('支持多游戏版本')
        )
        self.settingConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('启动器设置'),
            self.tr('自定义启动器配置')
        )

    def __initLayout(self):
        self.LauncherInterface.addSettingCard(self.startGameCard)
        self.ConfigInterface.addSettingCard(self.LauncherRepoCard)
        self.ConfigInterface.addSettingCard(self.settingConfigCard)
        self.ConfigInterface.addSettingCard(self.gameListCard)

        InitUI.addSubInterface(self, self.LauncherInterface, "LauncherInterface", self.tr('启动'), icon=FluentIcon.PLAY)
        InitUI.addSubInterface(self, self.ConfigInterface, "ConfigInterface", self.tr('配置'), icon=FluentIcon.EDIT)

        InitUI.initPivotLayout(self, self.LauncherInterface)

    def __connectSignalToSlot(self):
        self.startGameCard.clicked_start.connect(lambda path: open_file(self, path))
        self.settingConfigCard.clicked.connect(lambda: open_file(self, cfg.CONFIG))
        self.gameListCard.listChanged.connect(self.startGameCard.refreshComboBox)
        self.startGameCard.combobox_changed.connect(
            lambda path: self.parent.homeInterface.game_path_label.setText(self.tr('游戏路径: ') + path))
