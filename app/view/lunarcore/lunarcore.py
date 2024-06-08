from . import *
from app.importer import *
from app.module import *


class HyperlinkCard_LunarCore(SettingCard):
    def __init__(self, title, content=None, icon=FluentIcon.LINK):
        super().__init__(icon, title, content)
        self.linkButton_repo = HyperlinkButton('https://github.com/Melledy/LunarCore', 'LunarCore', self)
        self.linkButton_res1 = HyperlinkButton('https://github.com/Dimbreath/StarRailData', 'StarRailData', self)
        self.linkButton_res2 = HyperlinkButton('https://gitlab.com/Melledy/LunarCore-Configs', 'LunarCore-Configs',
                                               self)
        self.hBoxLayout.addWidget(self.linkButton_repo, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res2, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class LunarCore(ScrollArea):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.LunarCoreRepoCard = HyperlinkCard_LunarCore(
            self.tr('项目仓库'),
            self.tr('打开LunarCore相关仓库')
        )
        self.autoCopyCard = SwitchSettingCard(
            FluentIcon.COPY,
            self.tr('命令自动复制'),
            self.tr('选择命令时，自动复制命令到剪贴板'),
            configItem=cfg.autoCopy
        )
        self.CommandConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('自定义命令设置'),
            self.tr('手动配置自定义命令')
        )
        self.RelicDataConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('遗器命令设置'),
            self.tr('自定义遗器命令配置')
        )

    def __initLayout(self):
        self.ConfigInterface.addSettingCard(self.LunarCoreRepoCard)
        self.ConfigInterface.addSettingCard(self.autoCopyCard)
        self.ConfigInterface.addSettingCard(self.CommandConfigCard)
        self.ConfigInterface.addSettingCard(self.RelicDataConfigCard)

        InitUI.addSubInterface(self, self.ConfigInterface, 'ConfigInterface', self.tr('配置'), icon=FluentIcon.EDIT)
        self.RemteInterface = Remote('RemteInterface', self)
        InitUI.addSubInterface(self, self.RemteInterface, 'RemteInterface', self.tr('远程'), icon=FluentIcon.CONNECT)
        self.CommandInterface = Command('CommandInterface', self)
        InitUI.addSubInterface(self, self.CommandInterface, 'CommandInterface', self.tr('命令'), icon=FluentIcon.COMMAND_PROMPT)

        InitUI.initPivotLayout(self, self.ConfigInterface)

    def __connectSignalToSlot(self):
        self.autoCopyCard.checkedChanged.connect(self.handleAutoCopyChanged)
        self.CommandConfigCard.clicked.connect(lambda: open_file(self, cfg.MYCOMMAND))
        self.RelicDataConfigCard.clicked.connect(
            lambda: open_file(self, f'{cfg.ROOT}/src/data/{cfg.get(cfg.language).value.name()}/myrelic.txt'))

    def handleAutoCopyChanged(self):
        if cfg.get(cfg.autoCopy):
            Info(self, 'S', 1000, self.tr('自动复制已开启!'))
        else:
            Info(self, 'S', 1000, self.tr('自动复制已关闭!'))
