#!/usr/bin/env python3
"""FastAgent 示例脚本：一个简单的欢迎入口。"""


def greet(name: str = "FastAgent") -> str:
    """返回对指定名称的问候语。"""
    return f"Hello, {name}! Welcome to FastAgent."


if __name__ == "__main__":
    print(greet())
