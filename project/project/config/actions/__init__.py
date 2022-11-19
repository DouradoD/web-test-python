from ..constants import Platform
from .mobile.android.android_actions import AndroidActions
from .web.web_actions import WebActions

ACTIONS_MAP = {
    Platform.ANDROID: AndroidActions,
    # Platform.IOS: IOSActions,
    Platform.WEB: WebActions
}


def load_actions(platform, driver):
    return ACTIONS_MAP[platform](driver=driver)
