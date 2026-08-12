# Harness 技术知识补充

> 
> 说明：Harness 在这里特指**Agent 领域的调度 Harness**，是自研 Agent 系统里的调度管理层，属于智能体工程化组件，不属于开源标准框架。

## 1. 什么是 Agent‑Harness

Harness 是多智能体系统的**统一调度中枢层**，介于大模型、Skill 工具集、外部数据源之间。
核心定位：**管控 Agent 生命周期、路由任务、管理工具调用、维护上下文、做权限与限流，把原始 LLM 能力和业务 Skill 解耦**。

> 
> 和 LangGraph / AutoGen 的区别：
> 
> 
> - LangGraph：侧重图编排，写业务流程逻辑；
> - AutoGen：侧重多 Agent 对话交互；
> - Harness：偏向平台化管控，做统一网关、任务调度、调用审计、资源管控，上层再对接 Agent/LLM。

## 2. Harness 核心作用

1. **Agent 生命周期管理**：创建会话、保存会话记忆、会话销毁、超时回收，避免内存泄露。
2. **Skill 统一调度入口**：接收 LLM 输出的 Function‑Calling 请求，路由到对应的 Skill 执行，做参数校验、入参过滤、异常捕获。
3. **协议适配**：对接 MCP、OpenAI function‑call 格式，屏蔽不同大模型输出格式差异。
4. **可观测与管控**：记录每次调用 Token、耗时、异常日志，限流、鉴权，方便排查线上问题。
5. **任务分发**：多 Agent 场景下，把业务任务分配给对应智能体，协调多个 Agent 之间的消息流转。

## 3. Harness 与 Skill、Memory、LLM 的协作关系

```
业务请求 → Harness调度层
    ↓
1.读取Memory上下文（历史会话、业务记忆）
    ↓
2.组装Prompt，转发请求给LLM
    ↓
3.解析LLM返回的工具调用指令
    ↓
4.Harness路由调用对应的Skill（数据库查询、爬虫、报告生成等）
    ↓
5.拿到Skill执行结果，回写Memory
    ↓
6.整理结果返回给用户
```

- **Skill**：最小可执行能力单元，如查询数据库、生成文档、调用接口，只负责干活，不做调度。
- **Harness**：不实现具体业务能力，只负责**调度、校验、流转、管控**。
- **Memory**：由 Harness 读写维护，统一管理短期会话记忆、长期业务记忆。

## 4. 完整使用流程

### 步骤 1：注册 Skill 到 Harness

将各个业务 Skill（函数、工具）向 Harness 注册，提交工具描述、入参 schema、权限标签。
Harness 内部维护一份 Skill 注册表，知道每个工具名称、参数格式、允许哪些会话调用。

### 步骤 2：用户发起业务请求

请求进入 Harness，Harness 加载该会话对应的 Memory 上下文，拼接历史信息。

### 步骤 3：封装请求，调用大模型

Harness 组装 system prompt + 用户 query + 可用 Skill 列表，向 LLM 发送请求。

### 步骤 4：解析 LLM 输出，拦截与校验

解析 Function‑Calling 输出；Harness 做参数合法性校验、安全过滤、权限判断；
参数非法直接拦截，不向下执行 Skill。

### 步骤 5：路由执行 Skill

根据工具名称，从注册表找到对应 Skill，传入参数执行。
捕获 Skill 抛出的异常，包装错误信息，不直接透传底层堆栈给大模型。

### 步骤 6：结果回写 Memory，循环推理

将 Skill 返回结果写回 Memory；
如果 LLM 还需要继续调用工具，Harness 自动循环上述流程；
不需要继续工具调用，则整理最终自然语言结果返回前端。

### 步骤 7：会话结束 / 超时回收

Harness 清理临时资源，持久化重要记忆，记录全链路调用日志。

## 5. 为什么项目中要引入 Harness，而不是直接 LangGraph 硬编码

1. **解耦业务与调度逻辑**：Skill 只写业务，调度、鉴权、日志、限流全部收拢在 Harness，新增工具不需要改动 Agent 主逻辑。
2. **多 Agent 场景更友好**：业务变复杂，多个 Agent 协同的时候，统一由 Harness 做任务分发，不会出现到处写消息转发的代码。
3. **线上可观测性**：所有 LLM、Skill 调用全部过 Harness，统一埋点统计 token、成功率、耗时，方便优化成本和排查故障。
4. **屏蔽大模型差异**：不同厂商 Function‑call 格式不一样，Harness 做一层适配，切换模型上层业务几乎不用改动。

## 6. 注意点

1. Harness 属于**工程封装层，不是开源标准组件**，项目中一般为自研模块，市面上没有直接 pip 安装的 harness 包。
2. 小 Demo 不需要 Harness；适合生产环境、多工具、多 Agent、需要管控审计的项目。
3. 不要把业务逻辑写进 Harness，Harness 只做调度流转，业务逻辑下沉到 Skill。