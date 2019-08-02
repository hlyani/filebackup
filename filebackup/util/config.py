import configparser
import os

"""
for example:
    import config as cfg
    CONF = cfg.CONF
    CONF.get('default', 'verbose')
"""

# use DEFAULT_CONFIG if no configuration file
DEFAULT_CONFIG = {
    "default": {
        "key_secret": "value_secret",
        "log_level": "INFO",
        "logfile": "/var/log/yani.log",
        "logfile_size": "100",
        "logfile_backup_count": "5",
    },
    "test": {"test": "test"},
}


class ConfigOpts(configparser.ConfigParser):
    def __init__(self):
        configparser.DEFAULTSECT = "default"
        configparser.ConfigParser.__init__(self)

    def parse_cfg(self, _file):
        if os.path.exists(_file):
            self.read(_file)
        if not self.sections():
            print("Failed to parse config file, using default value!")
            for section, pair_options in DEFAULT_CONFIG.items():
                if not self.has_section(section):
                    self.add_section(section)
                for option, value in pair_options.items():
                    self.set(section, option, value)
        else:
            for section, pair_options in DEFAULT_CONFIG.items():
                for option, value in pair_options.items():
                    if not self.has_option(section, option):
                        self.set(section, option, value)


CONF = ConfigOpts()


def config_init(config_file):
    global CONF
    CONF.parse_cfg(config_file)
