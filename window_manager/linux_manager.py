import subprocess
import re
from typing import List, Optional
import mss
from PIL import Image
from .base_manager import BaseWindowManager, WindowInfo, WindowRect
from dataclasses import dataclass


class LinuxWindowManager(BaseWindowManager):
    """Linux 平台的 WindowManager 实现（依赖 wmctrl + xdotool + xprop）"""

    def list_windows(self) -> List[WindowInfo]:
        """返回所有窗口信息"""
        try:
            output = subprocess.check_output(["wmctrl", "-lG"]).decode("utf-8")
        except FileNotFoundError:
            raise RuntimeError("请先安装 wmctrl (sudo apt install wmctrl)")

        windows = []
        for line in output.strip().split("\n"):
            parts = line.split(None, 7)
            if len(parts) >= 8:
                win_id, _, x, y, w, h, _, title = parts
                rect = WindowRect(
                    left=int(x),
                    top=int(y),
                    width=int(w),
                    height=int(h)
                )
                windows.append(WindowInfo(
                    id=win_id,
                    title=title.strip(),
                    index=0,  # 临时，后面会重新计算
                    rect=rect
                ))
        # 给同名窗口添加 index
        title_count = {}
        for w in windows:
            t = w.title
            title_count[t] = title_count.get(t, -1) + 1
            w.index = title_count[t]

        return windows

    def focus_window(self, title: str, index: int = 0):
        """根据窗口标题聚焦窗口（支持同名窗口用 index 区分）"""
        windows = [w for w in self.list_windows() if title in w.title]
        if not windows:
            raise ValueError(f"未找到标题包含 '{title}' 的窗口")
        if index >= len(windows):
            raise ValueError(f"窗口索引超出范围: {index}")
        win_id = windows[index].id
        subprocess.run(["wmctrl", "-ia", win_id])

    def get_active_window(self) -> Optional[WindowInfo]:
        """返回当前活动窗口信息"""
        try:
            active_id = subprocess.check_output(
                ["xdotool", "getactivewindow"]
            ).decode("utf-8").strip()
        except FileNotFoundError:
            raise RuntimeError("请先安装 xdotool (sudo apt install xdotool)")

        for w in self.list_windows():
            if int(w.id, 16) == int(active_id):
                return w
        return None

    def resize_window(self, title: str, width: int, height: int, index: int = 0):
        """调整窗口大小"""
        windows = [w for w in self.list_windows() if title in w.title]
        if not windows:
            raise ValueError(f"未找到标题包含 '{title}' 的窗口")
        if index >= len(windows):
            raise ValueError(f"窗口索引超出范围: {index}")
        win_id = windows[index].id
        subprocess.run(["wmctrl", "-ir", win_id, "-e", f"0,{windows[index].rect.left},{windows[index].rect.top},{width},{height}"])

    def move_window(self, title: str, x: int, y: int, index: int = 0):
        """移动窗口"""
        windows = [w for w in self.list_windows() if title in w.title]
        if not windows:
            raise ValueError(f"未找到标题包含 '{title}' 的窗口")
        if index >= len(windows):
            raise ValueError(f"窗口索引超出范围: {index}")
        win_id = windows[index].id
        subprocess.run(["wmctrl", "-ir", win_id, "-e", f"0,{x},{y},{windows[index].rect.width},{windows[index].rect.height}"])

    def capture_window(self, title: str, index: int = 0):
        """给窗口截图"""
        windows = [w for w in self.list_windows() if title in w.title]
        if not windows:
            raise ValueError(f"未找到标题包含 '{title}' 的窗口")
        if index >= len(windows):
            raise ValueError(f"窗口索引超出范围: {index}")
        w = windows[index]
        rect = w.rect.to_dict()

        with mss.mss() as sct:
            sct_img = sct.grab(rect)

        # BGRX -> RGB
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")