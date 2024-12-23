import sys
import time
import ctypes
from ctypes.util import find_library

libX11 = ctypes.CDLL(find_library("X11"))

# Typedefs for better readability
X11TypeWindow = ctypes.c_ulong
X11TypeAtom = ctypes.c_ulong
X11TypeDisplay = ctypes.c_int64
X11TypeStatus = ctypes.c_int

XA_CARDINAL = 6
X11_SUCCESS = 0
RevertToPointerRoot = 1
CurrentTime = 0

# Function prototypes
libX11.XOpenDisplay.argtypes = [ctypes.c_char_p]
#libX11.XOpenDisplay.restype = X11TypeDisplay

libX11.XInternAtom.argtypes = [X11TypeDisplay, ctypes.c_char_p, ctypes.c_bool]
libX11.XInternAtom.restype = X11TypeAtom

libX11.XDefaultRootWindow.argtypes = [X11TypeDisplay]
libX11.XDefaultRootWindow.restype = X11TypeWindow

libX11.XQueryTree.argtypes = [
    X11TypeDisplay,
    X11TypeWindow,
    ctypes.POINTER(X11TypeWindow),
    ctypes.POINTER(X11TypeWindow),
    ctypes.POINTER(ctypes.POINTER(X11TypeWindow)),
    ctypes.POINTER(ctypes.c_uint)
]
libX11.XQueryTree.restype = X11TypeStatus

libX11.XGetWindowProperty.argtypes = [
    X11TypeDisplay,
    X11TypeWindow,
    X11TypeAtom,
    ctypes.c_long,
    ctypes.c_long,
    ctypes.c_bool,
    X11TypeAtom,
    ctypes.POINTER(X11TypeAtom),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_ulong),
    ctypes.POINTER(ctypes.c_ulong),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))
]
libX11.XGetWindowProperty.restype = X11TypeStatus

libX11.XFree.argtypes = [ctypes.c_void_p]
libX11.XFree.restype = ctypes.c_int

libX11.XRaiseWindow.argtypes = [X11TypeDisplay, X11TypeWindow]
libX11.XRaiseWindow.restype = None

libX11.XSetInputFocus.argtypes = [X11TypeDisplay, X11TypeWindow, ctypes.c_int, ctypes.c_int64]
libX11.XSetInputFocus.restype = None

libX11.XCloseDisplay.argtypes = [X11TypeDisplay]
libX11.XCloseDisplay.restype = None


def get_window_pid(display, window):
    pid_atom = libX11.XInternAtom(display, b"_NET_WM_PID", True)
    if pid_atom == 0:
        return None

    actual_type = X11TypeAtom()
    actual_format = ctypes.c_int()
    num_items = ctypes.c_ulong()
    bytes_after = ctypes.c_ulong()
    prop_pid = ctypes.POINTER(ctypes.c_ubyte)()

    status = libX11.XGetWindowProperty(
        display, window, pid_atom, 0, 1, False, XA_CARDINAL,
        ctypes.byref(actual_type), ctypes.byref(actual_format),
        ctypes.byref(num_items), ctypes.byref(bytes_after),
        ctypes.byref(prop_pid)
    )

    if status != X11_SUCCESS or num_items.value == 0:
        return None

    pid = ctypes.cast(prop_pid, ctypes.POINTER(ctypes.c_ulong)).contents.value
    libX11.XFree(prop_pid)

    return pid


def find_window_by_pid(display, root, pid):
    returned_root = X11TypeWindow()
    returned_parent = X11TypeWindow()
    top_level_windows = ctypes.POINTER(X11TypeWindow)()
    num_top_level_windows = ctypes.c_uint()

    status = libX11.XQueryTree(
        display, root,
        ctypes.byref(returned_root),
        ctypes.byref(returned_parent),
        ctypes.byref(top_level_windows),
        ctypes.byref(num_top_level_windows)
    )

    if status == 0:
        return None

    for i in range(num_top_level_windows.value):
        window_pid = get_window_pid(display, top_level_windows[i])
        if window_pid == pid:
            return top_level_windows[i]

        child_window = find_window_by_pid(display, top_level_windows[i], pid)
        if child_window:
            return child_window

    libX11.XFree(top_level_windows)
    return None


def main():
    display = libX11.XOpenDisplay(None)
    if not display:
        print("Unable to open display")
        return

    root = libX11.XDefaultRootWindow(display)
    if not root:
        print("Unable to get root window")
        return

    pid = 56422  # Replace with the target PID
    target_window = find_window_by_pid(display, root, pid)

    if target_window:
        print(f"Window ID for PID {pid}: {target_window} {display}")
        libX11.XRaiseWindow(display, target_window)
        libX11.XSetInputFocus(display, target_window, RevertToPointerRoot, 0)
    else:
        print(f"No window found for PID {pid}")

    libX11.XCloseDisplay(display)


if __name__ == "__main__":
    main()
