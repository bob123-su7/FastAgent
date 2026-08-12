# FastAgent

这是 Fast Agent，欢迎大家提贡献。


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

## 参与贡献

欢迎提交 Issue 或 Pull Request。提交前请先阅读[贡献指南](CONTRIBUTING.md)。
