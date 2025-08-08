# pyautogui_wrapper.py
import pyautogui
from typing import Optional
from gui_tools.window_manager.base_manager import WindowRect


class PyAutoGUIWrapper:
    def __init__(self, window_rect: Optional[WindowRect] = None):
        self.window_rect = window_rect

    def _to_absolute(self, x: int, y: int, relative: bool = True):
        if relative and self.window_rect:
            return self.window_rect.left + x, self.window_rect.top + y
        return x, y

    # 鼠标操作
    def move_to(self, x: int, y: int, relative=True):
        ax, ay = self._to_absolute(x, y, relative)
        pyautogui.moveTo(ax, ay)

    def click(self, x: Optional[int] = None, y: Optional[int] = None, relative=True):
        if x is not None and y is not None:
            self.move_to(x, y, relative)
        pyautogui.click()

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None, relative=True):
        if x is not None and y is not None:
            self.move_to(x, y, relative)
        pyautogui.doubleClick()

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None, relative=True):
        if x is not None and y is not None:
            self.move_to(x, y, relative)
        pyautogui.rightClick()

    def middle_click(self, x: Optional[int] = None, y: Optional[int] = None, relative=True):
        if x is not None and y is not None:
            self.move_to(x, y, relative)
        pyautogui.middleClick()

    def drag_to(self, x: int, y: int, duration=0.5, relative=True):
        ax, ay = self._to_absolute(x, y, relative)
        pyautogui.dragTo(ax, ay, duration=duration)

    def scroll(self, clicks: int):
        pyautogui.scroll(clicks)

    # 键盘操作
    def type_text(self, text: str, interval=0.05):
        pyautogui.typewrite(text, interval=interval)

    def press_key(self, key: str):
        pyautogui.press(key)

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)

