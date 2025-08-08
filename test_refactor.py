#!/usr/bin/env python3
# test_refactor.py - 测试重构后的功能

def test_imports():
    """测试导入是否正常"""
    try:
        # 测试 window_manager 导入
        from window_manager import WindowManager, WindowInfo, WindowRect
        print("✓ window_manager 导入成功")

        # 测试 pyautogui_wrapper 导入
        from pyautogui_wrapper import PyAutoGUIWrapper
        print("✓ pyautogui_wrapper 导入成功")

        # 测试 tools 导入
        from tools import TOOLS
        print("✓ tools 模块导入成功")
        print(f"  找到 {len(TOOLS)} 个工具")

        # 测试具体工具导入
        from tools import list_windows, click_at, activate_window
        print("✓ 具体工具导入成功")

        return True

    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_window_manager():
    """测试窗口管理器"""
    try:
        from window_manager import WindowManager

        window_manager = WindowManager()
        windows = window_manager.list_windows()
        print(f"✓ 窗口管理器工作正常，找到 {len(windows)} 个窗口")

        if windows:
            print(f"  示例窗口: {windows[0].title}")

        return True

    except Exception as e:
        print(f"✗ 窗口管理器测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("开始测试重构后的功能...")
    print("=" * 50)

    # 测试导入
    if not test_imports():
        return

    print()

    # 测试窗口管理器
    if not test_window_manager():
        return

    print()
    print("=" * 50)
    print("✓ 所有测试通过！重构成功！")


if __name__ == "__main__":
    main()