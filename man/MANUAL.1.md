% THEFUCK(1)

# NAME

thefuck -  Magnificent app which corrects your previous console command

# SYNOPSIS

thefuck cmd-to-fix...

thefuck [--alias | -a] [ALIAS-NAME]

thefuck [--help | -h]

thefuck [--version | -v]

# DESCRIPTION

You should place this command in your `.bash_profile`, `.bashrc`, `.zshrc` or
other startup script:

    eval "$(thefuck --alias)"

Then you can simply use `fuck` whenever you fucked a command.

# CONFIGURATION

Configurations file is `~/.thefuck/settings.py`. It is a Python file that can
contain the following variables:

## `rules`
list of enabled rules, by default `thefuck.conf.DEFAULT_RULES`

## `require_confirmation`
requires confirmation before running new command, by default `True`

## `wait_command`
max amount of time in seconds for getting previous command output

## `no_colors`
disable colored output

## `priority`
dict with rules priorities, rule with lower priority will be matched first

## `debug`
enables debug output, by default `False`

Example of `settings.py`:

```python
rules = ['sudo', 'no_command']
require_confirmation = True
wait_command = 10
no_colors = False
priority = {'sudo': 100, 'no_command': 9999}
debug = False
```

# ENVIRONMENT

## THEFUCK_RULES 
list of enabled rules, like `DEFAULT_RULES:rm_root` or `sudo:no_command`

## THEFUCK_REQUIRE_CONFIRMATION
require confirmation before running new command, `true`/`false`

## THEFUCK_WAIT_COMMAND
max amount of time in seconds for getting previous command output

## THEFUCK_NO_COLORS
disable colored output, `true`/`false`

## THEFUCK_PRIORITY
priority of the rules, like `no_command=9999:apt_get=100`, rule with lower
priority will be matched first

## THEFUCK_DEBUG
enables debug output, true/false

# FILES

All configuration goes into *~/.thefuck/*.

# EXAMPLE

You can find examples on <https://github.com/nvbn/thefuck>.

# BUGS

You can report bugs on <https://github.com/nvbn/thefuck/issues>.
Please export `THEFUCK_DEBUG=true` before executing The Fuck and include
the complete output of The Fuck as well as the version of The Fuck and Python
and the shell you use.

# SEE ALSO

The Fuck source code and all documentation may be downloaded from
<https://github.com/nvbn/thefuck>.
