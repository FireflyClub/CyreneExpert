from app.importer import *
from app.module import *


class PrimaryPushSettingCard_Fiddler(SettingCard):
    clicked_script = Signal()
    clicked_old = Signal()
    clicked_backup = Signal()

    def __init__(self, title, content=None, icon=FluentIcon.VPN):
        super().__init__(icon, title, content)
        self.button_script = PrimaryPushButton(self.tr('脚本打开'), self)
        self.button_old = PrimaryPushButton(self.tr('原版打开'), self)
        self.button_backup = PrimaryPushButton(self.tr('备份'), self)
        self.hBoxLayout.addWidget(self.button_script, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_old, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_backup, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_script.clicked.connect(self.clicked_script)
        self.button_old.clicked.connect(self.clicked_old)
        self.button_backup.clicked.connect(self.clicked_backup)


class CustomFlyoutView_Fiddler(FlyoutViewBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.lc_button = PrimaryPushButton('LunarCore')
        self.lc_ssl_button = PrimaryPushButton('LunarCore(SSL)')
        self.lc_button.setFixedWidth(120)
        self.lc_ssl_button.setFixedWidth(120)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.hBoxLayout.addWidget(self.lc_button)
        self.hBoxLayout.addWidget(self.lc_ssl_button)

        self.lc_button.clicked.connect(lambda: self.handleFiddlerButton('lc'))
        self.lc_ssl_button.clicked.connect(lambda: self.handleFiddlerButton('lc_ssl'))

    def handleFiddlerButton(self, mode):
        status = open_file(self, cfg.get(cfg.fiddlerPath))
        if status:
            if mode == 'lc':
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                               'copy /y "src\\patch\\fiddler\\CustomRules-LC.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                               shell=True)
            elif mode == 'lc_ssl':
                subprocess.run('del /f "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" && '
                               'copy /y "src\\patch\\fiddler\\CustomRules-LCSSL.js" "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js"',
                               shell=True)


class Proxy(ScrollArea):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.ProxyInterface = SettingCardGroup(self.scrollWidget)
        self.FiddlerCard = PrimaryPushSettingCard_Fiddler(
            'Fiddler',
            self.tr('使用Fiddler Scripts代理')
        )
        self.noproxyCard = PrimaryPushSettingCard(
            self.tr('重置'),
            FluentIcon.POWER_BUTTON,
            self.tr('重置代理'),
            self.tr('重置部分服务端未关闭的代理')
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.ProxyRepoCard = HyperlinkCard(
            'https://www.telerik.com/fiddler#fiddler-classic',
            'Fiddler',
            FluentIcon.LINK,
            self.tr('项目仓库'),
            self.tr('打开代理工具仓库')
        )
        self.fiddlerPathCard = PrimaryPushSettingCard(
            self.tr('修改'),
            FluentIcon.TILES,
            self.tr("选取Fiddler"),
            self.tr("支持选择Fiddler程序目录")
        )

    def __initLayout(self):
        self.ProxyInterface.addSettingCard(self.FiddlerCard)
        self.ProxyInterface.addSettingCard(self.noproxyCard)
        self.ConfigInterface.addSettingCard(self.ProxyRepoCard)
        self.ConfigInterface.addSettingCard(self.fiddlerPathCard)

        InitUI.addSubInterface(self, self.ProxyInterface, "ProxyInterface", self.tr('启动'), icon=FluentIcon.PLAY)
        InitUI.addSubInterface(self, self.ConfigInterface, "ConfigInterface", self.tr('配置'), icon=FluentIcon.EDIT)

        InitUI.initPivotLayout(self, self.ProxyInterface)

    def __connectSignalToSlot(self):
        self.fiddlerPathCard.clicked.connect(self.handlefiddlerPathSelect)
        self.FiddlerCard.clicked_script.connect(self.handleFiddlerTip)
        self.FiddlerCard.clicked_old.connect(lambda: open_file(self, cfg.get(cfg.fiddlerPath)))
        self.FiddlerCard.clicked_backup.connect(self.handleFiddlerBackup)
        self.noproxyCard.clicked.connect(self.handleProxyDisabled)

    def handlefiddlerPathSelect(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("选择Fiddler目录"), "./", "Executable Files (*.exe)")
        if not file_path or cfg.get(cfg.fiddlerPath) == file_path:
            return
        cfg.set(cfg.fiddlerPath, file_path)
        self.fiddlerPathCard.setContent(file_path)
        self.parent.homeInterface.fiddler_label.setText(self.tr("Fiddler路径: ") + file_path)

    def handleFiddlerTip(self):
        PopupTeachingTip.make(
            target=self.FiddlerCard.button_script,
            view=CustomFlyoutView_Fiddler(parent=self),
            tailPosition=TeachingTipTailPosition.RIGHT,
            duration=-1,
            parent=self
        )

    def handleFiddlerBackup(self):
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        subprocess.run(
            f'copy /y "%userprofile%\\Documents\\Fiddler2\\Scripts\\CustomRules.js" "CustomRules_{now_time}.js"',
            shell=True)
        Info(self, "S", 1000, self.tr("备份成功!"))

    def handleProxyDisabled(self):
        try:
            subprocess.run(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f',
                shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f',
                shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            Info(self, 'S', 1000, self.tr("全局代理已更改！"))
        except Exception as e:
            Info(self, 'E', 3000, self.tr("全局代理关闭失败！"), str(e))
