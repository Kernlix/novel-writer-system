---
id: post-archive
name: 归档后清理
hook: post-archive
stage: post
phase: after-archive
department: manager
runs-on: archive-complete
description: 卷归档完成后，清理临时文件、更新索引、准备下一卷
---

# 卷归档后清理

## 执行步骤

1. 清理当前卷的工作目录中的临时文件
2. 更新 `company/REGISTRY.md` 中的当前卷信息
3. 创建下一卷的大纲文件骨架（如果尚未创建）
4. 通知用户归档完成，提示下一卷可开始
