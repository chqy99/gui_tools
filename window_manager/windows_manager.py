import win32gui
import win32con
import win32ui
import mss
from typing import Optional, List
from PIL import Image
from .base_manager import BaseWindowManager, WindowInfo, WindowRect


class WindowsWindowManager(BaseWindowManager):
    def __init__(self):
        self._windows_cache: List[WindowInfo] = self.list_windows()

    def list_windows(self) -> List[WindowInfo]:
        windows: List[WindowInfo] = []

        def _enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    rect = WindowRect(
                        left=left,
                        top=top,
                        width=right - left,
                        height=bottom - top
                    )
                    windows.append(WindowInfo(
                        id=str(hwnd),
                        title=title,
                        index=0,  # 临时，后面加索引
                        rect=rect
                    ))

        win32gui.EnumWindows(_enum_handler, None)

        # 给同名窗口添加 index
        title_count = {}
        for w in windows:
            t = w.title
            title_count[t] = title_count.get(t, -1) + 1
            w.index = title_count[t]

        self._windows_cache = windows
        return windows

    def _find_window(self, title: str, index: int = 0) -> Optional[WindowInfo]:
        for w in self._windows_cache:
            if w.title == title and w.index == index:
                return w
        return None

    def focus_window(self, title: str, index: int = 0):
        win = self._find_window(title, index)
        if win:
            win32gui.SetForegroundWindow(int(win.id))

    def get_active_window(self) -> Optional[WindowInfo]:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        rect = WindowRect(left, top, right - left, bottom - top)

        # 找出索引
        index = 0
        for w in self._windows_cache:
            if w.title == title and int(w.id) == hwnd:
                index = w.index
                break

        return WindowInfo(id=str(hwnd), title=title, index=index, rect=rect)

    def resize_window(self, title: str, width: int, height: int, index: int = 0):
        win = self._find_window(title, index)
        if win:
            win32gui.MoveWindow(int(win.id), win.rect.left, win.rect.top, width, height, True)

    def move_window(self, title: str, x: int, y: int, index: int = 0):
        win = self._find_window(title, index)
        if win:
            win32gui.MoveWindow(int(win.id), x, y, win.rect.width, win.rect.height, True)

    def capture_window(self, title: str, index: int = 0) -> Optional[Image.Image]:
        """用 mss 给窗口截图"""
        win = self._find_window(title, index)
        if not win:
            return None

        rect_dict = {
            "left": win.rect.left,
            "top": win.rect.top,
            "width": win.rect.width,
            "height": win.rect.height
        }

        with mss.mss() as sct:
            sct_img = sct.grab(rect_dict)

        # 转成 PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img
