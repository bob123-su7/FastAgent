# AppendFileSkill 设计说明

## 目标

为内置文件工具增加安全的文本追加能力，让 Agent 可以在不读取并重写整个文件的情况下记录日志或逐步生成内容。

## 设计

- 在 `fastagent.tools.file_io` 新增 `AppendFileSkill`，与现有 `ReadFileSkill` 和 `WriteFileSkill` 保持相同的构造方式。
- `run(path, content)` 复用 `_resolve_within_root`，确保目标始终位于配置的根目录内。
- 自动创建缺失的父目录，并以 UTF-8 文本模式追加内容；目标不存在时创建文件。
- 将新 Skill 从 `fastagent.tools` 公开导出，不改变现有接口，也不增加第三方依赖。
- 文件系统异常继续由 `Skill.execute()` 的统一错误结果处理。

## 验收标准

- 连续两次追加后，通过 `ReadFileSkill` 能按顺序读回完整内容。
- 可以向尚不存在的嵌套目录中的文件追加内容。
- `../` 等越界路径被拒绝，且不会在根目录外创建文件。
- 现有测试与新增测试全部通过。
