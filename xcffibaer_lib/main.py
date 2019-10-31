'''Main setup and run loop for xcffibaer.

'''
import asyncio
import os
import sys

import xcffib
import xcffib.render
import xcffib.randr
from xcffib.randr import NotifyMask, ScreenChangeNotifyEvent

import i3ipc

from . import Bar, Store, Window, XSetup
from .atoms import initAtoms
from .timers import addDelay
from .utils import QuitApplication, inspect, printError, printInfo


DEFAULT_SCREEN_INDEX = 0

awaitingScreenChange = False


def handleWindowEvent(event):
    printInfo(f'Incoming {event.__class__.__name__}:')
    inspect(event)

    windowID = event.window if hasattr(event, 'window') else event.event
    Window.windowsByID[windowID].handleEvent(event)


def charListToString(list_):
    return ''.join(chr(c) for c in list_)


def run(theme, setupBar, setupStore, onInit=None, screen_index=DEFAULT_SCREEN_INDEX):
    conn = xcffib.connect(display=os.getenv('DISPLAY'))
    conn.randr = conn(xcffib.randr.key)
    conn.render = conn(xcffib.render.key)

    screens = conn.get_screen_pointers()

    root = conn.get_setup().roots.list[screen_index]

    initAtoms(conn)

    depthInfo = [
        d
        for d in root.allowed_depths.list
        if d.depth == 32
    ][0]

    printInfo('depthInfo:')
    inspect(depthInfo)

    visualType = [
        v
        for v in depthInfo.visuals.list
        if v._class == xcffib.xproto.VisualClass.TrueColor  # pylint: disable=protected-access
    ][0]

    printInfo('visualType:')
    inspect(visualType)

    xSetup = XSetup(conn, screens[screen_index], depthInfo, visualType, theme)

    dummy = Window(xSetup)

    printInfo('GetScreenResources:')
    screenResources = conn.randr.GetScreenResources(dummy.id).reply()
    inspect(screenResources)

    if onInit:
        onInit()

    i3conn = i3ipc.Connection()

    bars = []

    def paintBars():
        for bar in bars:
            bar.paint()

    store = Store(paintBars)
    setupStore(store, i3conn)

    wrappedI3Command = i3conn.command

    def i3Command(command):
        print(f'Sending i3 command: {repr(command)}')
        sys.stdout.flush()
        wrappedI3Command(command)

    i3conn.command = i3Command

    def setupBars():
        crtcInfoCookies = [(crtc, conn.randr.GetCrtcInfo(crtc, 0)) for crtc in screenResources.crtcs]
        for crtc, crtcInfoCookie in crtcInfoCookies:
            crtcInfo = crtcInfoCookie.reply()
            if crtcInfo.num_outputs:
                printInfo(f'Creating bar for crtc {crtc}.')

                outputs = [
                    charListToString(conn.randr.GetOutputInfo(output, 0).reply().name)
                    for output in crtcInfo.outputs
                ]
                printInfo('outputs:', outputs)
                bar = Bar(xSetup, height=21, screenExtents=crtcInfo, name=outputs[0])
                setupBar(bar, store, outputs, i3conn)
                bars.append(bar)
            else:
                print(f'(crtc {crtc} disabled)')

    setupBars()

    dummy.close()

    conn.randr.SelectInput(root.root, NotifyMask.ScreenChange)

    loop = asyncio.get_event_loop()

    def handleScreenChange():
        printInfo(f'Incoming screen change event; closing and re-creating bars.')
        while bars:
            try:
                bars.pop().close()
            except Exception as error:  # pylint: disable=broad-except
                printError(f'Unexpected {error.__class__.__name__} received while closing bar:', error)
                inspect(error)
        setupBars()
        globals()['awaitingScreenChange'] = False

    def shutdown():
        printInfo('Shutting down.')
        loop.stop()

    def xcbPoll():
        while True:
            try:
                #event = conn.wait_for_event()
                event = conn.poll_for_event()
            except xcffib.ProtocolException as error:
                printError(f'Protocol error {error.__class__.__name__} received!')
                shutdown()
                break
            except Exception as error:  # pylint: disable=broad-except
                printError(f'Unexpected {error.__class__.__name__} received:', error)
                inspect(error)
                #shutdown()
                break

            if conn.has_error():
                printError('Connection error received!')
                shutdown()
                break

            elif not event:
                break

            try:
                if isinstance(event, ScreenChangeNotifyEvent):
                    if not awaitingScreenChange:
                        printInfo(f'Incoming {event.__class__.__name__}; scheduling bar re-creation.')
                        globals()['awaitingScreenChange'] = True
                        addDelay(1, handleScreenChange)
                    else:
                        printInfo(f'Ignoring {event.__class__.__name__}; bar re-creation already scheduled.')
                else:
                    handleWindowEvent(event)
            except QuitApplication:
                shutdown()
                break

    try:
        i3conn.event_socket_setup()

        loop.add_reader(conn.get_file_descriptor(), xcbPoll)
        loop.add_reader(i3conn.sub_socket, i3conn.event_socket_poll)

        loop.run_forever()

    finally:
        i3conn.event_socket_teardown()

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        for window in Window.windowsByID.values():
            if hasattr(window, 'cleanUp') and callable(window.cleanUp):
                window.cleanUp()

    conn.disconnect()
