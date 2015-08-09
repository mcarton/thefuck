from . import logs, conf, types, shells, __version__
from .corrector import get_corrected_commands, get_rules
from .ui import select_command
from os.path import expanduser
from pathlib import Path
from pprint import pformat
from psutil import Process, TimeoutExpired
from subprocess import Popen, PIPE
import argparse
import colorama
import os
import six
import sys


def setup_user_dir():
    """Returns user config dir, create it when it doesn't exist."""
    user_dir = Path(expanduser('~/.thefuck'))
    rules_dir = user_dir.joinpath('rules')
    if not rules_dir.is_dir():
        rules_dir.mkdir(parents=True)
    conf.initialize_settings_file(user_dir)
    return user_dir


def wait_output(settings, popen):
    """Returns `True` if we can get output of the command in the
    `wait_command` time.

    Command will be killed if it wasn't finished in the time.

    """
    proc = Process(popen.pid)
    try:
        proc.wait(settings.wait_command)
        return True
    except TimeoutExpired:
        for child in proc.children(recursive=True):
            child.kill()
        proc.kill()
        return False


def get_command(settings, args):
    """Creates command from `args` and executes it."""
    if six.PY2:
        script = ' '.join(arg.decode('utf-8') for arg in args)
    else:
        script = ' '.join(args)

    if not script:
        return

    script = shells.from_shell(script)
    env = dict(os.environ)
    env.update(settings.env)

    with logs.debug_time(u'Call: {}; with env: {};'.format(script, env),
                         settings):
        result = Popen(script, shell=True, stdout=PIPE, stderr=PIPE, env=env)
        if wait_output(settings, result):
            stdout = result.stdout.read().decode('utf-8')
            stderr = result.stderr.read().decode('utf-8')

            logs.debug(u'Received stdout: {}'.format(stdout), settings)
            logs.debug(u'Received stderr: {}'.format(stderr), settings)

            return types.Command(script, stdout, stderr)
        else:
            logs.debug(u'Execution timed out!', settings)
            return types.Command(script, None, None)


def run_command(command, settings):
    """Runs command from rule for passed command."""
    if command.side_effect:
        command.side_effect(command, settings)
    shells.put_to_history(command.script)
    print(command.script)


# Entry points:

def main():
    description = 'Magnificent app which corrects your previous console command'
    parser = argparse.ArgumentParser(description=description,
                                     add_help=False)

    cmds = parser.add_mutually_exclusive_group(required=True)

    alias_name = shells.thefuck_alias()
    cmds.add_argument('--alias', '-a',
                      metavar='ALIAS_NAME=' + alias_name,
                      nargs='?',
                      help='output an example of alias for the current shell',
                      const=alias_name,
                      action=AliasAction)

    cmds.add_argument('--fix', '-f',
                      metavar='CMD',
                      nargs='+',
                      action=FixAction,
                      help='fix the given command')

    cmds.add_argument('--help', '-h',
                      nargs=0,
                      action=HelpAction,
                      help='show this help message and exit')

    cmds.add_argument('--rules', '-r',
                      nargs=0,
                      action=ListAction,
                      help='list enabled rules')

    cmds.add_argument('--version', '-v',
                      version=__version__,
                      action='version')

    parser.parse_args()

class FixAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        colorama.init()
        user_dir = setup_user_dir()
        settings = conf.get_settings(user_dir)
        with logs.debug_time('Total', settings):
            logs.debug(u'Run with settings: {}'.format(pformat(settings)), settings)

            command = get_command(settings, values)
            corrected_commands = get_corrected_commands(command, user_dir, settings)
            selected_command = select_command(corrected_commands, settings)
            if selected_command:
                run_command(selected_command, settings)


class AliasAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print_alias(values)


def print_alias(alias=None):
    if alias is None:
        # support for legacy `thefuck-alias` command
        if len(sys.argv) > 1:
            alias = sys.argv[1]
        else:
            alias = shells.thefuck_alias()

    print(shells.app_alias(alias))


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        user_dir = setup_user_dir()
        settings = conf.get_settings(user_dir)

        print('Enabled rules:')
        for rule in get_rules(user_dir, settings):
            print('\t', rule.name)


class HelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        msg = parser.format_help()

        # fix confusing generated message
        msg = msg.replace('CMD [CMD ...]', 'CMD')
        msg = msg.replace('optional arguments:', 'arguments:')

        parser._print_message(msg)
        parser.exit()
