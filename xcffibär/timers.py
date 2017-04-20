import time


sortedTimers = []


def addDelay(delay, callback):
    currentTime = time.monotonic()
    addDeadline(currentTime + delay, callback)


def addInterval(delay, callback):
    def callbackWrapper():
        addDelay(delay, callbackWrapper)
        callback()

    addDelay(delay, callbackWrapper)


def addDeadline(targetTime, callback):
    for i, (currTargetTime, currCallback) in enumerate(sortedTimers):
        if currTargetTime < targetTime:
            sortedTimers.insert(i, (targetTime, callback))
            return

    # We only get here if `targetTime` is less than for any already-registered timer. (or if there are no timers)
    sortedTimers.append((targetTime, callback))


def addImmediate(callback):
    sortedTimers.append((time.monotonic(), callback))


def triggerElapsedTimers():
    currentTime = time.monotonic()

    while sortedTimers and sortedTimers[-1][0] < currentTime:
        targetTime, callback = sortedTimers.pop()
        callback()
