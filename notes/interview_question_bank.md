# Agent 应用工程师面试题库（精炼版）

## Agent 基础
- Agent vs Workflow：何时需要“自主决策”，何时用确定性流程？
- ReAct / Plan-Execute-Reflect 的差异与失败模式。
- 结构化输出（JSON Schema）为什么重要？如何做校验与修复？

## 工具调用/函数调用
- 工具接口设计：输入校验、权限、幂等、超时、重试。
- 多工具编排：串行/并行、依赖图、失败回滚/降级。
- Prompt 注入：工具描述最小化、allowlist、输出隔离。

## 可靠性与工程化
- 观测：step trace、输入输出落盘、token/cost统计。
- 成本：缓存、模型分层（fast/slow）、批处理。
- 评估：离线集构建、指标（成功率/格式合规率/人工满意度）。

## 你项目（report-agent）可被问到
- 如何从 git log 得到“可汇报的工作项”？（聚类/去噪/归并）
- 如何保证日报格式稳定？（schema + self-check + repair）
- 如何处理“没有提交但有产出”的情况？（notes 输入）
- 如何避免编造？（引用原始证据、unknown占位、拒答策略）
