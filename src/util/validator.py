from src.head import *


class StringValidator(ConfigValidator):
    def validate(self, value):
        return value.strip() != ''

    def correct(self, value):
        if not value.strip():
            return ""
        return value
