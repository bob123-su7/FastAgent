import unittest

from fastagent.model import ModelAgent
from fastagent.skill import Skill, SkillRegistry
from fastagent.types import Message, Role, ToolCall


class ScriptedModel:
    def __init__(self, decisions: list[str | ToolCall]) -> None:
        self.decisions = iter(decisions)
        self.histories: list[list[Message]] = []

    async def complete(self, messages: list[Message]) -> str | ToolCall:
        self.histories.append(messages)
        return next(self.decisions)


class AddSkill(Skill):
    name = "add"

    async def run(self, a: int, b: int) -> int:
        return a + b


class ModelAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_model_agent_returns_model_response(self) -> None:
        model = ScriptedModel(["Hello"])

        self.assertEqual(await ModelAgent(model).run("Hi"), "Hello")
        self.assertEqual(model.histories[0][-1].content, "Hi")

    async def test_model_agent_receives_tool_result_in_history(self) -> None:
        model = ScriptedModel(
            [ToolCall(name="add", arguments={"a": 2, "b": 3}), "Five"]
        )
        skills = SkillRegistry()
        skills.register(AddSkill())

        self.assertEqual(await ModelAgent(model, skills=skills).run("Add"), "Five")
        self.assertEqual(model.histories[1][-1].role, Role.TOOL)
        self.assertEqual(model.histories[1][-1].content, "5")


if __name__ == "__main__":
    unittest.main()
