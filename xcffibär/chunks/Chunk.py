from ..utils import Perimeter


class Chunk(object):
    def __init__(self, theme=None, class_=None, width=None, height=None):
        self.class_ = class_

        self._intrinsicInnerWidth = 0
        self._intrinsicInnerHeight = 0
        self._overrideWidth = width
        self._overrideHeight = height

        if theme:
            self.setTheme(theme)

    def setTheme(self, theme):
        self.applyStyle(theme.chunkStyle(self.getClass()))

    def getClass(self):
        return self.class_ or self.__class__.__name__

    def applyStyle(self, chunkStyle):
        self.chunkStyle = chunkStyle

    def setContext(self, context):
        self.context = context
        self.updateIntrinsicSize()

    def paint(self, context):
        pass

    @property
    def padding(self):
        return self.chunkStyle.padding or Perimeter(0)

    # Intrinsic inner dimensions
    def updateIntrinsicSize(self):
        self.intrinsicInnerWidth, self.intrinsicInnerHeight = 0, 0

    @property
    def intrinsicInnerWidth(self):
        return self._intrinsicInnerWidth

    @intrinsicInnerWidth.setter
    def intrinsicInnerWidth(self, value):
        self._intrinsicInnerWidth = value

    @property
    def intrinsicInnerHeight(self):
        return self._intrinsicInnerHeight

    @intrinsicInnerHeight.setter
    def intrinsicInnerHeight(self, value):
        self._intrinsicInnerHeight = value

    # Override dimensions
    @property
    def overrideWidth(self):
        return self._overrideWidth

    @overrideWidth.setter
    def overrideWidth(self, value):
        self._overrideWidth = value

    @property
    def overrideHeight(self):
        return self._overrideHeight

    @overrideHeight.setter
    def overrideHeight(self, value):
        self._overrideHeight = value

    # Calculated inner dimensions
    @property
    def innerHeight(self):
        if self._overrideHeight is not None:
            padding = self.padding
            return self._overrideHeight - padding[3] - padding[1]
        else:
            return self._intrinsicInnerHeight

    @property
    def innerWidth(self):
        if self._overrideWidth is not None:
            padding = self.padding
            return self._overrideWidth - padding[3] - padding[1]
        else:
            return self._intrinsicInnerWidth

    # Calculated outer dimensions
    @property
    def outerHeight(self):
        padding = self.padding
        return padding[3] + self.innerHeight + padding[1]

    @property
    def outerWidth(self):
        padding = self.padding
        return padding[3] + self.innerWidth + padding[1]

    def getSize(self):
        return self.outerWidth, self.outerHeight
