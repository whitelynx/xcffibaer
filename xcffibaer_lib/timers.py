'''Timer functions

'''
import asyncio
import time


def addDelay(delay, callback):
    async def _job():
        await asyncio.sleep(delay)
        callback()
    asyncio.ensure_future(_job())


def addInterval(delay, callback):
    async def _job():
        while True:
            await asyncio.sleep(delay)
            callback()
    asyncio.ensure_future(_job())


def addDeadline(targetTime, callback):
    currentTime = time.monotonic()
    addDelay(max(targetTime - currentTime, 0), callback)


def addImmediate(callback):
    addDelay(0, callback)
