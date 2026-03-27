# validation-lab 最小运行路径

## 目标

把 validation-lab 从“只有目录和模板”推进到“有最小运行路径”。

这里的最小运行路径不是复杂自动化，而是先把：
- 任务从哪里进
- round 怎么起
- 结果怎么出
- main 怎么接

这 4 件事固定下来。

---

## 一、输入入口

所有新验证任务先进入：

- `validation-lab/inbox/`

推荐最小输入包：
- `brief.md`
- `audience.md`
- `hypothesis.md`
- `success-failure.md`
- `versions.md`

如果资料不全，也允许先只有 `brief.md`，但不能直接跳过输入定义。

---

## 二、如何启动一个 round

当 inbox 中出现一个新验证包时：

1. 分配新的 round 目录，例如：`round-002/`
2. 把必要输入复制或整理进该 round 目录
3. 初始化 `round-state.json`
4. 把 round 状态置为 `running`
5. 进入 comparison / judgement / next-actions 流程

最小原则：
- 一个验证请求，对应一个 round
- 一个 round，至少有输入、比较、结论、下一步

---

## 三、round 的最小输出

每个 round 跑完后，至少要产生：

- `result-summary.md`
- `next-actions.md`
- `round-state.json`

如果已经形成稳定结论，再把结论沉淀到：

- `validation-lab/reports/`

---

## 四、与 main 的交接方式

`main` 负责：
- 给出业务目标
- 决定要验证什么命题
- 接收 validation-lab 的结论
- 决定是否推进到真实市场

`validation-lab` 负责：
- 接收验证输入
- 组织 round
- 输出结构化验证结论
- 给出 go / no-go / iterate 建议

最小交接规则：
- `main` 不直接跳进 round 内部做判断
- `validation-lab` 不替代 `main` 做最终商业决策
- 双方通过结构化输入包和结构化结论交接

---

## 五、最小运行闭环

最小闭环是：

1. `main` 或人工把验证任务放进 `inbox/`
2. validation-lab 创建一个新的 `round-xxx/`
3. 补齐输入材料
4. 做版本比较与风险判断
5. 输出 `result-summary.md` 和 `next-actions.md`
6. 给 `main` 返回 go / no-go / iterate 结论
7. 如有必要，进入下一轮 round

---

## 六、当前阶段的边界

当前只做“能跑通的最小骨架”，不做：
- 重依赖安装
- MiroFish 接入
- 多服务自动编排
- 复杂消息总线

先确保这个实验室在不用外部复杂工具时，也能独立跑一轮验证。
