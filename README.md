# AI Agent 转型基地（前端 → Agent 应用工程师）

目标：1 个月内完成可展示的“工程师日报/周报自动化 Agent”（CLI + 简 Web 预览），并准备面试题库与项目复盘。

## 项目：report-agent（工具编排自动化）

输入（本地/命令）：
- `git log`（今日/本周提交）
- 可选：本地 `notes/*.md`（手动补充的会议/学习/阻塞）

输出：
- `outputs/daily_YYYY-MM-DD.md`
- `outputs/weekly_YYYY-[W]WW.md`
- Web 预览：加载/编辑/导出（最小实现）

能力（面试可讲）：
- 工具调用（shell/git/文件）+ 结构化中间态（JSON）
- 规划-执行-自检（rewrite/critique）
- 可靠性：超时/重试/幂等/缓存
- 评估：离线用例集 + 成功率/格式合规率
- 观测：trace 日志、每步输入输出落盘

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=你的key
# 可选：export OPENAI_BASE_URL=https://api.siliconflow.cn/v1
# 可选：export OPENAI_MODEL=deepseek-ai/DeepSeek-V3.2
python report_agent.py --kind daily
python report_agent.py --kind weekly
```

## 目录约定

- `report_agent.py`：日报/周报 Agent（MVP）
- `web/`：TS Web 预览（后续）
- `notes/`：学习笔记/面试题库/复盘
- `outputs/`：生成的日报周报

## 30 天节奏（每天 1-2h）

- Week1：函数调用/结构化输出 + git/fs 工具 + 日报 MVP
- Week2：周报 + 自检重写 + 失败处理/超时重试
- Week3：CLI 稳定化 + 观测/回放 + 简 Web 预览
- Week4：题库 + 系统设计 + mock 面试 + 项目复盘稿
