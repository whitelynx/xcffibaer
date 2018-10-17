'''Window class

'''
# pylint: disable=too-many-arguments
from xcffib.xproto import ColormapAlloc, CW, EventMask, WindowClass


events = EventMask.ButtonPress | EventMask.EnterWindow \
        | EventMask.LeaveWindow | EventMask.Exposure \
        | EventMask.PropertyChange | EventMask.StructureNotify


def createWindow(
        connection, pos, size, depth, visualID, attributes=None, windowID=None, parentID=None,
        borderWidth=0, windowClass=WindowClass.InputOutput, checked=False):
    '''A convenience method to create a new window.

    The major advantage of this is the ability to use a dictionary to specify window attributes; this eliminates
    the need to figure out what order to specify values in according to the numeric values of the 'CW' or
    'ConfigWindow' enum members you're using.

    '''
    # pylint: disable=too-many-locals
    if windowID is None:
        windowID = connection.generate_id()

    attribMask = 0
    attribValues = list()

    # Values must be sorted by CW or ConfigWindow enum value, ascending.
    # Luckily, the tuples we get from dict.items will automatically sort correctly.
    if attributes is None:
        attributes = {}
    for attrib, value in sorted(attributes.items()):
        attribMask |= attrib
        attribValues.append(value)

    if checked:
        call = connection.core.CreateWindowChecked
    else:
        call = connection.core.CreateWindow

    cookie = call(
        depth,
        windowID, parentID,
        *pos, *size,
        borderWidth, windowClass,
        visualID,
        attribMask, attribValues
    )

    if checked:
        return windowID, cookie
    return windowID


class Window(object):
    windowsByID = {}

    def __init__(self, xSetup, x=0, y=0, width=1, height=1, borderWidth=0, attributes=None, parentID=None):
        self.xSetup = xSetup
        self.closing = False

        if parentID is None:
            parentID = self.screen.root

        if attributes is None:
            attributes = {}
        if CW.BackPixel not in attributes and CW.BackPixmap not in attributes:
            attributes[CW.BackPixel] = self.screen.black_pixel
        if CW.BorderPixel not in attributes and CW.BorderPixmap not in attributes:
            attributes[CW.BorderPixel] = self.screen.black_pixel
        if CW.Colormap not in attributes:
            colormap = self.connection.generate_id()
            self.connection.core.CreateColormapChecked(
                ColormapAlloc._None,  # pylint: disable=protected-access
                colormap,
                parentID,
                self.visual.visual_id
            )
            attributes[CW.Colormap] = colormap
        if CW.EventMask not in attributes:
            attributes[CW.EventMask] = events

        self.id, cookie = createWindow(  # pylint: disable=invalid-name
            self.connection,
            (x, y), (width, height),
            self.depth.depth, visualID=self.visual.visual_id,
            attributes=attributes, parentID=parentID, borderWidth=borderWidth,
            windowClass=WindowClass.InputOutput, checked=True
        )
        cookie.check()

        Window.windowsByID[self.id] = self
        print(f'Created window {self.id}')

    @property
    def connection(self):
        return self.xSetup.connection

    @property
    def screen(self):
        return self.xSetup.screen

    @property
    def depth(self):
        return self.xSetup.depth

    @property
    def visual(self):
        return self.xSetup.visual

    @property
    def theme(self):
        return self.xSetup.theme

    def handleEvent(self, event):
        pass

    def close(self):
        print(f'Destroying window {self.id}')
        self.closing = True
        self.connection.core.DestroyWindowChecked(self.id).check()
