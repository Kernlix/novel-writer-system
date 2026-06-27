---
id: post-all-check
name: 全流程完整性检查钩子
hook: post-all-check
stage: post
phase: write
runs-on: after-all-checks
description: 全流程完整性检查——防止跳步骤
severity: blocking
created: 2026-06-21
updated: 2026-06-25
---

# 全流程完整性检查

> 每次章节创作完成后，逐项验证全流程是否走完。**缺任何一项都视为流程未完成，不得跳过。**

## 检查清单

### 1. 写前准备（Pre-write）
- [ ] 章纲已加载（`.story-system/chapters/chapter_XXX.md` 或大纲对应章节）
- [ ] 角色状态已加载（`人物/` 对应角色档案）
- [ ] 知识边界已检查（`知识边界/character-knowledge-boundary.md`）
- [ ] 字数预算已规划（拆解为 3~5 个场景，预估总和 ≥ 2200）

### 2. 章节正文
- [ ] 章节文件已写入（`章节/第XX章-标题.md`）
- [ ] 字数在 2000~4000 范围内（仅计中文）
- [ ] 破折号 ≤ 3 处
- [ ] 文件名格式正确（`第X章-英文标题.md`）
- [ ] 叙事技法运用合理（群像差异化/悬念分层/信息差利用）
- [ ] 关键场景有感官锚点（至少2种感官）
- [ ] 【素晴学】对话有角色缺陷驱动的碰撞——每段对话至少有2次因角色个性碰撞，非纯信息传递
- [ ] 【素晴学】有反高潮/幽默逃逸口——严肃情节后是否有符合角色性格的轻松节拍或荒诞转折
- [ ] 【素晴学】对话密度合理——无长段独白，单次发言控制在2-3句
- [ ] 【素晴学】剧情有日常锚点——检查剧情推是否被角色自身的日常困境（经济/社交/生活）驱动而非纯外部事件
- [ ] **标题质量**：标题准确反映本章内容且有吸引力（参考 `knowledge/writing/title-design-patterns.md`）
- [ ] **标题长度**：5-15字范围内（不超过20字）

### 3. 写后文档（Post-write）
- [ ] 章节摘要已生成（`章节摘要/第XX章摘要.md`）
- [ ] 审查报告已生成（`审查报告/chapter_XXX.review.json`）
- [ ] 章节跟踪文件已更新（`.story-system/chapters/chapter_XXX.md`）

### 4. 数据更新
- [ ] 角色状态已更新（`人物/` 对应角色——至少腐化值、等级）
- [ ] 伏笔追踪已更新（`大纲/伏笔追踪.md`——回收和新增）
- [ ] 悬念层级表已更新（短期+中期+长期悬念）
- [ ] 创作进度已更新（`.story-system/progress.md`）
- [ ] RAG 已重建索引

### 5. 设定一致性
- [ ] 角色没有说出超出知识范围的话（回查 `知识边界/`）
- [ ] 没有与大纲冲突的情节
- [ ] 新产生的知识已按分类规则放入正确位置
- [ ] 对话/叙事比例合理（非纯对话墙或纯叙述）

## 验证命令

```bash
# 一键验证脚本（调用 post-write-runner.py + 额外检查）
python .story-system/post-write-runner.py

# 手动验证项（脚本无法自动检查的）：
# 1. 知识边界检查：确认角色言行未越界
# 2. 大纲对照：章节内容与大纲无冲突
# 3. 伏笔追踪：已回收+新埋的伏笔都已记录
```

## 违规处理

如果检查发现任何缺失项：
1. **立即补全缺失步骤**，不得以"下次注意"为由跳过
2. 补全后重新运行检查，直到全绿通过
3. 缺项超过 3 次时，重新阅读本文件

## 速查命令

每次写完后在终端运行：

```bash
cd D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神

echo "=== 1. 章节文件 ==="
ls 章节/第7*.md 2>/dev/null | tail -3

echo "=== 2. 摘要 ==="
ls 章节摘要/第7*.md 2>/dev/null | tail -1

echo "=== 3. 审查报告 ==="
ls 审查报告/chapter_07*.json 2>/dev/null | tail -1

echo "=== 4. 跟踪文件 ==="
ls .story-system/chapters/chapter_07*.md 2>/dev/null | tail -1

echo "=== 5. 字数/破折号 ==="
python -c "import re; t=open('章节/第$(ls 章节/*.md | tail -1 | grep -oP '\d+').md',encoding='utf-8').read(); b=re.sub(r'^---.*?---\s*','',t,flags=re.DOTALL); print(f'字数:{len(re.findall(r\"[一-鿿]\",b))} 破折号:{b.count(\"——\")}')"
```
