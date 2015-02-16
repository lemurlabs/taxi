from __future__ import unicode_literals

import codecs
import io
import os
import six
import tempfile
from unittest import TestCase

from taxi.app import Taxi
from taxi.utils.file import expand_filename


class CommandTestCase(TestCase):
    def setUp(self):
        self.stdout = io.TextIOWrapper(io.BytesIO())

        _, self.config_file = tempfile.mkstemp()
        _, self.entries_file = tempfile.mkstemp()
        _, self.projects_db = tempfile.mkstemp()

        self.default_config = {
            'default': {
                'site': 'https://zebra.liip.ch',
                'username': 'john.doe',
                'password': 'john.doe',
                'date_format': '%d/%m/%Y',
                'editor': '/bin/false',
                'file': self.entries_file,
                'use_colors': '0'
            },
            'backends': {
                'dummy': 'dummy://foo:bar@localhost/test?foo=bar',
            },
            'dummy_aliases': {
                'alias_1': '123/456'
            },
        }

        self.default_options = {
        }

        self.default_options['config'] = self.config_file
        self.default_options['stdout'] = self.stdout
        self.default_options['projects_db'] = self.projects_db

    def tearDown(self):
        entries_file = expand_filename(self.entries_file)

        os.remove(self.config_file)
        if os.path.exists(entries_file):
            os.remove(entries_file)
        os.remove(self.projects_db)

    def write_config(self, config):
        with open(self.config_file, 'w') as f:
            for (section, params) in six.iteritems(config):
                f.write("[%s]\n" % section)

                for (param, value) in six.iteritems(params):
                    f.write("%s = %s\n" % (param, value))

    def write_entries(self, contents):
        with codecs.open(expand_filename(self.entries_file), 'a', 'utf-8') as f:
            f.write(contents)

    def read_entries(self):
        with codecs.open(expand_filename(self.entries_file), 'r', 'utf-8') as f:
            contents = f.read()

        return contents

    def run_command(self, command_name, args=None, options=None,
                    config_options=None):
        """
        Run the given taxi command with the given arguments and options. Before
        running the command, the configuration file is written with the given
        `config_options`, if any, or with the default config options.

        The output of the command is put in the `self.stdout` property and
        returned as a string.

        Args:
            command_name -- The name of the command to run
            args -- An optional list of arguments for the command
            options -- An optional options hash for the command
            config_options -- An optional options hash that will be used to
                              write the config file before running the command
        """
        if args is None:
            args = []

        if options is None:
            options = self.default_options

        if config_options is None:
            config_options = self.default_config
        else:
            config_options = dict(
                list(self.default_config.items()) +
                list(config_options.items())
            )
        self.write_config(config_options)

        self.stdout = io.TextIOWrapper(io.BytesIO())
        options['stdout'] = self.stdout

        app = Taxi()
        app.run_command(command_name, options=options, args=args)
        self.stdout.seek(0)

        return self.stdout.read()
