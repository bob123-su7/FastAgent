#!/usr/bin/env python3
"""示例：一个会调用 CalculatorSkill 的最小 Agent。

运行：
    python examples/calculator_agent.py
"""

import asyncio
import re

from fastagent import Agent, Message, SkillRegistry, ToolCall
from fastagent.tools import CalculatorSkill

_EXPRESSION_PATTERN = re.compile(r"[-+*/()\d.\s]+")


class CalculatorAgent(Agent):
    """规则版 Agent：从用户输入中抠出算术表达式并调用 calculator Skill。

    真实场景中 `think` 通常由 LLM 驱动；这里用简单规则代替，
    目的是演示 Agent / Skill / Memory 三者如何协作，无需外部 API Key。
    """

    async def think(self, history: list[Message]):
        last_user_message = next(m for m in reversed(history) if m.role.value == "user")
        already_called = any(m.role.value == "tool" for m in history)

        if already_called:
            tool_message = next(m for m in reversed(history) if m.role.value == "tool")
            return f"计算结果是：{tool_message.content}"

        match = _EXPRESSION_PATTERN.search(last_user_message.content)
        if not match:
            return "抱歉，我没有在你的输入中找到可计算的算术表达式。"

        return ToolCall(name="calculator", arguments={"expression": match.group().strip()})


async def main() -> None:
    skills = SkillRegistry()
    skills.register(CalculatorSkill())

    agent = CalculatorAgent(skills=skills)

    reply = await agent.run("帮我算一下 (3 + 5) * 2")
    print(reply)


if __name__ == "__main__":
    asyncio.run(main())
