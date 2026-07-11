# 🎭 灵境 · 小说创作智能体系统

> 入口文件 — 加载此文件即启动灵境创作系统。

## 📋 当前项目

**转生深渊领主，我靠种田苟成邪神**
- 章节：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\章节\`（已写 82 章）
- 角色：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\人物\`
- 大纲：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\大纲\`
- 设定：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\设定集\`

### 快速启动

| 命令 | 功能 |
|------|------|
| `/novel:start` | 🚀 **启动创作向导** |
| `/novel:write` | 章节写作 |
| `/novel:review` | 章节审查 |
| `/novel:learn` | 学习作品 |
| `/novel:search` | RAG语义搜索 |
| `/novel:search:deep` | LCM+RAG深度查询 |

## 🧠 智能体系统

系统包含 **27 个专业智能体**，分布在 5 个部门。完整注册表见 `company/REGISTRY.md`：

| 部门 | 数量 | 核心Agent |
|:-----|:---:|:---------|
| 负责人部门 | 2 | manager·知识检索 |
| 写作部门 | 8 | 写手·角色·剧情·喜剧写手·恋爱写手·技法检索·创作设定·短故事 |
| 审核部门 | 8 | 审查官·润色师·设定质检·逻辑审核·文风审核·角色审核·剧情审核·时代审查 |
| 学习部门 | 4 | 外部学习·内部分析·电子书提取·本能进化 |
| 招募部门 | 5 | 差距分析·岗位设计·技能研发·集成·部署 |

## 📂 Skills 索引

### 写作部门 Skills（22个）

| 类别 | Skill | 说明 |
|:-----|:------|:------|
| 喜剧 | `comedy-scene-design` | 反高潮+反差笑点四段式 |
| 喜剧 | `comedic-dialogue` | 漫才对话+吐槽节奏 |
| 喜剧 | `defect-comedy-engine` | 缺陷三条件+标签化设计 |
| 喜剧 | `comedy-pattern-library` | 9种高级喜剧格式 |
| 喜剧 | `system-comedy` | 体制/法庭/阶级喜剧 |
| 剧情 | `plot-rhythm` | 反转/悬念/三重钩子/情感过山车 |
| 情感 | `emotional-arc-design` | 防御性幽默/名字开关/情感弧线 |
| 基础 | `chapter-writing` | 章节构建方法 |
| 基础 | `booming-plot` | 剧情引爆 |
| 基础 | `decoupled-writing` | 解耦写作法 |
| 基础 | `save-the-cat` | Save the Cat 节拍表 |
| 基础 | `snowflake-method` | 雪花法大纲 |
| 基础 | `short-story-quick` | 短故事快速创作 |
| 网文 | `webnovel-suspense` | 悬疑惊悚写作 |
| 网文 | `webnovel-trend` | 扫榜/趋势分析 |
| 网文 | `webnovel-goldfinger` | 金手指设计 |
| 网文 | `webnovel-submit` | 投稿/平台适配 |
| 发布 | `docx-publish` | DOCX生成与投稿 |

### 通用参考

| 路径 | 说明 |
|:-----|:------|
| `SUMMARY.md` | 命令/流程/规则速查 |
| `knowledge/theory/lcm-rag-prompt-templates.md` | 提示词模板（5模板+5功能） |
| `knowledge/rules/REGISTRY.md` | 全部规则清单 |

## 🔄 通用工作流

```
负责人把握方向 → 写作部门(写手+角色+剧情+喜剧+技法检索)
  → 审查官(打回循环，最多3轮) → 负责人汇总报告
```

详见 `company/process/chapter-creation.md`
