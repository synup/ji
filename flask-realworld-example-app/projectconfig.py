# -*- coding: utf-8 -*-
"""Application configuration."""
from datetime import timedelta
import os
import json
from consul_pyconfig import config as pyconfig

conf = pyconfig.Config(
    component='example-app'
)

class Config(object):
    """Base configuration."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # This directory
    APP_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'conduit'))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_HEADER_PREFIX = 'Token'
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]
    JWT_HEADER_TYPE = 'Token'
    BCRYPT_LOG_ROUNDS = conf.get('bcrypt_log_rounds') or 13
    SECRET_KEY = conf.get('conduit_secret') or 'secret-key'
    ENV = conf.get('env') or 'dev'
    DEBUG = bool(conf.get('debug')) or False
    SQLALCHEMY_DATABASE_URI = conf.get('db_uri') or 'sqlite:///{0}'.format(os.path.join(PROJECT_ROOT, 'dev.db'))
