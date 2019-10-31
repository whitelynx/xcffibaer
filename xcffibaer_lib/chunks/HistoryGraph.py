'''History graph chunk

'''
from .Chunk import Chunk


class HistoryGraph(Chunk):
    def __init__(self, maxValue, value=None, values=None, reverse=False, flip=False, **kwargs):
        super().__init__(**kwargs)

        self._graphs = None
        self.valueHistory = []
        self.values = [value] if value is not None else values if values is not None else []
        self.maxValue = maxValue
        self.reverse = reverse
        self.flip = flip

    @property
    def value(self):
        return self.values[0]

    @value.setter
    def value(self, val):
        self.values = [val]

    @property
    def values(self):
        return self.valueHistory[0]

    @values.setter
    def values(self, values):
        self.valueHistory.insert(0, values)
        self.valueHistory = [values] + self.valueHistory[:self.innerWidth if self.chunkStyle else 10]

    def paint(self):
        ctx = self.beginPaint()

        if self.chunkStyle.trough:
            self.chunkStyle.trough.paint(ctx)

        if self.reverse:
            ctx.translate(self.innerWidth, 0)
            ctx.scale(-1, 1)

        if not self.flip:
            ctx.translate(0, self.innerHeight)
            ctx.scale(1, -1)

        for barIdx in range(self.innerWidth):
            self.paintBar(ctx, barIdx)
            ctx.translate(1, 0)

    def paintBar(self, ctx, barIdx):
        try:
            values = self.valueHistory[barIdx]
        except IndexError:
            values = []

        lastPos = 0
        for idx, value in enumerate(values):
            try:
                lastPos = self.paintSection(ctx, lastPos, idx, value)
            except ValueError:
                pass

    def paintSection(self, ctx, lastPos, idx, value):
        barSize = round(self.innerHeight * value / self.maxValue)
        if barSize == 0:
            # Bar is too small to display; skip.
            return lastPos

        ctx.rectangle(0, lastPos, 1, barSize)
        foreground = self.chunkStyle.foregrounds[idx] if self.chunkStyle.foregrounds else self.chunkStyle.foreground
        foreground.fill(ctx)

        return lastPos + barSize
