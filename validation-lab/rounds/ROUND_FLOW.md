# validation-lab round 流转规则

## round 标准阶段

1. `brief`
   - 明确本轮验证目标
   - 明确要回答的问题

2. `inputs-ready`
   - audience / hypothesis / versions / success-failure 都已准备好

3. `comparison`
   - 对 Version A / B / C 做结构化比较
   - 看接受点、误解点、风险点

4. `judgement`
   - 汇总关键发现
   - 输出 go / no-go / iterate 判断

5. `next-actions`
   - 明确下一轮要改什么
   - 明确是否进入真实世界验证

6. `done`
   - 本轮资料与结论归档

## 状态流转

- `pending` -> `running`
- `running` -> `blocked`
- `blocked` -> `running`
- `running` -> `done`

## round 完成标准

一个 round 只有满足以下条件才算 done：
- 输入材料齐全
- 至少完成一次版本比较
- 有结构化结论
- 有 next-actions
- 有 go / no-go / iterate 判断
