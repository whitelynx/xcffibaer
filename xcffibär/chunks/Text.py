'''Text chunk

'''
from ..pangocffi import CairoContext, ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT

from .Chunk import Chunk


usePangoCairo = True


stylePropMapping = {
    #'font': 'font',
    'fontFamily': 'font_family',
    #'fontSize': 'font_size',
    'fontSize': 'font',
    'fontStyle': 'font_style',
    'fontWeight': 'font_weight',
    'fontVariant': 'font_variant',
    'fontStretch': 'font_stretch',
    'fontFeatures': 'font_features',
    'foreground': 'foreground',
    'alpha': 'alpha',
    #'background': 'background',
    #'backgroundAlpha': 'background_alpha',
    'underline': 'underline',
    'underlineColor': 'underline_color',
    'rise': 'rise',
    'strikethrough': 'strikethrough',
    'strikethroughColor': 'strikethrough_color',
    'fallback': 'fallback',
    'lang': 'lang',
    'letterSpacing': 'letter_spacing',
    'gravity': 'gravity',
    'gravityHint': 'gravity_hint',
}


class Text(Chunk):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self._text = None
        self._formattedText = None
        self.layout = None

        self.textFormat = '%s'
        self.text = text

    @property
    def text(self):
        '''The displayed text.

        This supports Pango markup, as described at: https://developer.gnome.org/pango/stable/PangoMarkupFormat.html

        '''
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._formattedText = self.textFormat % (self.text, )

    def applyStyle(self, chunkStyle):
        '''
        TODO: Implement support for these pango markup <span> attributes:
            font, font_desc             A font description string, such as "Sans Italic 12". See
                                          pango_font_description_from_string() for a description of the format of the
                                          string representation . Note that any other span attributes will override
                                          this description. So if you have "Sans Italic" and also a style="normal"
                                          attribute, you will get Sans normal, not italic.
            font_family, face           A font family name
            font_size, size             Font size in 1024ths of a point, or one of the absolute sizes 'xx-small',
                                          'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', or one of the
                                          relative sizes 'smaller' or 'larger'. If you want to specify a absolute size,
                                          it's usually easier to take advantage of the ability to specify a partial
                                          font description using 'font'; you can use font='12.5' rather than
                                          size='12800'.
            font_style, style           One of 'normal', 'oblique', 'italic'
            font_weight, weight         One of 'ultralight', 'light', 'normal', 'bold', 'ultrabold', 'heavy', or a
                                          numeric weight
            font_variant, variant       One of 'normal' or 'smallcaps'
            font_stretch, stretch       One of 'ultracondensed', 'extracondensed', 'condensed', 'semicondensed',
                                          'normal', 'semiexpanded', 'expanded', 'extraexpanded', 'ultraexpanded'
            font_features               A comma separated list of OpenType font feature settings, in the same syntax
                                          as accepted by CSS. E.g: font_features='dlig=1, -kern, afrc on'
            foreground, fgcolor, color  An RGB color specification such as '#00FF00' or a color name such as 'red'.
                                          Since 1.38, an RGBA color specification such as '#00FF007F' will be
                                          interpreted as specifying both a foreground color and foreground alpha.
            background, bgcolor         An RGB color specification such as '#00FF00' or a color name such as 'red'.
                                          Since 1.38, an RGBA color specification such as '#00FF007F' will be
                                          interpreted as specifying both a background color and background alpha.
            alpha, fgalpha              An alpha value for the foreground color, either a plain integer between 1 and
                                          65536 or a percentage value like '50%'.
            background_alpha, bgalpha   An alpha value for the background color, either a plain integer between 1 and
                                          65536 or a percentage value like '50%'.
            underline                   One of 'none', 'single', 'double', 'low', 'error'
            underline_color             The color of underlines; an RGB color specification such as '#00FF00' or a
                                          color name such as 'red'
            rise                        Vertical displacement, in Pango units. Can be negative for subscript,
                                          positive for superscript.
            strikethrough               'true' or 'false' whether to strike through the text
            strikethrough_color         The color of strikethrough lines; an RGB color specification such as
                                          '#00FF00' or a color name such as 'red'
            fallback                    'true' or 'false' whether to enable fallback. If disabled, then characters
                                          will only be used from the closest matching font on the system. No fallback
                                          will be done to other fonts on the system that might contain the characters
                                          in the text. Fallback is enabled by default. Most applications should not
                                          disable fallback.
            lang                        A language code, indicating the text language
            letter_spacing              Inter-letter spacing in 1024ths of a point.
            gravity                     One of 'south', 'east', 'north', 'west', 'auto'.
            gravity_hint                One of 'natural', 'strong', 'line'.
        '''
        super().applyStyle(chunkStyle)

        props = []
        for styleKey, attribName in stylePropMapping.items():
            try:
                val = getattr(chunkStyle, styleKey)
                if val is not None:
                    props.append('%s="%s"' % (attribName, val))
            except AttributeError:
                pass

        if props:
            self.textFormat = '<span %s>%%s</span>' % (' '.join(props), )
        else:
            self.textFormat = '%s'

        self._formattedText = self.textFormat % (self.text, )

    def setContext(self, context):
        if usePangoCairo:
            context = CairoContext(context)

        if usePangoCairo:
            self.layout = context.create_layout()
            self.layout.set_markup(self.textFormat % (self.text, ))
            #print('printing text: \x1b[32m%r\x1b[m' % (self.textFormat % (self.text, ), ))

        else:
            if self.chunkStyle.fontFamily:
                context.select_font_face(self.chunkStyle.fontFamily)

            context.set_font_size(self.chunkStyle.fontSize)

        super().setContext(context)

    def updateIntrinsicSize(self):
        if usePangoCairo:
            width, height = self.layout.get_pixel_size()
        else:
            _xBearing, _yBearing, width, height, _xAdvance, _yAdvance = self.context.text_extents(self.text)

        self.intrinsicInnerWidth, self.intrinsicInnerHeight = width, height

    def paint(self):
        ctx = self.beginPaint()

        self.chunkStyle.foreground(ctx)
        if usePangoCairo:
            ctx.move_to(0, 0)
            ctx.show_layout(self.layout)
        else:
            ctx.move_to(0, self.innerHeight)
            ctx.show_text(self.text)


__all__ = ['Text', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT']
