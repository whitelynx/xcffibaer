'''X11 atom cache

'''
from .utils import printInfo, xStr


atomNames = [
    'UTF8_STRING',
    '_NET_WM_NAME',
    '_NET_WM_WINDOW_TYPE_DOCK',
    '_NET_WM_STATE_STICKY',
    '_NET_WM_STATE_ABOVE',
]
atoms = {}


def initAtoms(conn):
    printInfo('Initializing atoms...')

    atomCookies = dict(
        (name, conn.core.InternAtom(False, *xStr(name)))
        for name in atomNames
    )
    atoms.update(dict(
        (name, cookie.reply().atom)
        for name, cookie in atomCookies.items()
    ))
