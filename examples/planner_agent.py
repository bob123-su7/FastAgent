#!/usr/bin/env python3
"""示例：一个会把目标拆成执行计划的最小 Planner Agent。

运行：
    python examples/planner_agent.py
"""

import asyncio
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastagent import Agent, Message, Skill, SkillRegistry, ToolCall


class TaskPlannerSkill(Skill):
    """把用户目标拆成一组稳定的执行步骤，便于演示 Agent 调用工具。"""

    name = "task_planner"
    description = "根据用户目标生成一个离线、可重复的执行计划"

    async def run(self, goal: str) -> str:
        clean_goal = " ".join(goal.split())
        if not clean_goal:
            raise ValueError("目标不能为空")

        steps = [
            f"明确目标：{clean_goal}",
            "拆分任务：列出可以独立完成的小步骤。",
            "选择工具：决定需要调用哪些 Skill，并准备输入参数。",
            "执行验证：运行相关命令，确认结果符合预期。",
            "回顾结果：记录完成情况、遗留问题和下一步改进方向。",
        ]
        return "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))


class PlannerAgent(Agent):
    """规则版 Agent：先调用 TaskPlannerSkill，再把工具结果整理为回复。

    真实场景中 `think` 通常由 LLM 决定是否调用工具；这里使用固定规则，
    重点展示 Agent 如何通过 Memory 读取历史、调用 Skill 并产出最终回复。
    """

    async def think(self, history: list[Message]):
        tool_message = next((m for m in reversed(history) if m.name == "task_planner"), None)
        if tool_message is not None:
            return f"这是一个可执行计划：\n{tool_message.content}"

        last_user_message = next(m for m in reversed(history) if m.role.value == "user")
        return ToolCall(
            name="task_planner",
            arguments={"goal": last_user_message.content},
        )


async def main() -> None:
    skills = SkillRegistry()
    skills.register(TaskPlannerSkill())

    agent = PlannerAgent(skills=skills)

    reply = await agent.run("为 FastAgent 新增一个离线示例并验证它能运行")
    print(reply)


if __name__ == "__main__":
    asyncio.run(main())
