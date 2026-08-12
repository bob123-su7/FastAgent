#!/usr/bin/env python3
"""FastAgent 示例脚本：一个简单的任务处理 Agent 演示。"""


class SimpleAgent:
    """一个最简的 Agent 实现，根据输入关键词返回对应回复。"""

    def __init__(self, name: str = "SimpleAgent"):
        """初始化 Agent 名称。"""
        self.name = name
        self._rules: dict[str, str] = {
            "你好": "你好！我是 SimpleAgent，很高兴为你服务。",
            "时间": "抱歉，我暂时无法获取实时时间。",
            "帮助": "你可以尝试问我「你好」「时间」等关键词。",
        }

    def respond(self, user_input: str) -> str:
        """根据用户输入的关键词匹配规则并返回回复。"""
        for keyword, reply in self._rules.items():
            if keyword in user_input:
                return f"[{self.name}] {reply}"
        return f"[{self.name}] 抱歉，我没有理解你的意思。试试输入「帮助」？"


if __name__ == "__main__":
    agent = SimpleAgent()
    print(agent.respond("你好"))
    print(agent.respond("现在几点了？时间"))
    print(agent.respond("今天天气怎么样？"))
