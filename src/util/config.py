from src.head import *
from .validator import ExeValidator, ExeListValidator, StringValidator


def Info(self, types, time, title, content=''):
    if types == "S":
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=time,
            parent=self
        )
    elif types == "E":
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=time,
            parent=self
        )
    elif types == "W":
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=time,
            parent=self
        )

def open_file(self, file_path):
    if os.path.exists(file_path):
        os.startfile(file_path)
        Info(self, "S", 1000, self.tr("文件已打开!"))
        return True
    else:
        Info(self, "E", 3000, self.tr("找不到文件!"))
        return False

def get_version_type(version):
    if not os.path.exists('firefly-launcher.py'):
        return f'{version} REL'
    else:
        return f'{version} DEV'


class Language(Enum):
    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.Taiwan)
    ENGLISH = QLocale(QLocale.English)


class LanguageSerializer(ConfigSerializer):
    def serialize(self, language):
        return language.value.name()

    def deserialize(self, value: str):
        return Language(QLocale(value))


class Config(QConfig):
    ############### CONFIG ITEMS ###############
    dpiScale = OptionsConfigItem(
        "Style", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "Style", "Language", Language.ENGLISH, OptionsValidator(Language), LanguageSerializer(), restart=True)

    currentGamePath = ConfigItem("Config", "CurrentGamePath", "", StringValidator())
    gamePathList = ConfigItem("Config", "GamePathList", [], ExeListValidator())
    fiddlerPath = ConfigItem("Config", "FiddlerPath", "", ExeValidator())
    autoCopy = ConfigItem("Config", "AutoCopy", True, BoolValidator())

    # usePRemote = ConfigItem("Remote", "usePRemote", False, BoolValidator())
    # useCRemote = ConfigItem("Remote", "useCRemote", False, BoolValidator())
    # uid = ConfigItem("Remote", "Uid", "10001", StringValidator())
    # pKey = ConfigItem("Remote", "PKey", "", StringValidator())
    # serverUrl = ConfigItem("Remote", "ServerUrl", "127.0.0.1:619", StringValidator())
    # cKey = ConfigItem("Remote", "CKey", "lethe", StringValidator())

    ############### APP INFO ###############
    ROOT = os.getcwd()
    IMAGE = os.path.join(ROOT, 'data/image')
    ICON = os.path.join(ROOT, 'data/image/icon.ico')
    MYCOMMAND = os.path.join(ROOT, 'data/cmd/mycommand.txt')
    DEFAULT_MYCOMMAND = os.path.join(ROOT, 'data/cmd/mycommand-default.txt')

    APP_NAME = "Firefly Launcher (Lethe)"
    APP_VERSION = get_version_type("v2.0.0")
    APP_FONT = "SDK_SC_Web"

    ############### REMOTE INFO ###############
    # ROUTE_PAPPLY = "/api/papply"
    # ROUTE_PVERIFY = "/api/pverify"
    # ROUTE_PREMOTE = "/api/premote"
    # ROUTE_CREMOTE = "/api/cremote"

    ############### LINK CONFIG ###############
    URL_LATEST = "https://github.com/letheriver2007/Firefly-Launcher/releases/latest"
    URL_WRITER = "https://github.com/letheriver2007"
    URL_REPO = "https://github.com/letheriver2007/Firefly-Launcher"
    URL_RELEASES = "https://github.com/letheriver2007/Firefly-Launcher/releases"
    URL_ISSUES = "https://github.com/letheriver2007/Firefly-Launcher/issues"


cfg = Config()
cfg.themeColor.defaultValue = QColor("#FFC0CB")
cfg.set(cfg.themeColor, QColor("#FFC0CB"))
qconfig.load(f'{cfg.ROOT}/Config.json', cfg)
