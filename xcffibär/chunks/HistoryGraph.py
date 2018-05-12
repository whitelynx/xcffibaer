'''History graph chunk

'''
from .Chunk import Chunk
from .Graph import Graph
from ..Theme import ChunkStyle


class HistoryGraph(Chunk):
    def __init__(self, maxValue, value=None, values=None, reverse=False, **kwargs):
        super().__init__(**kwargs)

        self._graphs = None
        self.values = [value] if value is not None else values if values is not None else []
        self.maxValue = maxValue
        self.reverse = reverse

    @property
    def graphs(self):
        if self._graphs is None:
            # TODO: Actually get a real style here!
            graphStyle = ChunkStyle({})

            self._graphs = [
                Graph(maxValue=self.maxValue, width=1, height=self.innerHeight, vertical=True)
                for idx in range(self.innerWidth)
            ]
            for graph in self._graphs:
                graph.applyStyle(graphStyle)

        return self._graphs

    @property
    def value(self):
        return self.values[0]

    @value.setter
    def value(self, val):
        self.values = [val]

    @property
    def values(self):
        return self.graphs[0].values

    @values.setter
    def values(self, values):
        for idx, graph in enumerate(self._graphs or []):
            graph.values = self.graphs[idx + 1].values if idx + 1 < len(self.graphs) else values

    def paint(self):
        ctx = self.beginPaint()

        for idx, graph in enumerate(self.graphs):
            ctx.translate(self.innerWidth - idx, 0)
            ctx.rectangle(0, 0, 1, self.innerHeight)
            ctx.clip()
            graph.setContext(ctx)
