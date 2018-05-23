'''Bar class

'''
from collections import namedtuple
import os

import cairocffi
from cairocffi.xcb import XCBSurface
from xcffib.xproto import CW, PropMode, ExposeEvent, EnterNotifyEvent, \
     LeaveNotifyEvent, ButtonPressEvent, ConfigureNotifyEvent, \
     PropertyNotifyEvent
import xpybutil.ewmh as ewmh
import xpybutil.icccm as icccm

from .Window import Window
from .atoms import atoms
from .utils import xStr, QuitApplication, topStrut, bottomStrut


Chunks = namedtuple('Chunks', 'left right')

paintFinishMethod = None
#paintFinishMethod = 'flush'
#paintFinishMethod = 'show_page'
#paintFinishMethod = 'copy_page'

buttonNames = {
    1: 'left button',
    2: 'middle button',
    3: 'right button',
    4: 'wheel up',
    5: 'wheel down',
    8: 'back button',
}


class Bar(Window):
    def __init__(self, xSetup, height=16, bottom=False, screenExtents=None, name=''):
        black = xSetup.screen.black_pixel

        width = xSetup.screen.width_in_pixels if screenExtents is None else screenExtents.width

        if bottom:
            outputHeight = xSetup.screen.height_in_pixels if screenExtents is None else screenExtents.height
            pos = 0 if screenExtents is None else screenExtents.x, outputHeight - height
        else:
            if screenExtents is not None:
                pos = screenExtents.x, screenExtents.y
            else:
                pos = 0, 0

        attributes = {
            CW.BackPixel: black,
            CW.BorderPixel: black,
        }

        super().__init__(xSetup, *pos, width, height, attributes=attributes)

        strutPartial = bottomStrut(width, height, screenExtents.x) if bottom \
            else topStrut(width, screenExtents.y + height, screenExtents.x)

        cookies = [
            icccm.set_wm_state_checked(self.id, icccm.State.Normal, 0),
            icccm.set_wm_name_checked(self.id, f'xcffibaer_{name}'),
            icccm.set_wm_class_checked(self.id, 'xcffibaer', 'xcffibär'),
            ewmh.set_wm_pid_checked(self.id, os.getpid()),
            ewmh.set_wm_strut_checked(self.id, *strutPartial[:4]),
            ewmh.set_wm_strut_partial_checked(self.id, *strutPartial),
            ewmh.set_wm_window_type_checked(self.id, [atoms['_NET_WM_WINDOW_TYPE_DOCK']]),
            ewmh.set_wm_state_checked(self.id, [atoms['_NET_WM_STATE_STICKY'], atoms['_NET_WM_STATE_ABOVE']]),
            #FIXME: This fails. Doing it manually below works.
            #ewmh.set_wm_name_checked(self.id, 'xcffibär'),
        ]

        self.chunks = Chunks([], [])
        self.chunkExtents = {}

        self.lastWidth = width
        self.lastHeight = height

        #TODO: Make this request checked.
        self.connection.core.ChangeProperty(
            PropMode.Replace, self.id,
            atoms['_NET_WM_NAME'], atoms['UTF8_STRING'], 8,
            *xStr('xcffibär')
        )
        self.connection.core.MapWindow(self.id)

        self.surface = XCBSurface(self.connection, self.id, self.visual, width, height)

        self.connection.flush()

        for cookie in cookies:
            cookie.check()

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
            context.save()
            self.theme.background(context)
            context.set_operator(cairocffi.OPERATOR_SOURCE)
            context.paint()
            context.restore()

        chunkExtents = {}

        lastX = 0
        for chunk in self.chunks.left:
            with context:
                chunk.setContext(context)

                width, height = chunk.getSize()
                chunkExtents[chunk] = (lastX, lastX + width)

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
                chunkExtents[chunk] = (lastX, lastX + width)

                lastX -= width

                context.rectangle(lastX, 0, width, height)
                context.clip()
                context.translate(lastX, 0)

                chunk.paint()

        if paintFinishMethod is not None:
            getattr(self.surface, paintFinishMethod)()

        self.connection.flush()

        self.chunkExtents = chunkExtents

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
            print(f'{buttonNames.get(event.detail, f"button {event.detail}")} down')
            if event.detail == 3:
                raise QuitApplication()
            else:
                self.onClick(event)

        else:
            super().handleEvent(event)

    def onClick(self, event):
        for chunk, (startX, endX) in self.chunkExtents.items():
            if startX <= event.event_x < endX:
                chunk.onClick(event, event.event_x - startX, event.event_y)
                return

    def cleanUp(self):
        #self.connection.core.FreeGC(self.gc)
        #self.connection.core.FreePixmap(self.pixmap)
        pass
