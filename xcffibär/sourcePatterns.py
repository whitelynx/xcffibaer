'''Cairo source pattern definitions

'''
import re

longHexColorRE = re.compile(r'^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})?$')
shortHexColorRE = re.compile(r'^#?([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])?$')


def parseColorString(colorString):
    match = longHexColorRE.match(colorString)
    if match:
        return tuple(int(c, 16) / 255.0 for c in match.groups() if c is not None)
    else:
        match = shortHexColorRE.match(colorString)
        if match:
            return tuple(int(c, 16) / 15.0 for c in match.groups() if c is not None)
        else:
            raise ValueError("Couldn't parse hex color string!")


class Color(object):
    def __init__(self, *someColor):
        if len(someColor) == 1:
            someColor = someColor[0]

        if isinstance(someColor, str):
            someColor = parseColorString(someColor)

        if isinstance(someColor, tuple):
            if len(someColor) == 3:
                self.hasAlpha = False
            elif len(someColor) == 4:
                self.hasAlpha = True
            else:
                raise ValueError('Tuple colors must have either 3 or 4 components!')

            if all(isinstance(c, float) for c in someColor):
                self.components = someColor
            elif all(isinstance(c, int) for c in someColor):
                self.components = tuple(c / 255.0 for c in someColor)
            else:
                raise ValueError('Tuple colors must be either all floats or all ints!')

        else:
            raise ValueError('Unrecognized color input! Should be a tuple or a hex string.')

    def __call__(self, context):
        if self.hasAlpha:
            context.set_source_rgba(*self.components)
        else:
            context.set_source_rgb(*self.components)

    def __repr__(self):
        return 'Color' + repr(self.components)

    def __str__(self):
        return '#' + ''.join(hex(int(c * 255))[2:].rjust(2, '0') for c in self.components)


if __name__ == '__main__':
    def test(expr):
        print('{}: {}'.format(expr, eval(expr)))  # pylint: disable=eval-used

    test('Color("abc")')
    test('Color("abcd")')
    test('Color("08f")')
    test('Color("aabbcc")')
    test('Color("aabbccdd")')
    test('Color("007fff")')
    test('Color("0080ff")')
    test('Color("#abc")')
    test('Color("#abcd")')
    test('Color("#08f")')
    test('Color("#aabbcc")')
    test('Color("#aabbccdd")')
    test('Color("#007fff")')
    test('Color("#0080ff")')
    test('Color(1.0, 0.0, 1.0)')
    test('Color(255, 0, 255)')
    test('Color((1.0, 0.0, 1.0))')
    test('Color((255, 0, 255))')
