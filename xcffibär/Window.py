from xcffib.xproto import CW, EventMask, WindowClass


events = EventMask.ButtonPress | EventMask.EnterWindow \
        | EventMask.LeaveWindow | EventMask.Exposure \
        | EventMask.PropertyChange | EventMask.StructureNotify


class Window(object):
    def __init__(self, connection, screen, visualID, x=0, y=0, width=1, height=1, border=0, background=None):
        self.id = connection.generate_id()
        self.connection = connection
        self.screen = screen

        if background is None:
            background = screen.black_pixel

        cookie = connection.core.CreateWindowChecked(
            screen.root_depth, self.id, screen.root,
            x, y, width, height, border,
            WindowClass.InputOutput,
            visualID,
            CW.BackPixel | CW.EventMask,
            [background, events]
        )
        cookie.check()
