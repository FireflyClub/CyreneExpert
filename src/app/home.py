from src.head import *
from src.util import *


class CustomFlipItemDelegate(FlipImageDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        self.setBorderRadius(35)
        painter.save()
        rect = option.rect
        rect = QRect(rect.x(), rect.y(), rect.width(), rect.height())
        painter.setPen(Qt.white)
        painter.setFont(QFont(cfg.APP_FONT, 35))
        painter.drawText(rect.adjusted(0, -20, 0, 0), Qt.AlignCenter, cfg.APP_NAME)
        painter.setFont(QFont(cfg.APP_FONT, 20))
        painter.drawText(rect.adjusted(0, 90, 0, 0), Qt.AlignCenter, cfg.APP_VERSION)
        painter.restore()


class Home(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        self.parent = parent

        self.__initWidgets()

    def __initWidgets(self):
        self.flipView = HorizontalFlipView()

        self.image_files = glob.glob(os.path.join(cfg.IMAGE, 'bg_home_*.png'))
        self.flipView.addImages(self.image_files)
        self.flipView.setCurrentIndex(random.randint(0, len(self.image_files) - 1))

        self.flipView.setItemSize(QSize(1160, 350))
        self.flipView.setFixedSize(QSize(1160, 350))
        self.flipView.setItemDelegate(CustomFlipItemDelegate(self.flipView))

        self.name_labal = SubtitleLabel(self.tr('当前通道: ') + cfg.APP_NAME)
        self.version_label = SubtitleLabel(self.tr('当前版本: ') + cfg.APP_VERSION)
        self.game_path_label = SubtitleLabel(self.tr('游戏路径: ') + cfg.get(cfg.currentGamePath))
        self.fiddler_label = SubtitleLabel(self.tr('Fiddler路径: ') + cfg.get(cfg.fiddlerPath))
        self.name_labal.setFont(QFont(f'{cfg.APP_FONT}', 14))
        self.version_label.setFont(QFont(f'{cfg.APP_FONT}', 14))
        self.game_path_label.setFont(QFont(f'{cfg.APP_FONT}', 14))
        self.fiddler_label.setFont(QFont(f'{cfg.APP_FONT}', 14))
        
        self.button_launch = PrimaryPushButton(FluentIcon.PLAY_SOLID, self.tr(' 一键启动'))
        self.button_launch.setFixedSize(200, 65)
        self.button_launch.setIconSize(QSize(20, 20))
        self.button_launch.setFont(QFont(f'{cfg.APP_FONT}', 18))
        setCustomStyleSheet(self.button_launch, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')
        
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.flipView)
        self.image_layout.setAlignment(Qt.AlignHCenter)

        self.info_layout = QVBoxLayout()
        self.info_layout.addWidget(self.name_labal)
        self.info_layout.addWidget(self.version_label)
        self.info_layout.addWidget(self.game_path_label)
        self.info_layout.addWidget(self.fiddler_label)
        self.info_layout.addSpacing(80)

        self.launch_button_layout = QVBoxLayout()
        self.launch_button_layout.addWidget(self.button_launch, alignment=Qt.AlignBottom)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addLayout(self.info_layout)
        self.bottom_layout.addStretch(1)
        self.bottom_layout.addLayout(self.launch_button_layout)
        self.bottom_layout.setContentsMargins(25, 0, 25, 0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 30, 10, 10)
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.addSpacing(25)

    def __connectSignalToSlot(self):
        self.scrollTimer = QTimer(self)
        self.scrollTimer.timeout.connect(
            lambda: self.flipView.setCurrentIndex(random.randint(0, len(self.image_files) - 1)))
        self.scrollTimer.start(5000)
        self.button_launch.clicked.connect(self.handleGameLaunch)

    def handleGameLaunch(self):
        game_path = cfg.get(cfg.currentGamePath)
        fiddler_path = cfg.get(cfg.fiddlerPath)

        if not os.path.exists(game_path):
            server_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('游戏程序不存在!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            server_error_button = PrimaryPushButton(self.tr('前往修改'))
            server_error_button.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(1))
            server_error.addWidget(server_error_button)
            server_error.show()
            return
        if not os.path.exists(fiddler_path):
            server_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('Fiddler不存在!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            server_error_button = PrimaryPushButton(self.tr('前往修改'))
            server_error_button.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(3))
            server_error.addWidget(server_error_button)
            server_error.show()
            return

        open_file(self, game_path)
        open_file(self, fiddler_path)
