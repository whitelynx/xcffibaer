from collections import namedtuple

import cairocffi
from cairocffi.xcb import XCBSurface
from xcffib.xproto import CW, PropMode, ExposeEvent, EnterNotifyEvent, \
     LeaveNotifyEvent, ButtonPressEvent, ConfigureNotifyEvent, \
     PropertyNotifyEvent
import xpybutil.ewmh as ewmh

from .Window import Window
from .atoms import atoms
from .utils import xStr, QuitApplication, inspect


Chunks = namedtuple('Chunks', 'left right')

paintFinishMethod = None
#paintFinishMethod = 'flush'
#paintFinishMethod = 'show_page'
#paintFinishMethod = 'copy_page'


class Bar(Window):
    def __init__(self, connection, screen, visualType, theme, height=16, bottom=False, screenExtents=None):
        black = screen.black_pixel

        width = screen.width_in_pixels if screenExtents is None else screenExtents.width

        if bottom:
            outputHeight = screen.height_in_pixels if screenExtents is None else screenExtents.height
            x, y = 0 if screenExtents is None else screenExtents.x, outputHeight - height
        else:
            if screenExtents is not None:
                x, y = screenExtents.x, screenExtents.y
            else:
                x, y = 0, 0

        attributes = {
            CW.BackPixel: black,
            CW.BorderPixel: black,
            CW.OverrideRedirect: 1,
        }

        super().__init__(connection, screen, visualType.visual_id, x, y, width, height, attributes=attributes)

        setWMStrutPartialCookie = ewmh.set_wm_strut_partial_checked(
            self.id,
            0, 0, 0, height,  # left, right, top, bottom,
            0, 0,             # left_start_y, left_end_y
            0, 0,             # right_start_y, right_end_y,
            0, 0,             # top_start_x, top_end_x,
            0, width          # bottom_start_x, bottom_end_x
        )

        self.chunks = Chunks([], [])

        self.theme = theme

        self.lastWidth = width
        self.lastHeight = height

        connection.core.ChangeProperty(
            PropMode.Replace, self.id,
            atoms['_NET_WM_NAME'], atoms['UTF8_STRING'], 8,
            *xStr('xcffibär')
        )
        connection.core.MapWindow(self.id)

        self.surface = XCBSurface(connection, self.id, visualType, width, height)

        connection.flush()

        setWMStrutPartialCookie.check()

    def addChunkLeft(self, chunk):
        chunk.setTheme(self.theme)
        self.chunks.left.append(chunk)

    def addChunkRight(self, chunk):
        chunk.setTheme(self.theme)
        self.chunks.right.append(chunk)

    def addLeft(self, *chunks):
        for chunk in chunks:
            self.addChunkLeft(chunk)

    def addRight(self, *chunks):
        for chunk in chunks:
            self.addChunkRight(chunk)

    def paint(self):
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

        else:
            super().handleEvent(event)

    def cleanUp(self):
        #self.connection.core.FreeGC(self.gc)
        #self.connection.core.FreePixmap(self.pixmap)
        pass
