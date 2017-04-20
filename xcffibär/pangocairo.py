import cairocffi
import cffi


ffi = cffi.FFI()
ffi.include(cairocffi.ffi)
ffi.cdef('''
    /* GLib */
    typedef void* gpointer;
    void g_object_unref (gpointer object);

    /* Pango and PangoCairo */
    typedef ... PangoLayout;
    typedef enum {
        PANGO_ALIGN_LEFT,
        PANGO_ALIGN_CENTER,
        PANGO_ALIGN_RIGHT
    } PangoAlignment;
    int pango_units_from_double (double d);
    PangoLayout * pango_cairo_create_layout (cairo_t *cr);
    void pango_cairo_show_layout (cairo_t *cr, PangoLayout *layout);
    void pango_layout_set_width (PangoLayout *layout, int width);
    void pango_layout_set_alignment (PangoLayout *layout, PangoAlignment alignment);
    void pango_layout_set_markup (PangoLayout *layout, const char *text, int length);
    void pango_layout_get_pixel_size (PangoLayout *layout, int *width, int *height);
''')
gobject = ffi.dlopen('gobject-2.0')
pango = ffi.dlopen('pango-1.0')
pangocairo = ffi.dlopen('pangocairo-1.0')

units_from_double = pango.pango_units_from_double

ALIGN_LEFT = pango.PANGO_ALIGN_LEFT
ALIGN_CENTER = pango.PANGO_ALIGN_CENTER
ALIGN_RIGHT = pango.PANGO_ALIGN_RIGHT


def gObjectRef(pointer):
    return ffi.gc(pointer, gobject.g_object_unref)


def layoutText(context, text, alignment=ALIGN_CENTER, wrapWidth=None):
    layout = gObjectRef(pangocairo.pango_cairo_create_layout(context._pointer))

    pango.pango_layout_set_alignment(layout, alignment)

    if wrapWidth is not None:
        pango.pango_layout_set_width(layout, units_from_double(wrapWidth))

    markup = ffi.new('char[]', text.encode('utf8'))
    pango.pango_layout_set_markup(layout, markup, -1)

    return layout


def getTextLayoutSize(context, layout):
    width = ffi.new("int*")
    height = ffi.new("int*")
    pango.pango_layout_get_pixel_size(layout, width, height)

    return width[0], height[0]


def showTextLayout(context, layout):
    pangocairo.pango_cairo_show_layout(context._pointer, layout)


if __name__ == '__main__':
    def writeExamplePDF(target):
        pt_per_mm = 72 / 25.4
        width, height = 210 * pt_per_mm, 297 * pt_per_mm  # A4 portrait
        surface = cairocffi.PDFSurface(target, width, height)
        context = cairocffi.Context(surface)
        context.translate(0, 300)
        context.rotate(-0.2)

        layout = layoutText(context, '<span font="italic 30">Hi from Παν語!</span>', wrapWidth=width)
        showTextLayout(context, layout)

    writeExamplePDF(target='pango_example.pdf')
