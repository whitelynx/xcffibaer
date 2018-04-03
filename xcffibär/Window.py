from xcffib.xproto import CW, EventMask, WindowClass


events = EventMask.ButtonPress | EventMask.EnterWindow \
        | EventMask.LeaveWindow | EventMask.Exposure \
        | EventMask.PropertyChange | EventMask.StructureNotify


def createWindow(connection, x, y, width, height, depth, visualID, attributes={}, windowID=None, parentID=None,
                 borderWidth=0, windowClass=WindowClass.InputOutput, checked=False):
    """A convenience method to create a new window.

    The major advantage of this is the ability to use a dictionary to specify window attributes; this eliminates
    the need to figure out what order to specify values in according to the numeric values of the 'CW' or
    'ConfigWindow' enum members you're using.

    """
    if windowID is None:
        windowID = connection.generate_id()

    attribMask = 0
    attribValues = list()

    # Values must be sorted by CW or ConfigWindow enum value, ascending.
    # Luckily, the tuples we get from dict.items will automatically sort correctly.
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
        x, y, width, height,
        borderWidth, windowClass,
        visualID,
        attribMask, attribValues
    )

    if checked:
        return windowID, cookie
    else:
        return windowID


class Window(object):
    windowsByID = {}

    def __init__(self, connection, screen, visualID, x=0, y=0, width=1, height=1, borderWidth=0, attributes={},
                 parentID=None):
        self.connection = connection
        self.screen = screen

        if CW.BackPixel not in attributes:
            attributes[CW.BackPixel] = screen.black_pixel
        if CW.EventMask not in attributes:
            attributes[CW.EventMask] = events

        if parentID is None:
            parentID = screen.root

        self.id, cookie = createWindow(
            connection,
            x, y, width, height,
            screen.root_depth, visualID,
            attributes=attributes, parentID=parentID, borderWidth=borderWidth,
            windowClass=WindowClass.InputOutput, checked=True
        )
        cookie.check()

        Window.windowsByID[self.id] = self
        print(f'Created window {self.id}')

    def handleEvent(self, event):
        pass

    def close(self):
        print(f'Destroying window {self.id}')
        self.connection.core.DestroyWindowChecked(self.id).check()
