# validation-lab 使用说明

## 这是什么

`validation-lab` 是市场验证实验室 agent。它的职责是在项目进入真实世界之前，承担低成本、多轮、结构化的市场验证与反馈闭环。

## 它的用途（5 类）

1. **验证定位** —— 这个说法用户能不能懂？会不会误解？
2. **比较版本** —— Version A / B / C 哪个更好？
3. **找风险** —— 最大的 adoption blocker 是什么？
4. **给修正建议** —— 下一轮要改什么？
5. **判断能否进真实市场** —— go / no-go / iterate

## 使用方式

### 第一步：把验证任务发进去

把以下内容整理成输入包，发进 validation-lab：

- 项目名
- 本轮验证目标
- 待验证假设
- 目标用户
- 当前版本材料（文案 / 页面 / 想法都可以）
- 成功标准
- 失败标准

格式参考：
- `validation-lab/inbox/input-template.md`
- 或直接用人话写，我来整理

### 第二步：等待验证结论

validation-lab 会按 round 机制跑一轮，输出：

- 关键发现
- 主要接受点 / 误解点
- 风险点
- 修正建议
- go / no-go / iterate 判断
- 下一轮唯一最值得验证的问题

### 第三步：读取结论

结论会出现在：
- `validation-lab/rounds/round-xxx/result-summary.md`
- `validation-lab/rounds/round-xxx/next-actions.md`

### 第四步：决定下一步

- **go** → 可以推进真实市场动作
- **iterate** → 先改一轮再验证
- **no-go** → 先暂停，方向性风险太大

## 怎么投喂任务

最简单的方式：
直接在「市场验证」群里用人话描述你的验证需求，validation-lab 会自动接收并组织 round。

或者：
把输入内容写入 `validation-lab/inbox/` 目录，我会自动读取并启动 round。

## 当前已跑过的真实 round

- `round-002`（美国市场首发品牌表达方向验证）
  - 结论：推荐 Version A，但需要先迭代
  - 判断：iterate

## 目录结构

```
validation-lab/
├── inbox/              ← 任务入口
├── rounds/             ← 每轮验证的输入/输出
├── reports/            ← 结构化结论沉淀
├── tools/              ← 辅助脚本
├── logs/               ← 运行日志
├── state/              ← 状态控制面
└── sandbox/            ← 重依赖试验区
```

## 已知边界

- 它只负责市场验证，不负责主线执行
- 它不能替代 main agent 做商业决策
- 它目前不支持 MiroFish 等外部工具接入（Phase 3 规划）
