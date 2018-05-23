'''XSetup class

'''


class XSetup(object):
    def __init__(self, connection, screen, depthInfo, visualType, theme):
        self.connection = connection
        self.screen = screen
        self.depth = depthInfo
        self.visual = visualType
        self.theme = theme
