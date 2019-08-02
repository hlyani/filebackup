import sys
import os
import logging
import eventlet
from logging.handlers import RotatingFileHandler
from oslo_config import cfg as oslo_cfg
from flask import Flask
from flask_cors import CORS
from eventlet import wsgi
from .util import log
from .util.log import IgnoreFilter
from .util import config as cfg
from .globalvar import GlobalVar

CONF = cfg.CONF
FILE_FORMAT = (
    "[%(asctime)s.%(msecs)03d][%(pathname)s:%(funcName)s]" "[%(levelname)s] %(message)s"
)
LOG = logging.getLogger(__name__)


def log_init(app):
    root = logging.getLogger()
    level = CONF.get("default", "log_level")
    root.setLevel(level)

    log_file = CONF.get("default", "logfile")
    log_max_size = CONF.getint("default", "logfile_size") * 1024 * 1024
    log_backup_count = CONF.getint("default", "logfile_backup_count")
    fh = RotatingFileHandler(
        log_file, maxBytes=log_max_size, backupCount=log_backup_count
    )
    fh.setFormatter(logging.Formatter(fmt=FILE_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    root.addHandler(fh)

    # FIXME: how to remove default?
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)


# def configure_app(app, config, simple_context=False):
def configure_app(app, config, simple_context=False):
    # 1. 设置读取配置文件
    CONFIG_FILE = os.getenv("YANI_CONFIG_FILE") or "/etc/filebackup/yani.conf"
    cfg.config_init(CONFIG_FILE)
    # 初始化 olso config
    if os.path.exists(CONFIG_FILE):
        oslo_cfg.CONF(default_config_files=[CONFIG_FILE])

    # 2. 配置日志
    log_init(app)

    # # 3, 配置app
    # app.config["SECRET_KEY"] = CONF.get("default", "secret")
    print(CONF.get("default", "key_secret"))


def create_app(config=None, simple_context=False):
    app = Flask("yani")

    configure_app(app, config, simple_context)
    register_blueprints(app)
    if not simple_context:
        CORS(app)
    return app


def register_blueprints(app):
    from .blueprints.test.views import bp as test_bp

    app.register_blueprint(test_bp)


# if __name__ == "__main__":
def main():
    # sh = logging.StreamHandler()
    # sh.addFilter(IgnoreFilter())
    # sh.setFormatter(log.color_format())
    # sh.setLevel(logging.WARNING)
    # root_logger = logging.getLogger()
    # root_logger.addHandler(sh)
    # console_loglevel = logging.INFO
    # sh.setLevel(console_loglevel)
    # fh = logging.FileHandler("/var/log/yani.log")
    # fh.setLevel(logging.DEBUG)
    # fh.setFormatter(log.file_format())
    # root_logger.addHandler(fh)

    # print(GlobalVar.test)
    # print("hello yani")
    # LOG.info("hello yaninininini.......")
    # LOG.error("hello hl")
    app = create_app()
    LOG.info("hello yani")
    wsgi.server(eventlet.listen(("", 8778)), app)

