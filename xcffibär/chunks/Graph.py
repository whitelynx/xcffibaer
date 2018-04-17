from .Chunk import Chunk


class Graph(Chunk):
    def __init__(self, value, maxValue, align='right', **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.maxValue = maxValue
        self.align = align

    def paint(self):
        if self.chunkStyle.background:
            self.chunkStyle.background(self.context)
            self.context.paint()

        padding = self.padding
        self.context.translate(padding[3], padding[0])

        if self.chunkStyle.trough:
            self.context.rectangle(0, 0, self.innerWidth, self.innerHeight)
            self.chunkStyle.trough(self.context)
            self.context.fill()

        if self.chunkStyle.foreground:
            # TODO: Horizontal/vertical?
            barWidth = round(self.innerWidth * self.value / self.maxValue)
            self.context.rectangle(
                0 if self.align == 'left' else self.innerWidth - barWidth, 0,
                barWidth, self.innerHeight
            )
            self.chunkStyle.foreground(self.context)
            self.context.fill()
