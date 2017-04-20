from cairocffi import (
    ImageSurface,
    OPERATOR_CLEAR,
    OPERATOR_SOURCE, OPERATOR_OVER, OPERATOR_IN, OPERATOR_OUT, OPERATOR_ATOP,
    OPERATOR_DEST, OPERATOR_DEST_OVER, OPERATOR_DEST_IN, OPERATOR_DEST_OUT, OPERATOR_DEST_ATOP,
    OPERATOR_XOR, OPERATOR_ADD, OPERATOR_SATURATE, OPERATOR_MULTIPLY,
    OPERATOR_SCREEN, OPERATOR_OVERLAY, OPERATOR_DARKEN, OPERATOR_LIGHTEN,
    OPERATOR_COLOR_DODGE, OPERATOR_COLOR_BURN, OPERATOR_HARD_LIGHT, OPERATOR_SOFT_LIGHT,
    OPERATOR_DIFFERENCE, OPERATOR_EXCLUSION, OPERATOR_HSL_HUE, OPERATOR_HSL_SATURATION,
    OPERATOR_HSL_COLOR, OPERATOR_HSL_LUMINOSITY
)

from .Chunk import Chunk


class Image(Chunk):
    OPERATOR_CLEAR = OPERATOR_CLEAR
    OPERATOR_SOURCE = OPERATOR_SOURCE
    OPERATOR_OVER = OPERATOR_OVER
    OPERATOR_IN = OPERATOR_IN
    OPERATOR_OUT = OPERATOR_OUT
    OPERATOR_ATOP = OPERATOR_ATOP
    OPERATOR_DEST = OPERATOR_DEST
    OPERATOR_DEST_OVER = OPERATOR_DEST_OVER
    OPERATOR_DEST_IN = OPERATOR_DEST_IN
    OPERATOR_DEST_OUT = OPERATOR_DEST_OUT
    OPERATOR_DEST_ATOP = OPERATOR_DEST_ATOP
    OPERATOR_XOR = OPERATOR_XOR
    OPERATOR_ADD = OPERATOR_ADD
    OPERATOR_SATURATE = OPERATOR_SATURATE
    OPERATOR_MULTIPLY = OPERATOR_MULTIPLY
    OPERATOR_SCREEN = OPERATOR_SCREEN
    OPERATOR_OVERLAY = OPERATOR_OVERLAY
    OPERATOR_DARKEN = OPERATOR_DARKEN
    OPERATOR_LIGHTEN = OPERATOR_LIGHTEN
    OPERATOR_COLOR_DODGE = OPERATOR_COLOR_DODGE
    OPERATOR_COLOR_BURN = OPERATOR_COLOR_BURN
    OPERATOR_HARD_LIGHT = OPERATOR_HARD_LIGHT
    OPERATOR_SOFT_LIGHT = OPERATOR_SOFT_LIGHT
    OPERATOR_DIFFERENCE = OPERATOR_DIFFERENCE
    OPERATOR_EXCLUSION = OPERATOR_EXCLUSION
    OPERATOR_HSL_HUE = OPERATOR_HSL_HUE
    OPERATOR_HSL_SATURATION = OPERATOR_HSL_SATURATION
    OPERATOR_HSL_COLOR = OPERATOR_HSL_COLOR
    OPERATOR_HSL_LUMINOSITY = OPERATOR_HSL_LUMINOSITY

    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)

        self.image = image

    @property
    def image(self):
        '''The displayed image.

        This can either be a filename (string), or a binary mode file-like object with a `read()` method.

        '''
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.imageSurface = ImageSurface.create_from_png(value)

    def updateIntrinsicSize(self):
        #TODO: Scaling?
        self.intrinsicInnerWidth = self.imageSurface.get_width()
        self.intrinsicInnerHeight = self.imageSurface.get_height()

    def paint(self):
        if self.chunkStyle.background:
            print('\x1b[91mPainting background: %s\x1b[m' % (self.chunkStyle.background, ))
            self.chunkStyle.background(self.context)
            self.context.paint()

        padding = self.padding
        self.context.translate(padding[3], padding[0])
        #TODO: Scaling?
        self.context.set_source_surface(self.imageSurface)

        if self.chunkStyle.operator:
            self.context.set_operator(self.chunkStyle.operator)

        self.context.paint()
