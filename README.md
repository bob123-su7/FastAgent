# FastAgent

这是 Fast Agent，欢迎大家提贡献。助力每一个梦想。。。。



FastAgent 是一个面向实践的学习项目，欢迎通过示例、文档和练习共同完善它。

## 核心包：fastagent

`fastagent/` 是一个最小可用的 Agent 基础框架，提供三类核心抽象：

- **Skill**（`fastagent.skill`）：Agent 可调用的工具，`SkillRegistry` 负责注册与路由调度
- **Memory**（`fastagent.memory`）：维护会话上下文，内置 `InMemoryMemory`
- **Agent**（`fastagent.agent`）：驱动"感知 → 决策 → 执行 → 反思"循环的基类

内置了几个开箱即用的 Skill（`fastagent.tools`）：`CalculatorSkill`、`ClockSkill`、
`ReadFileSkill`、`WriteFileSkill`。详细设计见 [`docs/architecture.md`](docs/architecture.md)。

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
pytest
```

### 运行 Agent 示例

```bash
python examples/calculator_agent.py
```

## 快速开始

运行欢迎示例：

```bash
python3 examples/hello_fastagent.py
```

预期输出：

```text
Hello, FastAgent! Welcome to FastAgent.
```

仓库中的 `PYTHON知识点与练习网站` 文件还提供了 Python 知识点和练习入口。

## 文档导览

- [AI Agent 科普指南](AI_Agent.md)：了解智能体的核心能力、架构与常见应用。
- [Harness 技术介绍及运用](docs/harness技术介绍及运用.md)：理解调度层如何连接模型、记忆与工具。
- [AI Agent 工程落地与验收清单](docs/agent-engineering-checklist.md)：用任务契约、风险分级、评测与可观测性把 Demo 推进到可验收实现。
- [工作流程规范](工作流程规范/README.md)：通过结构化流程规划、执行和检查复杂任务。

## 参与贡献

欢迎提交 Issue 或 Pull Request。提交前请先阅读[贡献指南](CONTRIBUTING.md)。
