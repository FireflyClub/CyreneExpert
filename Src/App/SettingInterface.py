from Src.Import import *
from Src.Util import *


class Setting(ScrollArea):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        # InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.PersonalInterface = SettingCardGroup()
        self.themeColorCard = CustomColorSettingCard(
            CFG.themeColor,
            FluentIcon.PALETTE,
            self.tr('主题色'),
            self.tr('修改组件主题颜色')
        )
        self.zoomCard = ComboBoxSettingCard(
            CFG.dpiScale,
            FluentIcon.ZOOM,
            "DPI",
            self.tr("调整全局缩放"),
            texts=["100%", "125%", "150%", "175%", "200%", self.tr("跟随系统设置")]
        )
        self.languageCard = ComboBoxSettingCard(
            CFG.language,
            FluentIcon.LANGUAGE,
            self.tr('语言'),
            self.tr('界面显示语言'),
            texts=['简体中文', '繁體中文', 'English', self.tr('跟随系统设置')]
        )
        self.autoCopyCard = SwitchSettingCard(
            FluentIcon.COPY,
            self.tr('命令自动复制'),
            self.tr('选择命令时，自动复制命令到剪贴板'),
            configItem=CFG.autoCopy
        )
        self.restartCard = PrimaryPushSettingCard(
            self.tr('重启程序'),
            FluentIcon.ROTATE,
            self.tr('重启程序'),
            self.tr('无奖竞猜，存在即合理')
        )

    def __initLayout(self):
        self.PersonalInterface.addSettingCard(self.themeColorCard)
        self.PersonalInterface.addSettingCard(self.zoomCard)
        self.PersonalInterface.addSettingCard(self.languageCard)
        self.PersonalInterface.addSettingCard(self.autoCopyCard)
        self.PersonalInterface.addSettingCard(self.restartCard)

        # InitUI.addSubInterface(self, self.PersonalInterface, 'PersonalInterface', self.tr('程序'), icon=FluentIcon.SETTING)
        self.AboutInterface = About('AboutInterface', self)
        # InitUI.addSubInterface(self, self.AboutInterface, 'AboutInterface', self.tr('关于'), icon=FluentIcon.INFO)

        # InitUI.initPivotLayout(self, self.PersonalInterface)

    def __connectSignalToSlot(self):
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c, lazy=True))
        self.zoomCard.comboBox.currentIndexChanged.connect(self.restart_application)
        self.languageCard.comboBox.currentIndexChanged.connect(self.restart_application)
        self.autoCopyCard.checkedChanged.connect(self.handleAutoCopyChanged)
        self.restartCard.clicked.connect(self.restart_application)

    def handleAutoCopyChanged(self):
        if CFG.get(CFG.autoCopy):
            Info(self, 'S', 1000, self.tr('自动复制已开启!'))
        else:
            Info(self, 'S', 1000, self.tr('自动复制已关闭!'))

    def restart_application(self):
        current_process = QProcess()
        current_process.startDetached(sys.executable, sys.argv)
        sys.exit()


class About_Background(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(os.path.join(CFG.IMAGE, 'bg_about.png'))
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)

        painter.setPen(Qt.white)
        painter.setFont(QFont(CFG.APP_FONT, 45))
        painter.drawText(self.rect().adjusted(0, -30, 0, 0), Qt.AlignHCenter | Qt.AlignVCenter, CFG.APP_NAME)
        painter.setFont(QFont(CFG.APP_FONT, 30))
        painter.drawText(self.rect().adjusted(0, 120, 0, 0), Qt.AlignHCenter | Qt.AlignVCenter, CFG.APP_VERSION)


class About(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.about_image = About_Background()
        self.about_image.setFixedSize(1100, 500)

        self.link_writer = PushButton(FluentIcon.HOME, self.tr('   作者主页'))
        self.link_repo = PushButton(FluentIcon.GITHUB, self.tr('   项目仓库'))
        self.link_releases = PushButton(FluentIcon.MESSAGE, self.tr('   版本发布'))
        self.link_issues = PushButton(FluentIcon.HELP, self.tr('   反馈交流'))

        for link_button in [self.link_writer, self.link_repo, self.link_releases, self.link_issues]:
            link_button.setFixedSize(260, 70)
            link_button.setIconSize(QSize(16, 16))
            link_button.setFont(QFont(f'{CFG.APP_FONT}', 12))
            setCustomStyleSheet(link_button, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.about_image, alignment=Qt.AlignHCenter)

        self.info_button_layout = QHBoxLayout()
        self.info_button_layout.addWidget(self.link_writer)
        self.info_button_layout.addWidget(self.link_repo)
        self.info_button_layout.addWidget(self.link_releases)
        self.info_button_layout.addWidget(self.link_issues)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.info_button_layout)
        self.setLayout(self.main_layout)

    def __connectSignalToSlot(self):
        self.link_writer.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(CFG.URL_WRITER)))
        self.link_repo.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(CFG.URL_REPO)))
        self.link_releases.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(CFG.URL_RELEASES)))
        self.link_issues.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(CFG.URL_ISSUES)))
