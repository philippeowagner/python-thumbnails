# -*- coding: utf-8 -*-
import os
from thumbnails.conf import settings


class Thumbnail(object):

    size = None, None

    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return os.path.join(settings.THUMBNAIL_PATH, self.name)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def ratio(self):
        return float(self.width) / float(self.height)

    @property
    def is_portrait(self):
        return self.ratio < 1

    @property
    def is_landscape(self):
        return self.ratio > 1

    def exists(self):
        return NotImplemented
