from . import *
from app.importer import *
from app.module import *


class Main(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.handleFontCheck()

        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(cfg.APP_NAME)
        self.setFixedSize(1280, 768)
        self.setWindowIcon(QIcon(cfg.ICON))
        self.handleCenterWindow()

        setTheme(cfg.get(cfg.themeMode))
        setThemeColor(cfg.get(cfg.themeColor))

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(200, 200))
        self.splashScreen.raise_()
        self.show()
        QApplication.processEvents()
        self.__initNavigation()
        self.splashScreen.finish()
        self.__initInfo()

    def __initNavigation(self):
        self.homeInterface = Home('HomeInterface', self)
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, self.tr('主页'), FluentIcon.HOME_FILL)
        self.launcherInterface = Launcher('LauncherInterface', self)
        self.addSubInterface(self.launcherInterface, FluentIcon.PLAY, self.tr('启动器'), FluentIcon.PLAY)
        self.lunarcoreInterface = LunarCore('LunarCoreInterface', self)
        self.addSubInterface(self.lunarcoreInterface, FluentIcon.CAFE, 'LunarCore', FluentIcon.CAFE)
        self.proxyInterface = Proxy('ProxyInterface', self)
        self.addSubInterface(self.proxyInterface, FluentIcon.CERTIFICATE, self.tr('代理'), FluentIcon.CERTIFICATE)

        self.navigationInterface.addItem(
            routeKey='theme',
            icon=FluentIcon.CONSTRACT,
            text=self.tr('主题'),
            onClick=self.handleThemeChanged,
            selectable=False,
            position=NavigationItemPosition.BOTTOM
        )

        self.settingInterface = Setting('SettingInterface', self)
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, self.tr('设置'), FluentIcon.SETTING,
                             NavigationItemPosition.BOTTOM)

    def __initInfo(self):
        if cfg.LOGIN_STATUS:
            self.count_pwd = 0
            self.login_card = MessageLogin(self)
            self.login_card.show()
            self.login_card.passwordEntered.connect(self.handleLogin)

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
                        if cfg.APP_FONT.lower() in name.lower():
                            isSetupFont = True
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(reg_key)
        except Exception as e:
            Info(self, 'E', 3000, self.tr('检查字体失败: '), str(e))

        if not isSetupFont:
            subprocess.run(f'cd {cfg.ROOT}/src/patch/font && start zh-cn.ttf', shell=True)
            sys.exit()

    def __InitErrorInfos(self, hwid):
        self.count_pwd += 1

        if hasattr(self, 'login_error_info'):
            self.login_error_info.close()
        self.login_error_info = InfoBar(
            icon=InfoBarIcon.ERROR,
            title=self.tr('密码错误!'),
            content=self.tr('次数: ') + str(self.count_pwd),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )

        if hasattr(self, 'hwid_error'):
            self.hwid_error.close()
        self.hwid_error = InfoBar(
            icon=InfoBarIcon.WARNING,
            title=hwid,
            content='',
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        hwid_error_button = PrimaryPushButton(self.tr('复制'))
        hwid_error_button.clicked.connect(lambda: QApplication.clipboard().setText(hwid))
        self.hwid_error.addWidget(hwid_error_button)

        self.hwid_error.show()
        self.login_error_info.show()
    
    def __HandleLoginPWD(self, hwid):
        sha256_hash = hashlib.sha256((hwid + "Lethe").encode()).hexdigest()
        md5_hash = hashlib.md5((sha256_hash + "Lethe").encode()).hexdigest()
        return md5_hash[0:8].upper()

    def handleLogin(self, pwd):
        result = subprocess.check_output('wmic csproduct get uuid', shell=True)
        hwid = result.decode().strip().split('\n')[1].strip()

        if self.__HandleLoginPWD(hwid) == pwd or cfg.LOGIN_PWD == pwd:
            Info(self, 'S', 1000, self.tr('登录成功!'))
            self.login_card.close()
            self.login_error_info.close()
            self.hwid_error.close()
        else:
            self.__InitErrorInfos(hwid)

    def handleThemeChanged(self):
        new_theme = Theme.LIGHT if cfg.get(cfg.themeMode) == Theme.DARK else Theme.DARK
        setTheme(new_theme)
        cfg.set(cfg.themeMode, new_theme)
        cfg.save() # Bug
