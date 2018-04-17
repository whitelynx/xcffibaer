from .Chunk import Chunk


class Graph(Chunk):
    def __init__(self, maxValue, value=None, values=[], align='right', **kwargs):
        super().__init__(**kwargs)
        self.values = [value] if value is not None else values
        self.maxValue = maxValue
        self.align = align

    @property
    def value(self):
        return self.values[0]

    @value.setter
    def value(self, val):
        self.values = [val]

    def paint(self):
        ctx = self.context
        padding = self.padding

        if self.chunkStyle.background:
            self.chunkStyle.background(ctx)
            ctx.paint()

        ctx.translate(padding[3], padding[0])
        ctx.rectangle(0, 0, self.innerWidth, self.innerHeight)
        ctx.clip()

        if self.align == 'left':
            ctx.translate(self.innerWidth, 0)
            ctx.scale(-1, 1)

        if self.chunkStyle.trough:
            self.chunkStyle.trough(ctx)
            ctx.paint()

        if self.chunkStyle.foregrounds:
            # TODO: Horizontal/vertical?
            lastX = 0
            for idx, value in enumerate(self.values):
                try:
                    barWidth = round(self.innerWidth * value / self.maxValue)
                    ctx.rectangle(lastX, 0, barWidth, self.innerHeight)
                    self.chunkStyle.foregrounds[idx](ctx)
                    ctx.fill()
                    lastX += barWidth
                except ValueError:
                    pass
        elif self.chunkStyle.foreground:
            # TODO: Horizontal/vertical?
            barWidth = round(self.innerWidth * self.value / self.maxValue)
            ctx.rectangle(0, 0, barWidth, self.innerHeight)
            self.chunkStyle.foreground(ctx)
            ctx.fill()
