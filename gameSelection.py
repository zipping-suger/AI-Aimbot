from Xlib import display, X
import time
import mss
from typing import Union

# Could be do with
# from config import *
# But we are writing it out for clarity for new devs
from config import screenShotHeight, screenShotWidth

def get_all_windows():
    d = display.Display()
    root = d.screen().root
    root.change_attributes(event_mask=X.FocusChangeMask)
    windows = root.query_tree().children
    return windows

def get_window_title(window):
    window.change_attributes(event_mask=X.FocusChangeMask)
    window_title = window.get_wm_name()
    return window_title

def activate_window(window):
    window.set_input_focus(X.RevertToParent, X.CurrentTime)
    window.configure(stack_mode=X.Above)
    window.map()

def gameSelection() -> Union[tuple, None]:
    # Selecting the correct game window
    try:
        videoGameWindows = get_all_windows()
        print("=== All Windows ===")
        for index, window in enumerate(videoGameWindows):
            # only output the window if it has a meaningful title
            window_title = get_window_title(window)
            if window_title:
                print("[{}]: {}".format(index, window_title))
        # have the user select the window they want
        try:
            userInput = int(input(
                "Please enter the number corresponding to the window you'd like to select: "))
        except ValueError:
            print("You didn't enter a valid number. Please try again.")
            return None
        # "save" that window as the chosen window for the rest of the script
        videoGameWindow = videoGameWindows[userInput]
    except Exception as e:
        print("Failed to select game window: {}".format(e))
        return None

    # Activate that Window
    activationRetries = 30
    activationSuccess = False
    while (activationRetries > 0):
        try:
            activate_window(videoGameWindow)
            activationSuccess = True
            break
        except Exception as e:
            print("Failed to activate game window: {}".format(str(e)))
            print("Trying again... (you should switch to the game now)")
        # wait a little bit before the next try
        time.sleep(3.0)
        activationRetries = activationRetries - 1
    # if we failed to activate the window then we'll be unable to send input to it
    # so just exit the script now
    if activationSuccess == False:
        return None
    print("Successfully activated the game window...")

    # Starting screenshoting engine
    left = ((videoGameWindow.get_geometry().x + videoGameWindow.get_geometry().width) // 2) - (screenShotWidth // 2)
    top = videoGameWindow.get_geometry().y + \
        (videoGameWindow.get_geometry().height - screenShotHeight) // 2
    right, bottom = left + screenShotWidth, top + screenShotHeight

    region: dict = {"left": left, "top": top, "width": screenShotWidth, "height": screenShotHeight}

    # Calculating the center Autoaim box
    cWidth: int = screenShotWidth // 2
    cHeight: int = screenShotHeight // 2

    print(region)

    sct = mss.mss()

    return sct, region, cWidth, cHeight