from .utils import xStr


atomNames = [
    '_NET_WM_NAME',
    'UTF8_STRING',
]
atoms = {}


def initAtoms(conn):
    print('\x1b[92mInitializing atoms...\x1b[m')

    atomCookies = dict(
        (name, conn.core.InternAtom(False, *xStr(name)))
        for name in atomNames
    )
    atoms.update(dict(
        (name, cookie.reply().atom)
        for name, cookie in atomCookies.items()
    ))
