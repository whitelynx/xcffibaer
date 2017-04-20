from .Chunk import Chunk


class Separator(Chunk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def paint(self):
        if self.chunkStyle.background:
            self.chunkStyle.background(self.context)
            self.context.paint()
