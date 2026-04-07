# validation-lab 目录骨架说明

## 顶层定位

`validation-lab/` 是市场验证实验室的独立工作目录。
它与主线执行目录分开，目的是保证验证工作、重依赖试验、round 资料、日志与状态都能独立管理。

## 目录结构

- `inbox/`
  - 放主 agent 或人工提交进来的验证任务输入包
  - 这里是进入 validation-lab 的入口

- `rounds/`
  - 放每一轮验证过程的输入包、版本材料、中间判断与输出结果
  - 后续 `round-001/`、`round-002/` 等都会放在这里

- `reports/`
  - 放已经沉淀好的结构化结论
  - 更偏最终汇报物，而不是原始 round 工作草稿

- `tools/`
  - 放 validation-lab 自己的辅助脚本、桥接代码、未来可能的工具接入层
  - 如果以后接 MiroFish 或其他模块，优先从这里挂，而不是污染主系统根目录

- `logs/`
  - 放 validation-lab 自己的运行日志
  - 与 main / ecompass 日志分开

- `state/`
  - 放 round 状态、任务状态、当前活跃版本等结构化状态文件
  - 是这个实验室的“控制面”

- `sandbox/`
  - 放重依赖试验、临时 demo、隔离运行内容
  - 未来如果要试 MiroFish，这里是第一落点

## 当前原则

1. 先把目录边界分清，再往里填内容
2. 验证实验相关的脏活、试验活、重依赖，优先进 sandbox
3. 结构化输入进 inbox，结构化 round 资料进 rounds，结构化结论进 reports
4. 状态不要散落在文档里，后续统一收进 state
