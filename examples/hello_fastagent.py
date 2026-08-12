#!/usr/bin/env python3
"""FastAgent 示例脚本：一个简单的欢迎入口。"""

from __future__ import annotations

import argparse
import sys


def greet(name: str = "FastAgent") -> str:
    """返回对指定名称的问候语。"""
    return f"Hello, {name}! Welcome to FastAgent."


def main(argv: list[str] | None = None) -> int:
    """运行命令行欢迎示例。"""
    parser = argparse.ArgumentParser(description="Print a FastAgent welcome message.")
    parser.add_argument("name", nargs="?", default="FastAgent", help="Name to greet.")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    print(greet(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
