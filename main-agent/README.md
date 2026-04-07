# main-agent

主 Agent 的标准化任务池目录。

用途：
- 把原先散落在 `state/main_heartbeat_cache.json`、`logs/main_task_heartbeat.log`、daily memory 里的主控信息，同步成统一 task/state 结构
- 供总任务平台直接读取
- 不替换旧逻辑，先做兼容层，保证安全

目录：
- tasks/  标准任务定义
- state/  标准状态文件
- sync_main_agent.py  从现有 cache/log/memory 生成标准任务池

原则：
- 稳定优先，不做重型依赖
- 只做兼容同步，不侵入原 heartbeat 发送逻辑
- 发现异常优先记录日志，而不是自动做复杂修复
