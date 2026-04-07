# ecompass 项目目录说明

这个目录现在按“汇报 / 运行 / 归档”来分，不再让交付文件和底稿混在一起。

## 你最该看的文件

- 根目录汇报页：`/Users/palpet/.openclaw/workspace/ecompass_项目汇报页.html`
- 项目内汇报页：`/Users/palpet/.openclaw/workspace/ecompass/reports/ecompass_Kickstarter第一轮交付_汇报页.html`
- 桌面同步版：`/Users/palpet/Desktop/壮壮的ai助手文件/ecompass/ecompass_Kickstarter第一轮交付_汇报页.html`

## 当前目录结构

```text
ecompass/
├── app/           # 产品/网页原型
├── artifacts/     # 各任务的原始产物（outline / draft / deliverable）
├── dashboard/     # 状态面板
├── docs/          # 项目说明文档（brief / IA / content / preview / log）
├── logs/          # 运行日志
├── reports/       # 给人看的正式汇报 HTML / 交付页
├── state/         # 状态机文件
├── tasks/         # 任务定义与执行脚本
└── archive/       # 旧版本或历史文件（按需归档）
```

## 分类规则

### 1. reports/
放正式给人看的东西：
- HTML 汇报页
- 老板演示页
- 可直接打开汇报的单页文件

### 2. docs/
放项目说明底稿：
- PROJECT_BRIEF.md
- CONTENT.md
- IA.md
- PREVIEW.md
- LOG.md

### 3. artifacts/
放任务执行产物：
- outline.md
- draft_v1.md
- deliverable_v1.md
- done.txt

### 4. app/
放产品网页或交互原型。

### 5. state/ + tasks/
放自动化系统自身文件，不作为对老板的交付物。

## 默认交付规则

以后 ecompass 的正式交付，默认必须同时落三处：

1. `ecompass/reports/` 内保留项目正式版
2. workspace 根目录放一份中文名 HTML，方便直接找
3. 桌面项目文件夹同步一份，方便直接打开汇报

没完成这三步，不算真正交付。
