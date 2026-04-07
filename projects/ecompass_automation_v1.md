# ecompass 自动化执行系统 V1 方案

## 1. 目标

先做一个最小可运行闭环：

**输入一个任务 → 自动产出一份可交付文档 → 列表面板实时反映状态**

V1 不追求全自动平台，不追求漂亮网页，先验证三件事：
1. 流程真的能自动流转
2. 每一步都有可验证产物
3. 面板状态和真实执行一致

---

## 2. V1 范围

### 输入
- task_id
- 任务名
- 目标
- 输出类型（默认：文档）
- 截止时间
- 备注（可选）

### 输出
- `outline.md`
- `draft_v1.md`
- `deliverable_v1.md`
- `status.json`
- 列表型状态面板（可由 markdown / json / table 驱动）

---

## 3. V1 流程链

### Step 1: intake
接收任务并创建任务目录。

产物：
- `task.json`

完成条件：
- 任务目录创建成功
- 输入字段完整写入

### Step 2: outlining
自动生成大纲。

产物：
- `outline.md`

完成条件：
- 文件存在
- 至少 3 个一级标题
- 标题与任务目标相关

### Step 3: drafting
基于大纲生成第一稿。

产物：
- `draft_v1.md`

完成条件：
- 文件存在
- 字数达到最低阈值
- 各一级结构下有正文

### Step 4: editing
对第一稿进行整理、收束、交付化。

产物：
- `deliverable_v1.md`

完成条件：
- 文件存在
- 结构完整
- 可直接给人查看

### Step 5: storing
把交付物存到指定位置。

产物：
- 存储路径 / 云文档链接

完成条件：
- 文件真实存在于目标位置
- 链接或路径可验证

### Step 6: status_update
更新状态面板。

产物：
- `status.json`
- 列表型面板记录

完成条件：
- 当前步骤、产物、时间戳、状态已刷新

---

## 4. 列表型面板字段设计

V1 先不做网页，只维护统一状态结构。

### 核心字段
- `task_id`
- `task_name`
- `goal`
- `current_step`
- `status`（pending / running / blocked / failed / done）
- `artifact`
- `artifact_path`
- `updated_at`
- `deadline`
- `blocker`
- `next_step`

### 期望展示效果
可以先用 markdown table / json list：

| task_id | task_name | current_step | status | artifact | updated_at | blocker |
|---|---|---|---|---|---|---|
| ec-001 | 首页方案V1 | editing | running | draft_v1.md | 11:20 | 无 |

---

## 5. 状态机

### 合法状态
- `pending`
- `running`
- `blocked`
- `failed`
- `done`

### 状态流转
- pending → running
- running → blocked
- running → failed
- running → done
- blocked → running
- failed → running（允许人工恢复）

### 原则
- 没有产物，不允许标记为 done
- 没有 blocker 描述，不允许标记为 blocked
- 没有失败原因，不允许标记为 failed

---

## 6. 结果验证机制

每一步不能靠“口头完成”，必须靠验证。

### outlining 验证
- 文件存在
- 标题数量达标

### drafting 验证
- 文件存在
- 字数不为空
- 结构与大纲对应

### editing 验证
- 文件存在
- 交付版结构完整

### storing 验证
- 文件路径可访问 / 文档链接有效

### 总原则
**没有证据，不算完成。**

---

## 7. blocker 机制

只有两类输出允许打扰用户：
1. 已产出结果
2. 明确 blocker

### blocker 示例
- 目标定义出现二选一分叉
- 输出格式需要用户拍板
- 外部系统写入失败
- 缺少必要资料

### blocker 输出格式
- 结果：当前卡在哪一步
- 状态：blocked
- 证据：当前已有产物 / 错误信息
- 阻塞：需要用户拍板的问题

---

## 8. 异常与接管机制

### 自动重试
- 每一步最多自动重试 2 次

### 触发 blocked
- 连续两次失败
- 产物为空
- 外部写入失败
- 目标信息缺失

### 触发人工接管
- 同一步持续失败
- 目标本身不明确
- 外部依赖不可用

---

## 9. ecompass agent 在 V1 中的角色

ecompass 不再扮演“会说话的 CEO”，而是：

## orchestrator / 编排器

职责：
- 接收任务
- 判断当前应执行哪一步
- 校验产物是否真实完成
- 更新状态
- 只在 blocker 时上抛

不再做：
- 长篇管理汇报
- 复述规则
- 用状态口号冒充结果

---

## 10. 未来网页面板如何接

V1 先保证 `status.json` / 列表数据结构稳定。

未来网页面板直接读取这些字段即可展示：
- 当前步骤
- 已完成步骤
- 当前产物
- 是否异常
- 下一步

也就是说：
**先做真实状态流，网页只是展示层。**

---

## 11. 本周执行建议

### Day 1
- 定义任务目录结构
- 定义 `task.json` / `status.json` 结构
- 跑通 intake → outlining

### Day 2
- 跑通 outlining → drafting → editing

### Day 3
- 跑通 storing 和状态更新

### Day 4
- 补异常处理与 blocker 机制

### Day 5
- 用 1 个真实任务做端到端演示

---

## 12. 一句话结论

V1 的核心不是“看起来自动化”，而是：

**任务进入后，系统能稳定地产出一个可验证结果，并且列表面板状态与真实执行一致。**
