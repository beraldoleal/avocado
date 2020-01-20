# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; specifically version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# This code was inspired in the autotest project,
# client/shared/settings.py
#
# Authors: Travis Miller <raphtee@google.com>
#          Beraldo Leal <bleal@redhat.com>

"""
This module is a new and experimental configuration handler.

This will handle both, command line args and configuration files.
Settings() = configparser + argparser

Settings() is an attempt to implement part of BP001 and concentrate all
default values in one place. This module will read the Avocado configuration
options from many sources, in the following order:

  1. Default values (defaults.conf or defaults.py). This is a "source code"
     file and should not be changed by the Avocado' user.

  2. User/System configuration files (/etc/avocado or ~/.avocado/). This is
     configured by the user, on a more "permanent way".

  3. Command-line options parsed in runtime. This is configured by the user, on
     a more "temporary way";

ATTENTION: This is a future module, and will be moved out from this package
soon.
"""

import configparser
import glob
import os

from pkg_resources import resource_filename

from ..settings_dispatcher import SettingsDispatcher
from ...utils import path


class SettingsError(Exception):
    """
    Base settings error.
    """


class DuplicatedNamespace(SettingsError):
    """
    Raised when a namespace is already registered.
    """


class ConfigFileNotFound(SettingsError):
    """
    Error thrown when the main settings file could not be found.
    """

    def __init__(self, path_list):
        super(ConfigFileNotFound, self).__init__()
        self.path_list = path_list

    def __str__(self):
        return ("Could not find the avocado config file after looking in: %s" %
                self.path_list)


class Settings:
    """Settings, an experimental Avocado configuration handler.

    It is a simple wrapper around configparser and argparse.

    Also, one object of this class could be passed as config to plugins and
    modules.

    Please, note that most of methods and attributes here are private. Only
    public methods and attributes should be used outside this module.
    """

    def __init__(self, config_path=None):
        """Constructor. Tries to find the main settings files and load them.

        :param config_path: Path to a config file. Useful for unittesting.
        """
        self._config = configparser.ConfigParser()
        self._all_config_paths = []
        self._config_paths = []
        self._short_mapping = {}
        self._long_mapping = {}
        self._namespaces = {}

        # 1. Prepare config paths
        if config_path is None:
            self._prepare_base_dirs()
            self._append_config_paths()
        else:
            # Only used by unittests (the --config parses the file later)
            self._all_config_paths.append(config_path)

        # 2. Parse/read all config paths
        self._config_paths = self._config.read(self._all_config_paths)
        if not self._config_paths:
            raise ConfigFileNotFound(self._all_config_paths)

    def _append_config_paths(self):
        # 1. Append Defaults
        self._append_pkg_defaults()

        # 2. Override with system config
        self._append_system_config()

        # Allow plugins to modify/extend the list of configs
        dispatcher = SettingsDispatcher()
        if dispatcher.extensions:
            dispatcher.map_method('adjust_settings_paths',
                                  self._all_config_paths)

        # 3. Override with the user's local config
        self._append_user_config()

    def _append_pkg_defaults(self):
        config_pkg_base = os.path.join('etc', 'avocado', 'defaults.conf')
        config_path_pkg = resource_filename('avocado', config_pkg_base)
        self._all_config_paths.append(config_path_pkg)

    def _append_system_config(self):
        self._all_config_paths.append(self._config_path_system)
        configs = glob.glob(os.path.join(self._config_dir_system_extra,
                                         '*.conf'))
        for extra_file in configs:
            self._all_config_paths.append(extra_file)

    def _append_user_config(self):
        if not os.path.exists(self._config_path_local):
            self._create_empty_config()
        self._all_config_paths.append(self._config_path_local)

    def _create_empty_config(self):
        try:
            path.init_dir(self._config_dir_local)
            with open(self._config_path_local, 'w') as config_local_fileobj:
                content = ("# You can use this file to override "
                           "configuration values from '%s and %s\n"
                           % (self._config_path_system,
                              self._config_dir_system_extra))
                config_local_fileobj.write(content)
        except IOError:     # Some users can't write it (docker)
            pass

    # def _get_option_from_tag(self, tag):
    #     """tag = long option or positional."""
    #     tag = tag.replace('_', '-')
    #     try:
    #         mapping = self._long_mapping[tag]
    #         return self._namespaces[mapping]
    #     except KeyError:
    #         msg = "{} not found in internal mapping.".format(tag)
    #         raise SettingsError(msg)

    def _prepare_base_dirs(self):
        cfg_dir = '/etc'
        user_dir = os.path.expanduser("~")

        if 'VIRTUAL_ENV' in os.environ:
            cfg_dir = os.path.join(os.environ['VIRTUAL_ENV'], 'etc')
            user_dir = os.environ['VIRTUAL_ENV']

        self._config_dir_system = os.path.join(cfg_dir, 'avocado')
        self._config_dir_system_extra = os.path.join(cfg_dir,
                                                     'avocado',
                                                     'conf.d')
        self._config_dir_local = os.path.join(user_dir, '.config', 'avocado')
        self._config_path_system = os.path.join(self._config_dir_system,
                                                'avocado.conf')
        self._config_path_local = os.path.join(self._config_dir_local,
                                               'avocado.conf')

    def as_dict(self):
        """Return an ordered dictionary with the current active settings.

        This will return a ordered dict of both: configparse and merged
        argparse options.
        """
        result = {}
        for section in self._config.sections():
            result[section] = dict(self._config.items(section))
        return result

    def get(self, section, key):
        """Returns the current value inside a setion + key.

        If this section do not exists on config files but it was registered
        dynamicaly with `register_option` by a plugin, this will also get this
        value.

        :param section: Section in configuration file.
        :param key: name of key inside that section.
        """
        namespace = "{}.{}".format(section, key)

        if namespace in self._namespaces:
            default = self._namespaces[namespace]['default']
            key_type = self._namespaces[namespace]['key_type']
        else:
            return None

        try:
            if key_type is str:
                return self._config.get(section, key, fallback=default)
            elif key_type is bool:
                return self._config.getboolean(section, key, fallback=default)
            elif key_type is int:
                return self._config.getint(section, key, fallback=default)
            elif key_type is float:
                return self._config.getfloat(section, key, fallback=default)
            elif key_type is list:
                value = self._config.get(section, key, fallback=default)
                if isinstance(value, list):
                    return value
                if value:
                    return value.split(',')
                return []
            else:
                # Custom key type
                value = self._config.get(section, key, fallback=default)
                return key_type(value)
        except configparser.NoSectionError:
            raise SettingsError("Section {} is invalid.".format(section))
        except ValueError:
            raise SettingsError("Could not convert type.")
        except configparser.Error:
            raise SettingsError("{} is invalid.".format(key))

    def merge_with_arguments(self, arg_parse_config):
        """This method will merge the configparse with argparse.

        After parsing argument options this method should be executed to have
        an unified settings.

        :param arg_parse_config: argparse.config dictionary with all command
        line parsed arguments.
        """
        for tag, value in arg_parse_config.items():
            if value is not None:  # Ignoring None values
                try:
                    option = self._namespaces[tag]
                except KeyError:
                    continue  # Not registered yet, using the new module
                section = option.get('section')
                key = option.get('key')
                self.update_settings(section, key, value)

    def register_option(self, section, key, default, help_msg, key_type=str,
                        parser=None, positional_arg=False, short_arg=None,
                        long_arg=None, choices=None, nargs=None, metavar=None,
                        required=False, action=None):
        """Register an option dinamically.

        TODO: Better document this
        """
        namespace = "{}.{}".format(section, key)

        # Check if namespace is already registered
        if namespace in self._namespaces:
            msg = "Key {} already registered in section {}".format(key,
                                                                   section)
            raise DuplicatedNamespace(msg)

        # Register the option to a dynamic in-memory namespaces
        self._namespaces[namespace] = {'section': section,
                                       'key': key,
                                       'default': default,
                                       'key_type': key_type,
                                       'help_msg': help_msg,
                                       'parser': parser}

        if not parser:
            return  # Nothing else to do here

        arg_parse_args = {'help': help_msg,
                          'default': default}
        if nargs:
            arg_parse_args['nargs'] = nargs
        if metavar:
            arg_parse_args['metavar'] = metavar
        if choices:
            arg_parse_args['choices'] = choices
        if action:
            arg_parse_args['action'] = action

        # This will pre-configure a default action for bool types
        if key_type is bool:
            if default is False:
                arg_parse_args['action'] = 'store_true'
            else:
                arg_parse_args['action'] = 'store_false'
        elif key_type is list:
            # we convert a list into string to argparse. Yes, it is strange.
            arg_parse_args['type'] = str
        else:
            # Current argparse documentation is not clear, but 'type' and
            # 'required' are not accepted when 'store_*' is passed.
            arg_parse_args['type'] = key_type

        if positional_arg:
            if metavar is None:
                arg_parse_args['metavar'] = namespace.split('.')[-1]
            parser.add_argument(namespace, **arg_parse_args)
        else:
            arg_parse_args['required'] = required
            arg_parse_args['dest'] = namespace  # most of the magic is here
            name_or_tags = []
            if short_arg:
                # self._register_short_arg(short_arg, long_arg)
                name_or_tags.append(short_arg)
            if long_arg:
                # self._register_long_arg(long_arg, namespace)
                name_or_tags.append(long_arg)
            parser.add_argument(*name_or_tags, **arg_parse_args)

        self._namespaces[namespace]['arg_parse_args'] = arg_parse_args

    # def _register_long_arg(self, long_arg, namespace):
    #     # TODO: Need to register with the section
    #     long_arg = long_arg.replace('--', '')
    #     if long_arg in self._long_mapping:
    #         msg = "Option {} already registered.".format(long_arg)
    #         raise SettingsError(msg)
    #     self._long_mapping[long_arg] = namespace

    # def _register_short_arg(self, short_arg, long_arg):
    #     short_arg = long_arg.replace('-', '')
    #     if short_arg in self._short_mapping:
    #         msg = "Option {} already registered.".format(short_arg)
    #         raise SettingsError(msg)
    #     self._short_mapping[short_arg] = long_arg

    def update_settings(self, section, key, value):
        if isinstance(value, list):
            value = ','.join(value)

        if section not in self._config:
            self._config[section] = {key: str(value)}
        else:
            self._config[section][key] = str(value)


settings = Settings()  # pylint: disable-msg=invalid-name
