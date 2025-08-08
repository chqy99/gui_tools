# gui_query.py - 查询类工具函数
from langchain_core.tools import tool
from typing import List, Dict, Optional
from gui_tools.window_manager import WindowManager, WindowRect
from .shared_state import get_active_window, set_active_window


@tool
def list_windows() -> List[str]:
    """列出当前所有窗口标题"""
    window_manager = WindowManager()
    windows = window_manager.list_windows()
    return [w.title for w in windows]


@tool
def get_active_window_info() -> Dict:
    """获取当前活动窗口信息"""
    window_manager = WindowManager()
    active_window = window_manager.get_active_window()
    if active_window:
        return {
            "title": active_window.title,
            "index": active_window.index,
            "rect": active_window.rect.to_dict()
        }
    return {"error": "未找到活动窗口"}


@tool
def get_window_info(title: str, index: int = 0) -> Dict:
    """获取指定窗口信息"""
    window_manager = WindowManager()
    windows = window_manager.list_windows()
    matching_windows = [w for w in windows if title in w.title]

    if not matching_windows:
        return {"error": f"未找到标题包含 '{title}' 的窗口"}

    if index >= len(matching_windows):
        return {"error": f"窗口索引超出范围: {index}"}

    window = matching_windows[index]
    return {
        "title": window.title,
        "index": window.index,
        "rect": window.rect.to_dict()
    }


@tool
def activate_window(title: str, index: int = 0) -> Dict:
    """激活指定窗口并保存为当前窗口"""
    window_manager = WindowManager()

    # 聚焦窗口
    try:
        window_manager.focus_window(title, index)
    except Exception as e:
        return {"error": f"聚焦窗口失败: {str(e)}"}

    # 获取窗口信息
    windows = window_manager.list_windows()
    matching_windows = [w for w in windows if title in w.title]

    if not matching_windows or index >= len(matching_windows):
        return {"error": f"未找到窗口: {title} (index: {index})"}

    active_window_rect = matching_windows[index].rect
    set_active_window(active_window_rect)
    return {
        "message": f"已激活窗口: {title}",
        "rect": active_window_rect.to_dict()
    }


@tool
def get_current_active_window() -> Dict:
    """获取当前激活的窗口信息"""
    active_window = get_active_window()
    if active_window is None:
        return {"error": "未激活任何窗口"}
    return {
        "rect": active_window.to_dict()
    }
