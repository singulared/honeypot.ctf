# -*- coding: utf-8 -*-

import importlib
import os


default = 'config.default2.config'


def load(config_name=default):
    config = importlib.import_module(config_name)
    config.db = os.path.sep.join(config_name.split('.')[:-1] + ['db.sqlite'])
    return config
