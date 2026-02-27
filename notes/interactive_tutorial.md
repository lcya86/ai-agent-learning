# 交互式转型教程：前端 → Agent 应用工程师（30天，每天1-2h）

规则：每天只做“任务卡”。你把产出（文件/命令输出/截图）贴回来，我再解锁下一天并给反馈。

你将掌握：工具调用、编排（Plan-Execute-Check）、可靠性（超时/重试/幂等）、评估（离线集/指标）、观测（trace）、基础RAG（选修）、以及面试表达。

## Week 1：LLM 工程基础 + 结构化输出

### Day1 环境与最小调用
- 任务：
  1) 用 pip 创建/激活虚拟环境（venv）
  2) 安装依赖：`pip install -r requirements.txt`
  3) 新建 `notes/day1_log.md`，记录：Python版本、pip版本、依赖安装是否成功
  4) 运行 `day1_hello_llm.py` 并把输出粘到 `notes/day1_log.md`
- 验收：
  - `notes/day1_log.md` 存在且包含以上信息

### Day2 结构化输出（JSON Schema）
- 任务：
  1) 新建 `day2_structured_output.py`
  2) 让模型按 pydantic schema 输出：`{"summary": str, "todos": [str], "risks": [str]}`
  3) 对输出做校验：校验失败时再次请求“修复为合法JSON”
  4) 产出：把一次成功与一次失败修复的raw输出保存到 `notes/day2_log.md`
- 验收：
  - 代码可运行
  - `notes/day2_log.md` 包含两次case

### Day3 工具调用：本地文件读写工具
- 任务：
  1) 写 `tools/fs_tools.py`：`read_text(path)`, `write_text(path, content)`, `list_md(dir)`
  2) 写 `day3_tool_fs.py`：给定 `notes/` 目录，生成“今日学习摘要.md”到 `outputs/`
- 验收：
  - `outputs/` 生成了文件

### Day4 工具调用：shell/git 工具
- 任务：
  1) 写 `tools/git_tools.py`：获取最近N条提交/按时间since
  2) 写 `day4_tool_git.py`：把git log转成结构化JSON（commit、date、msg）
- 验收：
  - JSON可解析，字段完整

### Day5 最小Agent编排：Plan → Execute
- 任务：
  1) 写 `agent/planner.py`：输入“目标+可用工具描述”输出计划（步骤数组）
  2) 写 `agent/executor.py`：按步骤调用工具，收集结果
- 验收：
  - 能完成一个固定目标（例如：生成今天的工作摘要）

### Day6 Check/Repair：自检与重写
- 任务：
  1) 写 `agent/checker.py`：检查输出是否满足格式与“有证据”
  2) 不满足则触发重写（最多2次）
- 验收：
  - trace里能看到check与rewrite

### Day7 复盘与面试表达
- 任务：
  1) 新建 `notes/week1_retro.md`：讲清你实现的“结构化输出+工具+编排+自检”
  2) 形成3分钟项目口述稿
- 验收：
  - 口述稿可直接用于面试

## Week 2：可靠性（超时/重试/幂等）+ CLI
Day8-14：把Week1的Agent包装成CLI，加入超时/重试/缓存/幂等；并做一组离线输入回放。

## Week 3：观测与评估 + 简Web预览
Day15-21：trace落盘、指标统计；最小Web预览（加载outputs并编辑导出）。

## Week 4：面试冲刺
Day22-30：高频题库刷题+系统设计（Agent平台/评估/成本）+ mock面试。

---

# 现在开始：Day1
把 `notes/day1_log.md` 完成后发我（粘贴内容即可）。
