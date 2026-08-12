# FastAgent

> 助力每一个梦想 🚀 —— 一个面向实践的 AI Agent 学习项目

FastAgent 是一个**面向实践**的 AI Agent 学习项目，欢迎通过示例、文档和练习共同完善它。无论你是刚接触智能体的新手，还是想深入工程落地的开发者，都能在这里找到从概念到实践的学习路径。

## ✨ 项目亮点

- **从概念到实践**：从 AI Agent 科普，到 Harness 调度层，再到工程落地验收，一条完整的学习链路。
- **可运行的示例**：开箱即用的 Python 示例，快速体验 FastAgent。
- **在线练习入口**：基于 COZE 打造的 Python 知识点与练习网站，点击即练。
- **跨工具工作流规范**：一套通用的 10 步闭环工作流程 Skill，兼容 WorkBuddy / Claude Code / Codex / Cursor。
- **社区共建**：欢迎通过 Issue 和 Pull Request 一起完善这个学习项目。


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



## 📁 目录结构

```
FastAgent/
├── examples/                          # 可运行的示例代码
│   └── hello_fastagent.py             # 欢迎示例
├── docs/                              # 技术文档
│   ├── harness技术介绍及运用.md        # Harness 调度层详解
│   └── agent-engineering-checklist.md # 工程落地与验收清单
├── 工作流程规范/                       # 跨工具工作流 Skill
│   ├── SKILL.md                       # 10 步闭环流程规范
│   ├── README.md                      # 使用说明
│   ├── install.sh                     # 一键安装脚本
│   └── references/                    # 提示词与设计规范
├── AI_Agent.md                        # AI Agent 科普指南
├── PYTHON知识点与练习网站              # Python 在线练习入口
├── AGENTS.md                          # AI 代理协作约定
├── CONTRIBUTING.md                    # 贡献指南
└── requirements.txt                   # 依赖清单
```

## 📚 文档导览

| 文档 | 说明 |
| --- | --- |
| [AI Agent 科普指南](AI_Agent.md) | 了解智能体的核心能力、架构与常见应用，从概念到实践一文读懂。 |
| [Harness 技术介绍及运用](docs/harness技术介绍及运用.md) | 理解调度层如何连接模型、记忆与工具。 |
| [AI Agent 工程落地与验收清单](docs/agent-engineering-checklist.md) | 用任务契约、风险分级、评测与可观测性把 Demo 推进到可验收实现。 |
| [工作流程规范](工作流程规范/README.md) | 通过结构化流程规划、执行和检查复杂任务。 |

## 🧠 学习路径建议

1. **入门**：阅读 [AI Agent 科普指南](AI_Agent.md)，建立对智能体的整体认知。
2. **进阶**：阅读 [Harness 技术介绍及运用](docs/harness技术介绍及运用.md)，理解调度层如何工作。
3. **实践**：运行 `examples/hello_fastagent.py`，动手体验；通过 `PYTHON知识点与练习网站` 在线练习 Python。
4. **落地**：参考 [AI Agent 工程落地与验收清单](docs/agent-engineering-checklist.md)，把 Demo 推进到可验收实现。
5. **提效**：使用 [工作流程规范](工作流程规范/README.md)，用结构化流程规划、执行和检查复杂任务。

## 🤝 参与贡献

欢迎提交 Issue 或 Pull Request！提交前请先阅读[贡献指南](CONTRIBUTING.md)。

- 🐛 发现 Bug？提交 Issue 告诉我们。
- 💡 有改进想法？欢迎提交 PR。
- 📖 想补充文档或示例？同样欢迎。

## 📄 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](工作流程规范/LICENSE)。

---

**FastAgent —— 助力每一个梦想，一起把 AI Agent 学明白、用起来。**
