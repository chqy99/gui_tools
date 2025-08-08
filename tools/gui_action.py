# gui_action.py - 执行操作类工具函数
from langchain_core.tools import tool
from typing import Optional, Dict
from window_manager import WindowManager, WindowRect
from pyautogui_wrapper import PyAutoGUIWrapper, ScreenCapture
from .shared_state import get_active_window


@tool
def click_at(x: int, y: int, relative: bool = True) -> Dict:
    """点击坐标"""
    active_window = get_active_window()
    if active_window is None and relative:
        return {"error": "未激活窗口，无法使用相对坐标"}

    try:
        PyAutoGUIWrapper(active_window).click(x, y, relative)
        return {"message": f"已点击坐标 ({x}, {y})"}
    except Exception as e:
        return {"error": f"点击失败: {str(e)}"}


@tool
def move_mouse(x: int, y: int, relative: bool = True) -> Dict:
    """移动鼠标"""
    active_window = get_active_window()
    if active_window is None and relative:
        return {"error": "未激活窗口，无法使用相对坐标"}

    try:
        PyAutoGUIWrapper(active_window).move_to(x, y, relative)
        return {"message": f"已移动鼠标到 ({x}, {y})"}
    except Exception as e:
        return {"error": f"移动鼠标失败: {str(e)}"}


@tool
def double_click_at(x: int, y: int, relative: bool = True) -> Dict:
    """双击坐标"""
    active_window = get_active_window()
    if active_window is None and relative:
        return {"error": "未激活窗口，无法使用相对坐标"}

    try:
        PyAutoGUIWrapper(active_window).double_click(x, y, relative)
        return {"message": f"已双击坐标 ({x}, {y})"}
    except Exception as e:
        return {"error": f"双击失败: {str(e)}"}


@tool
def right_click_at(x: int, y: int, relative: bool = True) -> Dict:
    """右键点击坐标"""
    active_window = get_active_window()
    if active_window is None and relative:
        return {"error": "未激活窗口，无法使用相对坐标"}

    try:
        PyAutoGUIWrapper(active_window).right_click(x, y, relative)
        return {"message": f"已右键点击坐标 ({x}, {y})"}
    except Exception as e:
        return {"error": f"右键点击失败: {str(e)}"}


@tool
def middle_click_at(x: int, y: int, relative: bool = True) -> Dict:
    """中键点击坐标"""
    active_window = get_active_window()
    if active_window is None and relative:
        return {"error": "未激活窗口，无法使用相对坐标"}

    try:
        PyAutoGUIWrapper(active_window).middle_click(x, y, relative)
        return {"message": f"已中键点击坐标 ({x}, {y})"}
    except Exception as e:
        return {"error": f"中键点击失败: {str(e)}"}


@tool
def drag_to(x: int, y: int, duration: float = 0.5, relative: bool = True) -> Dict:
    """拖动鼠标到目标位置"""
    active_window = get_active_window()
    if active_window is None and relative:
        return {"error": "未激活窗口，无法使用相对坐标"}

    try:
        PyAutoGUIWrapper(active_window).drag_to(x, y, duration, relative)
        return {"message": f"已拖动到坐标 ({x}, {y})"}
    except Exception as e:
        return {"error": f"拖动失败: {str(e)}"}


@tool
def scroll_mouse(clicks: int) -> Dict:
    """滚动鼠标"""
    try:
        PyAutoGUIWrapper(get_active_window()).scroll(clicks)
        return {"message": f"已滚动鼠标 {clicks} 次"}
    except Exception as e:
        return {"error": f"滚动失败: {str(e)}"}


@tool
def type_text(text: str, interval: float = 0.05) -> Dict:
    """输入文字"""
    try:
        PyAutoGUIWrapper(get_active_window()).type_text(text, interval)
        return {"message": f"已输入文字: {text}"}
    except Exception as e:
        return {"error": f"输入文字失败: {str(e)}"}


@tool
def press_key(key: str) -> Dict:
    """按键"""
    try:
        PyAutoGUIWrapper(get_active_window()).press_key(key)
        return {"message": f"已按键: {key}"}
    except Exception as e:
        return {"error": f"按键失败: {str(e)}"}


@tool
def hotkey(*keys: str) -> Dict:
    """组合快捷键"""
    try:
        PyAutoGUIWrapper(get_active_window()).hotkey(*keys)
        return {"message": f"已执行快捷键: {'+'.join(keys)}"}
    except Exception as e:
        return {"error": f"快捷键失败: {str(e)}"}


@tool
def screenshot_current_window(filepath: str) -> Dict:
    """对当前激活窗口截图并保存"""
    active_window = get_active_window()
    if active_window is None:
        return {"error": "未激活窗口"}

    try:
        img = ScreenCapture.screenshot_rect(active_window)
        ScreenCapture.save_screenshot(img, filepath)
        return {"message": f"截图已保存到: {filepath}"}
    except Exception as e:
        return {"error": f"截图失败: {str(e)}"}


@tool
def resize_window(title: str, width: int, height: int, index: int = 0) -> Dict:
    """调整窗口大小"""
    try:
        window_manager = WindowManager()
        window_manager.resize_window(title, width, height, index)
        return {"message": f"已调整窗口 '{title}' 大小为 {width}x{height}"}
    except Exception as e:
        return {"error": f"调整窗口大小失败: {str(e)}"}


@tool
def move_window(title: str, x: int, y: int, index: int = 0) -> Dict:
    """移动窗口"""
    try:
        window_manager = WindowManager()
        window_manager.move_window(title, x, y, index)
        return {"message": f"已移动窗口 '{title}' 到 ({x}, {y})"}
    except Exception as e:
        return {"error": f"移动窗口失败: {str(e)}"}


@tool
def capture_window(title: str, filepath: str, index: int = 0) -> Dict:
    """对指定窗口截图并保存"""
    try:
        window_manager = WindowManager()
        img = window_manager.capture_window(title, index)
        if img:
            ScreenCapture.save_screenshot(img, filepath)
            return {"message": f"窗口截图已保存到: {filepath}"}
        else:
            return {"error": f"未找到窗口: {title}"}
    except Exception as e:
        return {"error": f"窗口截图失败: {str(e)}"}
