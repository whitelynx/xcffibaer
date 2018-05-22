'''Utility functions

'''
import sys

from collist import collist


class QuitApplication(Exception):
    pass


def xStr(string):
    encoded = string.encode('utf8')
    return len(encoded), encoded


def Perimeter(*args):  # pylint: disable=invalid-name
    if len(args) == 1:
        return (args[0], args[0], args[0], args[0])
    elif len(args) == 2:
        return (args[0], args[1], args[0], args[1])
    elif len(args) == 3:
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


def printWarning(message, *args):
    print(' '.join([color('38;5;202', message), *(str(arg) for arg in args)]), file=sys.stderr)


def printInfo(message, *args):
    print(' '.join([color(93, message), *(str(arg) for arg in args)]))


def inspect(obj, attrFilter=publicDataAttrs):
    output = []
    for key in dir(obj):
        val = getattr(obj, key)
        if attrFilter(key, val):
            #print('  %s: %r' % (key, val))
            output.append('  \x1b[96m%s:\x1b[m %r' % (key, val))
    print(collist(output) if sys.stdout.isatty() else '\n'.join(output))


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
