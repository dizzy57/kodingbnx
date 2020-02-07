from .base import *

DEBUG = True

THIRD_PARTY_APPS += [
    "debug_toolbar",
    "django_extensions",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE


def show_django_debug_toolbar_in_debug_mode(request):
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "kodingbnx.settings.development.show_django_debug_toolbar_in_debug_mode",
}
