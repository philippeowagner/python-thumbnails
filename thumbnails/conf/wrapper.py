# -*- coding: utf-8 -*-
import importlib
import json
import os

from thumbnails.compat import makedirs

from . import defaults


class SettingsWrapper(object):

    def __init__(self):
        self.defaults = {}
        self.settings_modules = []
        self._load_from_module(defaults, self.defaults)
        if os.environ.get('THUMBNAILS_SETTINGS_MODULE'):
            self.settings_modules.append(
                importlib.import_module(os.environ.get('THUMBNAILS_SETTINGS_MODULE'))
            )

        if os.environ.get('DJANGO_SETTINGS_MODULE'):
            try:
                from django.conf import settings as settings_django  # noqa skip:isort
                from . import defaults_django
                self.settings_modules.append(defaults_django)
                self.settings_modules.append(settings_django)
            except ImportError:
                pass

        if not os.path.exists(self.THUMBNAIL_PATH):
            makedirs(os.path.dirname(self.THUMBNAIL_PATH), exist_ok=True)
            makedirs(self.THUMBNAIL_PATH, exist_ok=True)

    def __getattr__(self, key):
        value = self.defaults.get(key, None)

        for settings_module in self.settings_modules:
            if getattr(settings_module, key, None):
                value = getattr(settings_module, key, None)

        if 'overridden_settings' in os.environ:
            settings = json.loads(os.environ['overridden_settings'])
            if key in settings:
                value = settings[key]

        if value is None:
            raise AttributeError('No setting for "{}".'.format(key))

        return value

    def _load_from_module(self, _module, target):
        for setting in dir(_module):
            if not setting.startswith('_'):
                target[setting] = getattr(_module, setting)
