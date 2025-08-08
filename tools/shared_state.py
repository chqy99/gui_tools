# shared_state.py - 共享状态管理
from typing import Optional
from window_manager import WindowRect

_active_window: Optional[WindowRect] = None


def get_active_window() -> Optional[WindowRect]:
    """获取当前激活窗口"""
    global _active_window
    return _active_window


def set_active_window(window_rect: WindowRect):
    """设置当前激活窗口"""
    global _active_window
    _active_window = window_rect


def clear_active_window():
    """清除当前激活窗口"""
    global _active_window
    _active_window = None