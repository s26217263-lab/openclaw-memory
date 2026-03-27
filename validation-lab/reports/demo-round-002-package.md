# validation-lab demo round-002 交付整理

## 1. 本轮 demo 的用途
这是一轮用于验证 validation-lab 是否真的能跑通的真实样例。
它不是模板空壳，而是已经完成一次从输入到结论的实际 round。

## 2. 本轮 demo 题目
美国市场首发：我们应该把首个自有品牌产品讲成“设计感/科技感的亲密生活方式产品”，还是讲成“直接功能导向的成人用品”？

## 3. 本轮 demo 的文件结构
### 输入文件
- `validation-lab/inbox/demo-us-launch-brief.md`

### round 文件
- `validation-lab/rounds/round-002/brief.md`
- `validation-lab/rounds/round-002/audience.md`
- `validation-lab/rounds/round-002/version-a.md`
- `validation-lab/rounds/round-002/version-b.md`
- `validation-lab/rounds/round-002/questions.md`
- `validation-lab/rounds/round-002/result-summary.md`
- `validation-lab/rounds/round-002/next-actions.md`
- `validation-lab/rounds/round-002/round-state.json`

## 4. 本轮最终结论
- 主方向：Version A
- 判断：Iterate
- 当前不建议直接上纯抽象版 A
- 需要先把 Version A 调成“更清楚但不低端”的中间版本，再进入真实市场验证

## 5. 这套样例以后怎么复用
以后要跑新的验证题，只要照着这套结构替换内容即可：
1. 把新题目写进 inbox
2. 新建一个新的 round 目录
3. 填 brief / audience / versions / questions
4. 输出 result-summary / next-actions / round-state
5. 最后沉淀到 reports

## 6. 这个样例证明了什么
它证明 validation-lab 已经具备最小可运行能力：
- 能接收真实问题
- 能组织成 round
- 能输出结构化结论
- 能给出 iterate 判断
- 能形成下一轮行动建议
