# AI Agent 公司/项目架构研究报告

**研究目的**：为 ecompass 体系设计可持续扩展的多 agent 组织架构
**研究时间**：2026-03-28
**研究范围**：GitHub 高星项目 + 行业框架 + 企业架构理论 + OpenClaw 自身能力

---

## 一、核心结论（先给结论）

**推荐架构：Supervisor Pattern（主管模式）**

```
main agent（我 / 用户入口）
    ↓ 任务下发
project-supervisor（ecompass / 项目主导 agent）
    ↓ 调度
├── validation-lab（市场验证专家）
├── launch-prep（预热运营专家）
├── [future: supply-chain-agent]
├── [future: content-agent]
└── [future: seo-agent]
```

**和传统的关键区别**：
- 不是 ecompass 变大变成万金油
- 而是 ecompass 作为"项目主管"，通过调度专业 sub-agent 来完成工作
- sub-agent 之间通过文件约定通信，不直接相互调用

---

## 二、三大基础协调模式（来自 GitHub 高星框架）

### 模式 1：Chain（链式）

```
Agent A → Agent B → Agent C
```

**适用场景**：线性流程，后一步依赖前一步的输出
**代表框架**：LangGraph（状态机）、AutoGen（对话链）
**GitHub 热度**：LangChain ~116k stars
**弱点**：不适合有分支、有判断的复杂流程

### 模式 2：Router（路由）

```
User Input → Router Agent → [Agent A / Agent B / Agent C]
```

**适用场景**：任务分类后分发，同一个入口，不同处理逻辑
**代表框架**：LangChain LCEL、RAG + Router
**特点**：一个中央 agent 做分类决策，不做执行

### 模式 3：Supervisor（主管）⭐ 推荐

```
Supervisor
  ↓ delegate
[Worker Agent A] [Worker Agent B] [Worker Agent C]
  ↓ report back
Supervisor
```

**适用场景**：复杂任务、需要判断、多种专业能力的场景
**代表框架**：AutoGen Supervisor、CrewAI Hierarchical Crews
**GitHub 热度**：AutoGen（微软）+ CrewAI 22k+ stars
**特点**：
- 中央 supervisor 只负责调度和整合，不做具体执行
- 每个 worker agent 是独立专家
- 任务完成后结果汇报给 supervisor 汇总
- 这是企业级 AI 组织最接近真实的模式

---

## 三、行业权威框架参考

### McKinsey《The Agentic Organization》（2024）

麦肯锡提出"agentic organization"概念：
> AI 正在带来自工业革命和数字革命以来最大规模的组织模式转变。这个新范式将人类和 AI agent（虚拟和物理）联合，在几乎零边际成本下大规模并肩工作。

**五大支柱**：
1. Business Model（商业模式）
2. Operating Model（运营模式）
3. Governance（治理）
4. Workforce, People & Culture（人力与文化）
5. Technology & Data（技术与数据）

**对 ecompass 的启示**：ecompass 作为项目主导 agent，需要在这五个维度上都有对应的 agent 子系统支撑。单一 agent 不够用，需要多 agent 协作体系。

### Gartner《AI-First Startup Organizational Structure》

AI-First 公司典型结构：
- **CEO/战略层**：人类最终决策
- **COO/运营层**：AI agent 执行日常运营
- **Specialist Agents**：专业化任务处理
- **Orchestrator**：任务分发和结果整合

**特点**：扁平化、快速迭代、人类做判断、AI 做执行

### CIO《The AI Agent Orchestrator: The New CTO》

> AI agent orchestrator 是负责组织全部 AI agent 组合的端到端管理的执行角色。这类似于传统 CTO 的职责，但范围更广——不只是管技术，还要管 AI 决策质量和工作流。

**对 ecompass 的定位**：ecompass 实际上正在扮演"项目级 AI Orchestrator"的角色。

---

## 四、GitHub 高星框架分析

### LangChain（~116k stars）
**定位**：瑞士军刀，通用 LLM 应用开发框架
**优点**：生态最大，工具链最全，文档最完整
**缺点**：对自主 agent 来说偏"低级"，需要大量胶水代码
**适合**：需要灵活定制的复杂工作流

### AutoGen（微软，~35k stars）
**定位**：多 agent 对话框架
**优点**：微软背书，企业级，支持群聊（group chat）模式
**缺点**：概念较重，学习曲线陡
**适合**：需要 agent 之间真正对话协商的企业场景

### CrewAI（22k+ stars）
**定位**：角色扮演团队框架
**优点**：上手最简单，概念最接近人类团队，role/goal/backstory 清晰
**缺点**：相对较新，高级功能在快速迭代中
**适合**：快速原型和验证**推荐参考**：CrewAI 的 Role-Based Agent 设计最适合 ecompass 体系。它的核心理念——每个 agent 有清晰的角色、目标、背景故事——正是 ecompass 所需要的。

---

## 五、OpenClaw 的多 Agent 能力

OpenClaw 支持两种多 agent 架构：

### 方式 1：Workspace 隔离（当前使用）
```
Gateway
  ├── agent: main（我，当前入口）
  ├── agent: ecompass（独立 workspace）
  ├── agent: validation-lab（独立 workspace）
  └── [future agents]
```
**特点**：
- 每个 agent 有独立 workspace、memory、identity
- 通过文件（inbox）通信
- 适合"平级协作"，而非真正的"上下级"
- sub-agent 通过 `sessions_spawn` 启动，临时任务

### 方式 2：Supervisor 模式（推荐构建）

```
main agent（用户入口 / 协调层）
  ↓ spawn + 指令
ecompass（project-supervisor）
  ↓ spawn + 指令
├── validation-lab（specialist）
├── launch-prep（specialist）
└── [future: content-agent]
```

**OpenClaw 实现路径**：
1. ecompass 维持独立 agent 身份
2. 通过 `sessions_spawn` + `sessions_send` 与 sub-agent 通信
3. sub-agent 完成工作后汇报给 ecompass
4. ecompass 整合结果后向 main agent 汇报
5. main agent 最终向用户呈现

---

## 六、星巴克/麦当劳组织结构参考价值评估

### 麦当劳（高度标准化）
- **可借鉴点**：SOP 驱动，重复任务高度自动化 → 对应 agent 的"标准化工作流"
- **不可借鉴点**：层级森严，不适合 AI agent 的灵活调度

### 星巴克（体验驱动）
- **可借鉴点**：品牌文化渗透到每个触点 → 对应 agent 的"角色一致性"
- **不可借鉴点**：服务人员培训成本高 → 对应 agent 学习成本问题

### 真正的参考对象
更应该参考的是 **AI-Native 公司**，如：
- **Waymo**：多传感器融合 = 多 agent 协作决策
- **Stripe**：API-first，任务高度结构化 → 对应 agent 的标准化工具调用
- **Notion**：模块化，插件生态 → 对应 agent 的 skill 可插拔设计

---

## 七、适合 ecompass 的终极架构方案

### 架构总览

```
层 0：用户入口（main agent / 用户直接沟通）
    ↓ 任务分配
层 1：Project Supervisor（ecompass / 各项目主导 agent）
    ↓ 专业任务下发
层 2：Specialist Agents（validation-lab / launch-prep / [future]）
    ↓ 结果汇报
层 1：Project Supervisor（整合判断）
    ↓ 汇报
层 0：用户入口（最终结果呈现）
```

### ecomppass 作为 Project Supervisor 的职责

**必须拥有的能力（ecompass 的核心职责）**：
1. 任务拆解——把复杂任务拆成子任务，分发给正确的 specialist
2. 判断优先级——哪个先做，哪个后做
3. 结果整合——把 specialist 的输出整合成用户需要的结论
4. 决策升级——只有跨维度、不可逆、涉及资源分配的问题才上报给用户

**ecompass 不应该做的事**：
1. 自己做市场验证（→ 交给 validation-lab）
2. 自己做 Reddit 渗透（→ 交给 launch-prep）
3. 天天管执行细节（→ 让 specialist 自己跑）

### Specialist Agent 的设计原则

每个 specialist agent 必须是：
1. **独立可启动**——有自己独立的 workspace、identity、SOUL.md
2. **输入输出明确**——知道收什么格式，产出什么格式
3. **通过文件通信**——不直接互相调用，通过 inbox/artifact 文件交互
4. **有明确边界**——只做职责范围内的事，不越界

---

## 八、通信协议设计（核心）

### 任务下发协议（main → ecomppass）
```json
{
  "task": "Shenpan Kickstarter 预热方案制定",
  "deadline": "2026-04-01",
  "priority": "high",
  "context": "V4 已通过，GO to launch",
  "deliverable": "launch-prep inbox 中的任务包"
}
```

### 任务下发协议（ecompass → specialist）
```json
{
  "task": "制定 Shenpan Kickstarter 预热内容日历",
  "target_agent": "launch-prep",
  "context_file": "ecompass/projects/shenpan/context.md",
  "output_file": "launch-prep/inbox/shenpan-prewarm-plan.md",
  "deadline": "3 days"
}
```

### 结果回报协议（specialist → ecomppass）
```json
{
  "from": "launch-prep",
  "task_id": "shenpan-prewarm-001",
  "status": "done",
  "output_file": "launch-prep/artifacts/shenpan-prewarm-calendar.md",
  "summary": "预热内容日历已完成，含 4 周计划",
  "blockers": ["无 Reddit 账号", "需要确认 email platform"],
  "escalate": true
}
```

---

## 九、OpenClaw 现有能力的评估

**已经支持的**：
- ✅ 多 agent 独立 workspace（ecompass、validation-lab）
- ✅ subagent spawn（临时任务）
- ✅ sessions_send（跨 agent 通信）
- ✅ 共享 skills（~/.openclaw/skills/）
- ✅ 心跳脚本（task heartbeat）

**需要补充的**：
- ⚠️ ecompass 没有系统级"spawn + 等待结果"的自动化（目前是手动 sessions_spawn）
- ⚠️ specialist agent 的 inbox/artifact 目录规范还没建立
- ⚠️ 缺少正式的"任务下发 → 执行 → 回报 → 整合"的循环机制

---

## 十、最终推荐方案（分阶段）

### 阶段 1（现在）：建立基础通信协议
- 建立 `ecompass/inbox/` 和 `specialists/*/inbox/` 目录规范
- 制定任务下发/回报的模板
- ecompass 学会用 sessions_send 向 specialist 发任务

### 阶段 2（1-2周后）：建 launch-prep specialist
- 创建 launch-prep agent（Kickstarter 预热专家）
- 建立 ecompass → launch-prep 的任务下发流程
- 跑一个真实任务验证通信协议

### 阶段 3（持续）：扩展 specialist 池
- 按需增加新的 specialist（content-agent、seo-agent 等）
- 不需要的时候就保持空闲，不浪费资源

### 核心原则
> **ecompass 不变大，ecompass 变聪明。变大的是 specialist 池，不是 supervisor。**

---

## 附录：关键参考资源

| 资源 | 类型 | 链接 |
|------|------|------|
| CrewAI | GitHub 22k+ | github.com/crewAIInc/crewAI |
| AutoGen（微软）| GitHub 35k+ | microsoft.github.io/autogen |
| LangGraph | GitHub 状态机 | langchain.com |
| McKinsey: Agentic Organization | 报告 | mckinsey.com |
| Azure: AI Agent Design Patterns | 架构指南 | learn.microsoft.com |
| Google Cloud: Choose Agent Pattern | 决策指南 | docs.cloud.google.com |
| OpenClaw Multi-Agent 文档 | 官方 | docs.openclaw.ai/concepts/multi-agent |
