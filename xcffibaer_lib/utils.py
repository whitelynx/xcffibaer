'''Utility functions

'''
import os
import subprocess
import sys

from collist import collist


def toBool(input_string):
    return input_string.upper() in ('T', 'TRUE', '1', 'YES', 'ON')


VERBOSE = toBool(os.getenv('VERBOSE', 'false'))


class QuitApplication(Exception):
    pass


class MouseButton:
    left = 1
    middle = 2
    right = 3
    scroll_up = 4
    scroll_down = 5
    back = 8
    forward = 9

    names = {
        1: 'left button',
        2: 'middle button',
        3: 'right button',
        4: 'wheel up',
        5: 'wheel down',
        8: 'back button',
        9: 'forward button',
    }


def xStr(string):
    encoded = string.encode('utf8')
    return len(encoded), encoded


def Perimeter(*args):  # pylint: disable=invalid-name
    if len(args) == 1:
        return (args[0], args[0], args[0], args[0])
    if len(args) == 2:
        return (args[0], args[1], args[0], args[1])
    if len(args) == 3:
        return (args[0], args[1], args[2], args[1])
    return (args[0], args[1], args[2], args[3])


def dataAttrs(key, val):
    return key != '__dict__' and not callable(val)


def publicDataAttrs(key, val):
    return not key.startswith('__') and not key.endswith('__') and not callable(val)


def methodAttrs(_key, val):
    return callable(val)


def color(colorNum, message):
    return f'\x1b[{colorNum}m{message}\x1b[m'


def printError(message, *args):
    print(' '.join([color(91, message), *(str(arg) for arg in args)]), file=sys.stderr)
    sys.stderr.flush()


def printWarning(message, *args):
    print(' '.join([color('38;5;202', message), *(str(arg) for arg in args)]), file=sys.stderr)
    sys.stderr.flush()


def printInfo(message, *args):
    print(' '.join([color(93, message), *(str(arg) for arg in args)]))
    sys.stdout.flush()


def inspect(obj, attrFilter=publicDataAttrs):
    indent = '  ' if VERBOSE and not sys.stdout.isatty() else ''
    output = []

    for key in dir(obj):
        try:
            val = getattr(obj, key)
            if attrFilter(key, val):
                output.append('%s\x1b[96m%s:\x1b[m %r' % (indent, key, val))
        except Exception as error:  # pylint: disable=broad-except
            output.append('%s\x1b[96m%s:\x1b[m \x1b[91m%r\x1b[m' % (indent, key, error))

    if sys.stdout.isatty():
        print(collist(output))
    elif VERBOSE:
        print('\n'.join(output))
    else:
        print('  ' + ', '.join(output))
    sys.stdout.flush()


def runCommand(path):
    subprocess.call(os.path.expanduser(path))


def topStrut(width, height, left=0):
    return (
        0, 0, height, 0,         # left, right, top, bottom,
        0, 0,                    # left_start_y, left_end_y
        0, 0,                    # right_start_y, right_end_y,
        left, left + width - 1,  # top_start_x, top_end_x,
        0, 0                     # bottom_start_x, bottom_end_x
    )


def bottomStrut(width, height, left=0):
    return (
        0, 0, 0, height,        # left, right, top, bottom,
        0, 0,                   # left_start_y, left_end_y
        0, 0,                   # right_start_y, right_end_y,
        0, 0,                   # top_start_x, top_end_x,
        left, left + width - 1  # bottom_start_x, bottom_end_x
    )


def leftStrut(width, height, top=0):
    return (
        width, 0, 0, 0,         # left, right, top, bottom,
        top, top + height - 1,  # left_start_y, left_end_y
        0, 0,                   # right_start_y, right_end_y,
        0, 0,                   # top_start_x, top_end_x,
        0, 0                    # bottom_start_x, bottom_end_x
    )


def rightStrut(width, height, top=0):
    return (
        0, width, 0, 0,         # left, right, top, bottom,
        0, 0,                   # left_start_y, left_end_y
        top, top + height - 1,  # right_start_y, right_end_y,
        0, 0,                   # top_start_x, top_end_x,
        0, 0                    # bottom_start_x, bottom_end_x
    )
