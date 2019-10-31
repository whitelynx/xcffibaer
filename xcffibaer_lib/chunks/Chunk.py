'''Base Chunk class

'''
from ..utils import Perimeter, printWarning


class Chunk(object):
    def __init__(self, theme=None, styles=None, width=None, height=None, onClick=None):
        self.context = None
        self.chunkStyle = None
        self.theme = None
        self._styles = []

        if styles is None:
            styles = []
        elif isinstance(styles, str):
            styles = styles.split()
        self.styles = styles

        self._intrinsicInnerWidth = 0
        self._intrinsicInnerHeight = 0
        self._overrideWidth = width
        self._overrideHeight = height
        self._onClick = onClick
        self.padding = Perimeter(0)

        if theme:
            self.setTheme(theme)

        self._updateInnerWidth()
        self._updateInnerHeight()

    @property
    def styles(self):
        return self._styles

    @styles.setter
    def styles(self, styles):
        self._styles = styles
        if self.theme:
            self.setTheme(self.theme)

    def setTheme(self, theme):
        self.theme = theme
        self.applyStyle(theme.getChunkStyle(*self.getStyleNames()))

    def getStyleNames(self):
        styleNames = [self.__class__.__name__] + self.styles
        # Without this reverse, earlier styles apparently override later ones, which is unexpected
        styleNames.reverse()
        return styleNames

    def applyStyle(self, chunkStyle):
        self.chunkStyle = chunkStyle
        self.padding = self.chunkStyle.padding or Perimeter(0)
        self._updateInnerWidth()
        self._updateInnerHeight()

    def setContext(self, context):
        self.context = context
        self.updateIntrinsicSize()

    def beginPaint(self):
        ctx = self.context
        padding = self.padding

        if self.chunkStyle.background:
            self.chunkStyle.background.paint(ctx)

        ctx.translate(padding[3], padding[0])
        ctx.rectangle(0, 0, self.innerWidth, self.innerHeight)
        ctx.clip()

        return ctx

    def paint(self):
        pass

    def onClick(self, event, clickX, clickY):
        if self._onClick:
            self._onClick(event, clickX, clickY)
        else:
            printWarning(f'{self.__class__.__name__}: Unhandled button {event.detail} click at ({clickX}, {clickY}).')

    # Intrinsic inner dimensions
    def updateIntrinsicSize(self):
        self.intrinsicInnerWidth, self.intrinsicInnerHeight = 0, 0

    @property
    def intrinsicInnerWidth(self):
        return self._intrinsicInnerWidth

    @intrinsicInnerWidth.setter
    def intrinsicInnerWidth(self, value):
        self._intrinsicInnerWidth = value
        self._updateInnerWidth()

    @property
    def intrinsicInnerHeight(self):
        return self._intrinsicInnerHeight

    @intrinsicInnerHeight.setter
    def intrinsicInnerHeight(self, value):
        self._intrinsicInnerHeight = value
        self._updateInnerHeight()

    # Override dimensions
    @property
    def overrideWidth(self):
        return self._overrideWidth

    @overrideWidth.setter
    def overrideWidth(self, value):
        self._overrideWidth = value
        self._updateInnerWidth()

    @property
    def overrideHeight(self):
        return self._overrideHeight

    @overrideHeight.setter
    def overrideHeight(self, value):
        self._overrideHeight = value
        self._updateInnerHeight()

    # Calculated inner dimensions
    def _updateInnerHeight(self):
        if self._overrideHeight is not None:
            padding = self.padding
            self.innerHeight = self._overrideHeight - padding[0] - padding[2]
        else:
            self.innerHeight = self._intrinsicInnerHeight

    def _updateInnerWidth(self):
        if self._overrideWidth is not None:
            padding = self.padding
            self.innerWidth = self._overrideWidth - padding[3] - padding[1]
        else:
            self.innerWidth = self._intrinsicInnerWidth

    # Calculated outer dimensions
    @property
    def outerHeight(self):
        padding = self.padding
        return padding[0] + self.innerHeight + padding[2]

    @property
    def outerWidth(self):
        padding = self.padding
        return padding[3] + self.innerWidth + padding[1]

    def getSize(self):
        return self.outerWidth, self.outerHeight
