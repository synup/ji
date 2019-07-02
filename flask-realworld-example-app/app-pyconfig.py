# -*- coding: utf-8 -*-
"""Create an application instance."""

from conduit.app import create_app
from projectconfig import Config

CONFIG = Config

app = create_app(CONFIG)
