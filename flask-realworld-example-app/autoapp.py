# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from conduit.app import create_app
from projectconfig import Config
# from conduit.settings import DevConfig, ProdConfig

CONFIG = Config

app = create_app(CONFIG)
