'''Graph chunk

'''
from .Chunk import Chunk


class Graph(Chunk):
    def __init__(self, maxValue, value=None, values=None, reverse=False, vertical=False, **kwargs):
        super().__init__(**kwargs)
        self.values = [value] if value is not None else values if values is not None else []
        self.maxValue = maxValue
        self.reverse = reverse
        self.vertical = vertical

    @property
    def value(self):
        return self.values[0]

    @value.setter
    def value(self, val):
        self.values = [val]

    def paint(self):
        ctx = self.beginPaint()

        if not self.reverse and self.vertical:
            ctx.translate(0, self.innerHeight)
            ctx.scale(1, -1)
        elif self.reverse and not self.vertical:
            ctx.translate(self.innerWidth, 0)
            ctx.scale(-1, 1)

        if self.chunkStyle.trough:
            self.chunkStyle.trough.paint(ctx)

        lastPos = 0
        for idx, value in enumerate(self.values):
            try:
                #fg = self.chunkStyle.foregrounds[idx] if self.chunkStyle.foregrounds else self.chunkStyle.foreground
                #barWidth = round(self.innerWidth * value / self.maxValue)
                #ctx.rectangle(lastX, 0, barWidth, self.innerHeight)
                #fg.fill(ctx)
                #lastX += barWidth
                lastPos = self.paintSection(ctx, lastPos, idx, value)
            except ValueError:
                pass

    def paintSection(self, ctx, lastPos, idx, value):
        barSize = round((self.innerHeight if self.vertical else self.innerWidth) * value / self.maxValue)
        if self.vertical:
            ctx.rectangle(0, lastPos, self.innerWidth, barSize)
        else:
            ctx.rectangle(lastPos, 0, barSize, self.innerHeight)
        foreground = self.chunkStyle.foregrounds[idx] if self.chunkStyle.foregrounds else self.chunkStyle.foreground
        foreground.fill(ctx)
        return lastPos + barSize
