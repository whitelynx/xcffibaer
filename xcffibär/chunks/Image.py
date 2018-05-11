'''Image chunk

'''
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

    def __init__(self, image=None, **kwargs):
        super().__init__(**kwargs)

        self._image = None
        self._styleImage = None
        self.imageSurface = None

        self.image = image

    @property
    def image(self):
        '''The displayed image as explicitly defined in the constructor.

        This can either be a filename (string), or a binary mode file-like object with a `read()` method.

        '''
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self._makeImageSurface()

    @property
    def styleImage(self):
        '''The displayed image as defined by the style.

        This can either be a filename (string), or a binary mode file-like object with a `read()` method.

        '''
        return self._styleImage

    @styleImage.setter
    def styleImage(self, value):
        self._styleImage = value
        self._makeImageSurface()

    def _makeImageSurface(self):
        image = self._image if self._image is not None else self._styleImage
        if image is not None:
            self.imageSurface = ImageSurface.create_from_png(image)
        else:
            self.imageSurface = None

    def applyStyle(self, chunkStyle):
        super().applyStyle(chunkStyle)

        self.styleImage = chunkStyle.image

    def updateIntrinsicSize(self):
        #TODO: Scaling?
        self.intrinsicInnerWidth = self.imageSurface.get_width()
        self.intrinsicInnerHeight = self.imageSurface.get_height()

    def paint(self):
        ctx = self.beginPaint()
        #TODO: Scaling?

        if self.chunkStyle.operator:
            ctx.set_operator(self.chunkStyle.operator)

        if self.chunkStyle.foreground:
            self.chunkStyle.foreground(ctx)
            ctx.mask_surface(self.imageSurface)
        else:
            ctx.set_source_surface(self.imageSurface)
            ctx.paint()
