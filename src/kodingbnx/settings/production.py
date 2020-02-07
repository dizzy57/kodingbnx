from .base import *

ALLOWED_HOSTS = ["kodingbnx.pythonanywhere.com"]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DATABASES["default"]["OPTIONS"]["sql_mode"] = "STRICT_TRANS_TABLES"

STATIC_ROOT = "/home/kodingbnx/static"

SESSION_COOKIE_AGE = 365 * 24 * 60 * 60  # 365 days in seconds
