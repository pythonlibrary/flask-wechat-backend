import os
import platform
import logging
from logging import StreamHandler, FileHandler

from logging.handlers import RotatingFileHandler

from flask.logging import default_handler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    @classmethod
    def start_hook(cls):
        pass

    @classmethod
    def init_app(cls, app):
        pass


class LocalmachineConfig(Config):
    DEBUG = True

    WEIWIN_TOKEN = 'foobar'

    CONFIG_DIR = '.'
    SITEMAP_URL = "http://pythonlibrary.net/post-sitemap.xml"

    @classmethod
    def init_app(cls, app):
        # logs to stderr
        app.logger.removeHandler(default_handler)
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        formatter = logging.Formatter('wechat: '
                                      '{'
                                      '"loggerName":"%(name)s", '
                                      '"asciTime":"%(asctime)s", '
                                      '"levelName":"%(levelname)s", '
                                      '"filename":"%(filename)s", '
                                      '"lineno":"%(lineno)d", '
                                      '"functionName":"%(funcName)s", '
                                      '"levelNo":"%(levelno)s", '
                                      '"lineNo":"%(lineno)d", '
                                      '"message":"%(message)s"'
                                      '}'
                                      )
        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        


class ProductionConfig(Config):
    DEBUG = False

    WEIWIN_TOKEN = 'foobar'

    CONFIG_DIR = '/usr/config'
    SITEMAP_URL = "http://wordpress/post-sitemap.xml"

    @classmethod
    def init_app(cls, app):
        app.logger.removeHandler(default_handler)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        # TODO - split log files if size is too big
        file_handler = RotatingFileHandler("/var/log/" + 'pythonlibrary_api_log.log', maxBytes=1024 * 1024 * 100, backupCount=10)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)


config = {
    'development': LocalmachineConfig,
    'production': DockerConfig,
    'default': LocalmachineConfig
}
