from . import *
from Src.Import import *
from Src.Util import *


class Main(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.handleFontCheck()

        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(CFG.APP_NAME)
        self.setFixedSize(1280, 768)
        self.setWindowIcon(QIcon(CFG.ICON))
        self.handleCenterWindow()

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(200, 200))
        self.splashScreen.raise_()
        self.show()
        QApplication.processEvents()
        self.__initNavigation()
        self.splashScreen.finish()

    def __initNavigation(self):
        self.homeInterface = Home('HomeInterface', self)
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, self.tr('主页'), FluentIcon.HOME_FILL)
        self.commandInterface = CommandManager('CommandManager', self)
        self.addSubInterface(self.commandInterface, FluentIcon.CAFE, self.tr('命令'), FluentIcon.CAFE)

        self.navigationInterface.addItem(
            routeKey='theme',
            icon=FluentIcon.CONSTRACT,
            text=self.tr('主题'),
            onClick=lambda: toggleTheme(True, True),
            selectable=False,
            position=NavigationItemPosition.BOTTOM
        )

        self.settingInterface = Setting('SettingInterface', self)
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, self.tr('设置'), FluentIcon.SETTING,
                             NavigationItemPosition.BOTTOM)

    def handleCenterWindow(self):
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def handleFontCheck(self):
        isSetupFont = False
        registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts")
        ]
        try:
            for hkey, sub_key in registry_keys:
                reg = winreg.ConnectRegistry(None, hkey)
                reg_key = winreg.OpenKey(reg, sub_key)
                i = 0
                while True:
                    try:
                        name, data, types = winreg.EnumValue(reg_key, i)
                        if CFG.APP_FONT.lower() in name.lower():
                            isSetupFont = True
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(reg_key)
        except Exception as e:
            Info(self, 'E', 3000, self.tr('检查字体失败: '), str(e))

        if not isSetupFont:
            subprocess.run(f'cd {CFG.ROOT}/data/font && start zh-cn.ttf', shell=True)
            sys.exit()
