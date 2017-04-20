from collections import namedtuple

import cairocffi
from cairocffi.xcb import XCBSurface
from xcffib.xproto import PropMode, ExposeEvent, EnterNotifyEvent, \
     LeaveNotifyEvent, ButtonPressEvent, ConfigureNotifyEvent, \
     PropertyNotifyEvent

from .Window import Window
from .atoms import atoms
from .utils import xStr, QuitApplication, inspect


Chunks = namedtuple('Chunks', 'left right')

paintFinishMethod = None
#paintFinishMethod = 'flush'
#paintFinishMethod = 'show_page'
#paintFinishMethod = 'copy_page'


class Bar(Window):
    def __init__(self, connection, screen, visualType, theme, height=16):
        black = screen.black_pixel
        width = screen.width_in_pixels

        super().__init__(connection, screen, visualType.visual_id, width=width, height=height, background=black)

        self.chunks = Chunks([], [])

        self.theme = theme

        self.lastWidth = width
        self.lastHeight = height

        print('\x1b[93matoms:\x1b[m')
        inspect(atoms)
        connection.core.ChangeProperty(
            PropMode.Replace, self.id,
            atoms['_NET_WM_NAME'], atoms['UTF8_STRING'], 8,
            *xStr('xcffibär')
        )
        connection.core.MapWindow(self.id)

        connection.flush()

        #  :param conn: The :class:`xcffib.Connection` for an open XCB connection
        #  :param drawable:
        #      An XID corresponding to an XCB drawable (a pixmap or a window)
        #  :param visual: An :class:`xcffib.xproto.VISUALTYPE` object.
        #  :param width: integer
        #  :param height: integer
        self.surface = XCBSurface(connection, self.id, visualType, width, height)

        connection.flush()

    def addChunkLeft(self, chunk):
        chunk.setTheme(self.theme)
        self.chunks.left.append(chunk)

    def addChunkRight(self, chunk):
        chunk.setTheme(self.theme)
        self.chunks.right.append(chunk)

    def paint(self):
        print('\x1b[92mPaint...\x1b[m')

        context = cairocffi.Context(self.surface)
        with context:
            self.theme.background(context)
            context.paint()

        lastX = 0
        for chunk in self.chunks.left:
            with context:
                chunk.setContext(context)

                width, height = chunk.getSize()

                context.rectangle(lastX, 0, width, height)
                context.clip()
                context.translate(lastX, 0)

                chunk.paint()

                lastX += width

        lastX = self.lastWidth
        for chunk in self.chunks.right:
            with context:
                chunk.setContext(context)

                width, height = chunk.getSize()

                lastX -= width

                context.rectangle(lastX, 0, width, height)
                context.clip()
                context.translate(lastX, 0)

                chunk.paint()

        if paintFinishMethod is not None:
            getattr(self.surface, paintFinishMethod)()

        self.connection.flush()

    def handleEvent(self, event):
        if isinstance(event, ExposeEvent):
            self.paint()

        elif isinstance(event, ConfigureNotifyEvent):
            print('Property Change!')
            if event.width != self.lastWidth or event.height != self.lastHeight:
                print('\x1b[95m%d x %d\x1b[m' % (event.width, event.height))
                self.surface.set_size(event.width, event.height)
                #self.surface.set_drawable(self.id, event.width, event.height)
                self.lastWidth = event.width
                self.lastHeight = event.height
                self.paint()

        elif isinstance(event, PropertyNotifyEvent):
            print('Configure Notify!')

        elif isinstance(event, EnterNotifyEvent):
            print('Enter (%d, %d)' % (event.event_x, event.event_y))

        elif isinstance(event, LeaveNotifyEvent):
            print('Leave (%d, %d)' % (event.event_x, event.event_y))

        elif isinstance(event, ButtonPressEvent):
            print('Button %d down' % event.detail)
            raise QuitApplication()

    def cleanUp(self):
        #self.connection.core.FreeGC(self.gc)
        #self.connection.core.FreePixmap(self.pixmap)
        pass
