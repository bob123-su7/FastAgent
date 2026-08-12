#!/usr/bin/env python3
"""AgentTracer 使用演示：模拟一个 Agent 的三阶段执行流程。

运行方式::

    python3 examples/tracer_demo.py

此演示无需额外依赖，仅使用标准库。"""

import time
import random

from fastagent import AgentTracer


# ── 模拟 Agent 工具 ──────────────────────────────────────────────────────────

def mock_search(query: str) -> str:
    """模拟一次搜索工具调用。"""
    time.sleep(random.uniform(0.05, 0.2))
    return f"搜索结果（关于 '{query}'）"


def mock_llm_call(prompt: str) -> str:
    """模拟一次大模型调用。"""
    time.sleep(random.uniform(0.1, 0.4))
    return f"大模型回复（针对 {len(prompt)} 字符的提示词）"


# ── 主流程 ──────────────────────────────────────────────────────────────────

def main() -> None:
    tracer = AgentTracer(name="查询天气Agent")

    # 阶段 1：理解意图
    with tracer.span("理解用户意图", metadata={"model": "gpt-4o"}):
        mock_llm_call("明天北京天气怎么样？")

    # 阶段 2：搜索信息（含嵌套子步骤）
    with tracer.span("搜索外部信息", metadata={"tool": "SearchAPI"}):
        with tracer.span("查询天气 API"):
            mock_search("北京 2026-08-13 天气")
        with tracer.span("解析 API 返回"):
            mock_llm_call("解析天气数据 JSON")

    # 阶段 3：生成回复
    with tracer.span("生成最终回复", metadata={"model": "gpt-4o", "tokens": 256}):
        mock_llm_call("根据天气信息生成友好回复")

    # 打印追踪报告
    tracer.print_tree()

    # 输出统计摘要
    print()
    print("=== 统计摘要 ===")
    print(tracer.stats())

    # 输出 JSON（可对接外部监控系统）
    print()
    print("=== JSON 导出（供 AgentOps 对接）===")
    print(tracer.to_json())


if __name__ == "__main__":
    main()
