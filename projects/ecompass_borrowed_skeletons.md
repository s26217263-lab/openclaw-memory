# ecompass 可借鉴自动化骨架筛选（第一轮）

## 结论先说

我先不找“万能自治 agent”，而是找可借的骨架。第一轮筛完，最值得借的是三类：

1. **Orchestrator / Worker 架构**
2. **State machine / task queue 架构**
3. **Artifact / evidence tracking 架构**

不优先借的：
- 只会演示多 agent 对话的框架
- 只有漂亮状态流、没有验证机制的 demo
- 强依赖复杂云基础设施的重型方案

---

## 第一类：Orchestrator / Worker

### 借什么
- 一个主编排层负责：分步骤、定当前步骤、判断完成条件、上抛 blocker
- 多个执行层负责：大纲、初稿、编辑、存储等单步任务

### 为什么值得借
因为 ecompass 现在最大的问题不是“不会说”，而是：
- 它没形成稳定持续推进
- 它容易把进行时叙事当成结果
- 它一个 agent 包太多职责

### 借完之后怎么用
在 ecompass 里：
- **ecompass = orchestrator**
- 子步骤 = worker / step executor

这样 ecompass 不再负责“从头包到尾写一切”，而是负责：
- 任务进入
- 状态判断
- 下一步调度
- blocker 汇报

---

## 第二类：State machine / task queue

### 借什么
- 用任务池保存“还有哪些活没干完”
- 用状态机保存“当前跑到哪一步”
- 用 next_step / next_run_at 决定什么时候继续推进

### 为什么值得借
因为你现在最不满意的是：
- 你说一句，它动一下
- 你不说，它就像停住了

这不是人格问题，是**没有持续运行机制**。

### 借完之后怎么用
引入最小状态机：
- pending
- running
- blocked
- failed
- done

引入最小步骤流：
- intake
- outlining
- drafting
- editing
- storing
- done

这样任务就不是聊天记录，而是一个会继续存在的对象。

---

## 第三类：Artifact / evidence tracking

### 借什么
- 每一步都要有真实产物
- 每一步都要有完成验证
- 每一步都能挂到列表型面板

### 为什么值得借
因为这正好击中你最在意的商业逻辑：
- 不看过程
- 只看结果
- 要低管理成本

### 借完之后怎么用
每一步都挂上：
- artifact
- artifact_path
- updated_at
- blocker

验证规则：
- 没证据，不算完成
- 没产物，不准亮灯

---

## 不优先借的骨架

### 1. 纯多 agent 对话骨架
问题：
- 看起来热闹
- 但不天然带状态机
- 不天然带任务池
- 不天然带结果验证

### 2. 纯流程面板 demo
问题：
- UI 很好看
- 但底层不一定真在产出
- 容易变成“自动化演出”

### 3. 重型企业框架
问题：
- 太重
- 接入成本高
- 前期 ROI 不好

---

## 第一轮推荐采用的组合

### 推荐组合
**Orchestrator / Worker + Task Queue + Artifact Tracking**

这是最适合 ecompass 当前阶段的骨架组合，因为它满足：
- 能持续推进
- 能低带宽汇报
- 能只看结果
- 能以后再接网页面板

---

## 怎么接进 ecompass

### ecompass 角色定位
- ecompass = orchestrator
- 不再做叙事型 CEO
- 只负责：读任务、定步骤、验产物、更新状态、报 blocker

### 数据结构
- `task.json`
- `status.json`
- `outline.md`
- `draft_v1.md`
- `deliverable_v1.md`

### 面板
先只做列表：
- task_id
- current_step
- status
- artifact
- updated_at
- blocker

---

## 当前阶段判断

### 已确认适合借的
- orchestrator / worker 思路
- state machine / task queue 思路
- artifact / evidence tracking 思路

### 暂不建议引入的
- 大而全自治框架
- UI 先行方案
- 只会讲 agent 协作故事的 demo

---

## 下一步动作

1. 把这三类骨架继续落成 ecompass 的本地目录结构
2. 定义 `task.json` / `status.json` schema
3. 做最小 task runner 骨架
4. 让 ecompass 开始围绕 task queue 而不是围绕聊天推进

---

## 一句话结论

第一轮筛选结果已经出来了：

**ecompass 最值得借的不是“万能自治 agent”，而是 orchestrator-worker + state machine + evidence tracking 这三块骨架。**
