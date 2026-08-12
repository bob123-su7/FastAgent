# 贡献指南

感谢你对 FastAgent 的关注！本项目欢迎代码、测试、示例和文档贡献。下面的流程帮助你在提交前完成一个范围清晰、可验证且便于审查的改动。

## 适合贡献的内容

- 修复 `fastagent/` 中可稳定复现的行为问题。
- 为已有模块补充单元测试，尤其是边界条件和错误路径。
- 增加可以独立运行的 `examples/` 示例。
- 改进 `docs/`、README 或学习材料中的错误、缺失步骤和过时说明。
- 提出与 FastAgent 学习和实践目标相关的功能建议。

对于较大的功能或架构调整，建议先创建 Issue 说明使用场景、最小范围和验收方式，再开始实现。这样可以避免重复工作，也能让讨论聚焦在问题本身。

## 项目结构速览

| 路径 | 用途 |
| --- | --- |
| `fastagent/` | Agent、模型、记忆、技能、工具和追踪器的核心实现。 |
| `tests/` | 使用 pytest 编写的自动化测试。 |
| `examples/` | 可直接运行的学习和演示代码。 |
| `docs/` | 架构、评测、Harness 和追踪相关文档。 |
| `.github/` | Issue 模板和持续集成工作流。 |
| `工作流程规范/` | 可复用的跨工具工作流 Skill。 |

修改前请先阅读与目标目录相邻的说明和现有实现。仓库根目录的 `AGENTS.md` 约定优先级高于 README 和局部说明；如果这些说明存在冲突，请以 `AGENTS.md` 为准。

## 开始前准备

项目在 `pyproject.toml` 中声明了 Python 3.10 或更高版本。源码使用了 `str | None` 等 Python 3.10 引入的类型标注语法，因此 Python 3.9 及更低版本不能完整运行测试。

先确认解释器版本：

```bash
python3 --version
```

建议在虚拟环境中安装依赖，避免影响系统 Python：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`.venv/` 已被 Git 忽略，无需提交。如果你使用 Windows，请将激活命令替换为：

```powershell
.venv\Scripts\Activate.ps1
```

安装完成后，可以先运行欢迎示例确认基础环境可用：

```bash
python examples/hello_fastagent.py
```

预期会输出：

```text
Hello, FastAgent! Welcome to FastAgent.
```

## 获取代码并创建分支

如果你不是仓库成员，请先在 GitHub 上 Fork 本仓库，然后克隆自己的 Fork：

```bash
git clone https://github.com/<your-account>/FastAgent.git
cd FastAgent
```

为上游仓库添加只读远端有助于后续同步：

```bash
git remote add upstream https://github.com/limouren2000/FastAgent.git
git remote -v
```

在开始新工作前，从最新的 `main` 创建分支：

```bash
git switch main
git pull origin main
git switch -c feature/short-description
```

分支名请描述改动目的，例如：

```text
docs/improve-trace-guide
fix/handle-empty-tool-result
test/add-memory-edge-cases
```

一个分支尽量只解决一个独立问题。不要将不相关的格式化、重命名或本地配置与功能修复混在同一个 PR 中。

## 开发与测试

测试套件使用 pytest 和 pytest-asyncio。提交前，请在仓库根目录运行：

```bash
python -m pytest
```

也可以只运行与改动相关的测试文件，以便在开发过程中快速反馈：

```bash
python -m pytest tests/test_agent.py
python -m pytest tests/test_trace.py
```

修改示例时，请直接运行对应脚本，并确认 README 或文档中的命令和预期输出仍然准确。例如：

```bash
python examples/calculator_agent.py
python -X utf8 examples/tracer_demo.py
```

测试未能运行、被环境阻塞或出现已有失败时，请不要忽略该结果。请在 PR 描述中写明执行的命令、观察到的错误和它与本次改动的关系，便于维护者判断。

## 修改范围与代码风格

保持改动小而聚焦，并尽量沿用目标文件已有的命名、类型标注、文档字符串和错误处理方式。

新增或修改公开接口时：

- 为正常路径补充或更新测试。
- 覆盖影响使用者的错误路径或边界条件。
- 在必要时更新 `README.md`、`docs/` 或对应示例。
- 避免在测试中访问真实网络、时间敏感服务或用户文件。

新增示例时：

- 放在 `examples/` 下，并使用能说明意图的文件名。
- 保持离线、可重复运行，除非文档明确说明外部依赖。
- 在示例顶部或相邻文档中说明运行命令和预期行为。

修改文档时：

- 验证每一条命令与当前仓库结构和依赖一致。
- 使用现有术语，并链接到仓库内的相关文档而不是复制同一段说明。
- 不要把未验证的性能数据、兼容性结论或功能承诺写成事实。

## 提交前检查

提交前先查看工作区，确认没有将虚拟环境、缓存、编辑器配置或无关文件带入改动：

```bash
git status --short
git diff
```

检查空白错误和冲突标记：

```bash
git diff --check
git grep -nE '^(<<<<<<<|=======|>>>>>>>)' -- . ':!*.lock' || true
```

完成相关测试后，按文件暂存，而不是默认暂存全部内容：

```bash
git add path/to/changed_file.py
git diff --cached
```

最后检查一次暂存区内容：

```bash
git diff --cached --check
git status --short
```

## 提交规范

- 使用中文或英文撰写提交信息均可，但请保持简洁。
- 一次提交尽量只完成一件事。
- 使用能说明意图的前缀，例如 `docs:`、`fix:`、`test:` 或 `feat:`。
- 如果有相关 Issue，请在提交信息或 PR 描述中引用。

示例：

```text
docs: clarify local test setup
fix: preserve tool errors in agent history
test: cover empty memory history
```

提交后推送分支：

```bash
git push -u origin feature/short-description
```

## Pull Request 清单

创建 PR 前，请确认以下内容：

- [ ] PR 只包含一个清晰的问题或改进。
- [ ] 分支基于最新的 `main`。
- [ ] 已运行相关测试，或已说明无法运行的原因。
- [ ] 已运行 `git diff --check`。
- [ ] 已更新需要同步的测试、示例或文档。
- [ ] PR 描述包含改动内容、修改原因和验证结果。
- [ ] 不包含密钥、访问令牌、真实用户数据或本地环境文件。

PR 描述可以使用下面的模板：

```markdown
## What changed

- Describe the user-visible change.

## Why

- Explain the problem this change solves.

## Validation

- `python -m pytest`
- Any focused commands or manual checks
```

如果测试未运行或失败，请将实际命令和原因写在 `Validation` 中，而不是删除该部分。

## 高质量 PR 叙事模板（推荐）

当你希望 PR 更易审阅、也更能体现工程价值时，可以采用以下结构。它强调“问题定义、决策依据、验证证据”三件事，适合文档改进、功能迭代和缺陷修复。

### 标题建议

- 使用「动作 + 对象 + 价值」结构，避免泛化标题。
- 示例：
	- `docs: elevate contribution guide with review-ready PR narrative patterns`
	- `fix: harden tool-call boundary checks for predictable agent execution`
	- `test: expand regression coverage for memory edge conditions`

### 描述模板

```markdown
## Executive Summary

- One-sentence statement of what changed and why it matters.

## Problem Statement

- What concrete issue existed before this change?
- Who or what was affected?

## Design Decision

- Key implementation choice(s) and trade-offs.
- Why this approach was selected over alternatives.

## Scope

- Included: explicit list of files or behaviors changed.
- Excluded: related but intentionally deferred items.

## Validation

- `python -m pytest`
- Additional focused checks (commands + observed results).

## Risk & Rollback

- Known risks introduced by this change.
- How to revert safely if unexpected regressions appear.
```

### 审阅友好清单

- 用“可验证事实”替代“主观判断”，例如命令、输出、对比结果。
- 控制单个 PR 的变更范围，减少审阅上下文切换。
- 对潜在风险做显式说明，避免审阅者猜测隐含影响。
- 若涉及行为变化，给出最小复现步骤，确保他人可独立验证。

## Issue 与反馈

提交 Bug 前，请先搜索现有 Issue，并使用仓库最新的 `main` 分支复现问题。Bug 报告应包含最小复现步骤、预期行为、实际行为和运行环境；仓库提供的 Bug 模板会引导你填写这些信息。

功能建议应优先描述要解决的使用者问题、受影响的场景和可验证的结果，而不是只给出实现方案。仓库提供的功能建议模板会要求填写背景、方案、备选方案和验收方式。

如果你不确定某个想法是否适合实现，欢迎先通过 Issue 讨论。感谢你帮助 FastAgent 变得更清晰、更可运行，也更适合学习和实践。
