from .Chunk import Chunk


class Graph(Chunk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def paint(self):
        if self.chunkStyle.background:
            self.chunkStyle.background(self.context)
            self.context.paint()

        padding = self.padding
        self.context.translate(padding[3], padding[0])
        #TODO: Scaling?
        self.context.set_source_surface(self.imageSurface)
        self.context.paint()
