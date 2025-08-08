# tools/__init__.py - 工具注册模块
from .gui_query import (
    list_windows,
    get_active_window_info,
    get_window_info,
    activate_window,
    get_current_active_window,
)

from .gui_action import (
    click_at,
    move_mouse,
    double_click_at,
    right_click_at,
    middle_click_at,
    drag_to,
    scroll_mouse,
    type_text,
    press_key,
    hotkey,
    screenshot_current_window,
    resize_window,
    move_window,
    capture_window,
)

# 所有可用的工具列表
TOOLS = [
    # 查询类工具
    list_windows,
    get_active_window_info,
    get_window_info,
    activate_window,
    get_current_active_window,

    # 操作类工具
    click_at,
    move_mouse,
    double_click_at,
    right_click_at,
    middle_click_at,
    drag_to,
    scroll_mouse,
    type_text,
    press_key,
    hotkey,
    screenshot_current_window,
    resize_window,
    move_window,
    capture_window,
]

__all__ = [
    "TOOLS",
    # 查询类工具
    "list_windows",
    "get_active_window_info",
    "get_window_info",
    "activate_window",
    "get_current_active_window",
    # 操作类工具
    "click_at",
    "move_mouse",
    "double_click_at",
    "right_click_at",
    "middle_click_at",
    "drag_to",
    "scroll_mouse",
    "type_text",
    "press_key",
    "hotkey",
    "screenshot_current_window",
    "resize_window",
    "move_window",
    "capture_window",
]