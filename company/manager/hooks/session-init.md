---
id: session-init
name: 会话初始化钩子
hook: session-init
stage: session
phase: session
runs-on: session-start
description: 会话初始化
created: 2026-06-21
updated: 2026-06-25
---

# 会话初始化钩子

## 触发时机
每次启动 Claude Code 进入项目目录时自动触发。

## 执行流程
1. 检测项目结构完整性
2. 恢复上次会话状态（检查点）
3. 加载当前进度（已完成章节、当前章节）
4. 检查待处理的审查/修改任务
5. 提示待处理事项

## 分卷检测
1. 检查当前创作进度，确认所属卷号（第1~40章为卷1，41~81为卷2，依此类推）
2. 检查 `.lcm/卷N/lcm.db` 是否存在（当前卷的 LCM 归档数据库）
3. 确保 `LCM_DATABASE_PATH` 环境变量指向当前卷的 lcm.db
4. 确认 `.rag/volume_mgr.py`（分卷管理工具）存在
5. 若 LCM 工具可用，执行 `lcm_status` 确认引擎正常运行

## LCM 数据库验证
1. 检查 LCM 数据库文件是否存在：`小说项目/转生深渊领主，我靠种田苟成邪神/.lcm/卷N/lcm.db`
2. 确保 `LCM_DATABASE_PATH` 环境变量已正确设置
3. 确认 `.rag/volume_mgr.py` 可正常调用

## 输出
- 项目状态摘要
- 待办事项列表
- 上次会话的上下文
