'''Switcher chunk

'''
from .Chunk import Chunk
from .Text import Text


class Switcher(Chunk):
    def __init__(self, choices=None, choiceStylePrefix='choice', onChoiceClick=None, **kwargs):
        super().__init__(**kwargs)
        self._choices = []
        self.choiceChunks = []
        self.chunkExtents = {}

        self.choiceStylePrefix = choiceStylePrefix
        self.choices = choices if choices is not None else []
        self.onChoiceClick = onChoiceClick

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, choices):
        if len(choices) != len(self._choices):
            self.choiceChunks = [Text(choice) for choice in choices]
        self._choices = choices

        for choice, chunk in zip(choices, self.choiceChunks):
            chunk.choice = choice
            chunk.text = choice['name']
            chunk.styles = [self.choiceStylePrefix]
            if choice['visible']:
                chunk.styles.append(f'{self.choiceStylePrefix}-visible')
            if choice['urgent']:
                chunk.styles.append(f'{self.choiceStylePrefix}-urgent')
            if choice['focused']:
                chunk.styles.append(f'{self.choiceStylePrefix}-focused')

            if self.theme is not None:
                chunk.setTheme(self.theme)

    def setTheme(self, theme):
        super().setTheme(theme)
        for chunk in self.choiceChunks:
            chunk.setTheme(theme)

    def updateIntrinsicSize(self):
        self.intrinsicInnerWidth = sum(chunk.outerWidth for chunk in self.choiceChunks)
        self.intrinsicInnerHeight = max(chunk.outerHeight for chunk in self.choiceChunks)

    def paint(self):
        ctx = self.beginPaint()

        chunkExtents = {}

        lastX = 0
        for chunk in self.choiceChunks:
            with ctx:
                chunk.setContext(ctx)

                width, height = chunk.getSize()
                chunkExtents[chunk] = (lastX, lastX + width)

                ctx.rectangle(lastX, 0, width, height)
                ctx.clip()
                ctx.translate(lastX, 0)

                chunk.paint()

                lastX += chunk.outerWidth

        self.chunkExtents = chunkExtents

    def onClick(self, event, clickX, clickY):
        for chunk, (startX, endX) in self.chunkExtents.items():
            if startX <= event.event_x < endX:
                self.onChoiceClick(chunk.choice)
                return
