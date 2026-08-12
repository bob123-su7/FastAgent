"""AgentTracer：轻量级 Agent 执行追踪器。

提供嵌套步骤计时、控制台彩色输出和结构化数据导出，
帮助开发者在调试 Agent 时快速定位耗时瓶颈。
"""

from __future__ import annotations

import json
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Optional


# ── ANSI 颜色（非 Windows 终端或 Windows Terminal 均支持） ──────────────────
_RESET = "\033[0m"
_COLORS = {
    "dim": "\033[2m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "red": "\033[31m",
    "bold": "\033[1m",
}


def _color(text: str, name: str) -> str:
    return f"{_COLORS.get(name, '')}{text}{_RESET}"


# ── TraceSpan ────────────────────────────────────────────────────────────────


class TraceSpan:
    """表示 Agent 执行过程中的一个步骤。"""

    def __init__(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        parent: Optional[TraceSpan] = None,
    ) -> None:
        self.name = name
        self.metadata = metadata or {}
        self.parent = parent
        self.children: List[TraceSpan] = []
        self._start: float = 0.0
        self._end: float = 0.0

    @property
    def duration_ms(self) -> float:
        """步骤耗时（毫秒）。"""
        if self._start:
            end = self._end or time.perf_counter()
            return (end - self._start) * 1000
        return 0.0

    @property
    def depth(self) -> int:
        """当前步骤在追踪树中的深度（0 = 根）。"""
        return self.parent.depth + 1 if self.parent else 0

    def _render_tree(self, lines: List[str], prefix: str = "", is_last: bool = True) -> None:
        """递归生成树形字符串。"""
        connector = "└── " if is_last else "├── "
        branch = "    " if is_last else "│   "

        dur = self.duration_ms
        if dur >= 1000:
            dur_str = _color(f"{dur/1000:.2f}s", "yellow")
        elif dur >= 500:
            dur_str = _color(f"{dur:.0f}ms", "yellow")
        else:
            dur_str = f"{dur:.0f}ms"

        meta_str = ""
        if self.metadata:
            items = [f"{k}={v}" for k, v in self.metadata.items()]
            meta_str = _color(f"  ({', '.join(items)})", "dim")

        lines.append(f"{prefix}{connector}{_color(self.name, 'cyan')}  {dur_str}{meta_str}")

        for i, child in enumerate(self.children):
            child._render_tree(lines, prefix + branch, i == len(self.children) - 1)

    def _collect_stats(self, stats: Dict[str, Any]) -> None:
        """递归收集自身及所有子节点的统计数据。"""
        if self.parent is not None:  # 跳过根节点
            dur = round(self.duration_ms, 2)
            stats["total_spans"] += 1
            stats["total_duration_ms"] += dur
            if dur < stats["min_duration_ms"]:
                stats["min_duration_ms"] = dur
                stats["min_duration_span"] = {"name": self.name, "duration_ms": dur}
            if dur > stats["max_duration_ms"]:
                stats["max_duration_ms"] = dur
                stats["max_duration_span"] = {"name": self.name, "duration_ms": dur}
            if self.depth > stats["max_depth"]:
                stats["max_depth"] = self.depth
        for child in self.children:
            child._collect_stats(stats)

    def to_dict(self) -> Dict[str, Any]:
        """将追踪树导出为字典，便于 JSON 序列化。"""
        return {
            "name": self.name,
            "duration_ms": round(self.duration_ms, 2),
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children],
        }


# ── AgentTracer ──────────────────────────────────────────────────────────────


class AgentTracer:
    """Agent 执行追踪器。

    用法示例::

        tracer = AgentTracer()

        with tracer.span("规划阶段", metadata={"tool": "ReAct"}):
            with tracer.span("调用搜索引擎"):
                ...
            with tracer.span("总结结果"):
                ...

        tracer.print_tree()
        # 导出: print(json.dumps(tracer.to_dict(), indent=2, ensure_ascii=False))
    """

    def __init__(self, name: str = "AgentRun") -> None:
        self._root = TraceSpan(name=name)
        self._root._start = time.perf_counter()
        self._current = self._root

    # ── 上下文管理器 ──────────────────────────────────────────────────────

    @contextmanager
    def span(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> Iterator[TraceSpan]:
        """创建一个追踪步骤，支持嵌套。

        参数:
            name: 步骤名称。
            metadata: 附加元数据（如 tool、model、tokens 等）。
        """
        span = TraceSpan(name=name, metadata=metadata, parent=self._current)
        self._current.children.append(span)
        prev = self._current
        self._current = span
        span._start = time.perf_counter()
        try:
            yield span
        finally:
            span._end = time.perf_counter()
            self._current = prev

    # ── 装饰器 ────────────────────────────────────────────────────────────

    def trace(
        self, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None
    ) -> Callable:
        """将函数包裹为追踪步骤。

        参数:
            name: 步骤名称，默认为函数名。
            metadata: 附加元数据。
        """

        def decorator(func: Callable) -> Callable:
            span_name = name or func.__name__

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                with self.span(span_name, metadata=metadata):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    # ── 输出 ──────────────────────────────────────────────────────────────

    def print_tree(self) -> None:
        """在控制台打印彩色追踪树。"""
        root_dur = self._root.duration_ms
        header = f"\n{_color('AgentTracer 追踪报告', 'bold')}  "
        header += _color(f"(总耗时 {root_dur:.0f}ms)", "dim")
        header += "\n" + "─" * 50
        print(header)
        for i, child in enumerate(self._root.children):
            lines: List[str] = []
            child._render_tree(lines, "", i == len(self._root.children) - 1)
            print("\n".join(lines))
        print("─" * 50)

    def to_dict(self) -> Dict[str, Any]:
        """将整个追踪树导出为字典。"""
        return self._root.to_dict()

    def to_json(self, indent: int = 2) -> str:
        """将追踪树导出为 JSON 字符串。"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def stats(self) -> Dict[str, Any]:
        """返回追踪执行的统计摘要。

        返回字典包含:
            - total_spans: 步骤总数（不含根节点）
            - total_duration_ms: 所有步骤总耗时（ms）
            - avg_duration_ms: 平均耗时（ms）
            - min_duration_ms / max_duration_ms: 最快 / 最慢步骤耗时
            - min_duration_span / max_duration_span: 最快 / 最慢步骤的名称与耗时
            - max_depth: 最大嵌套深度
        """
        stats: Dict[str, Any] = {
            "total_spans": 0,
            "total_duration_ms": 0.0,
            "min_duration_ms": float("inf"),
            "max_duration_ms": -1.0,
            "min_duration_span": None,
            "max_duration_span": None,
            "max_depth": 0,
        }
        self._root._collect_stats(stats)
        if stats["total_spans"] > 0:
            stats["avg_duration_ms"] = round(
                stats["total_duration_ms"] / stats["total_spans"], 2
            )
        else:
            stats["avg_duration_ms"] = 0.0
        stats["total_duration_ms"] = round(stats["total_duration_ms"], 2)
        stats["min_duration_ms"] = (
            round(stats["min_duration_ms"], 2)
            if stats["min_duration_span"] is not None
            else 0.0
        )
        if stats["max_duration_span"] is None:
            stats["max_duration_ms"] = 0.0
        else:
            stats["max_duration_ms"] = round(stats["max_duration_ms"], 2)
        return stats
