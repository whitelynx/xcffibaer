'''XSetup class

'''


class XSetup:
    def __init__(self, connection, screen, depthInfo, visualType, root, theme):
        self.connection = connection
        self.screen = screen
        self.depth = depthInfo
        self.visual = visualType
        self.root = root
        self.theme = theme
