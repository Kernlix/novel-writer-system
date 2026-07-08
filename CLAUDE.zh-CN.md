# Claude Code 配置 — 灵境小说创作系统

## 自动加载
当你在本目录打开 Claude Code 时，系统自动就绪。

## 工作路径约定
- 系统仓库：`company/` — **虚拟AI公司**（5部门 + Skills + Hooks）
- 知识库：`knowledge/` — **知识图书馆**
- 工具：`.rag/` — RAG引擎/分卷管理/Reranker
- 小说项目：`D:\allproject\小说项目\{project}\`

## 系统结构
- `company/` — 智能体定义（5个部门+Agent+Skill+Hook）
  - `manager/` — 负责人部门
  - `writing/` — 写作部门
  - `review/` — 审核部门
  - `learning/` — 学习部门
  - `recruitment/` — 招募部门
- `knowledge/` — 知识图书馆（统一知识库）
- `.rag/` — 工具集成（RAG引擎/分卷管理/Reranker服务）
- `.era-knowledge/` — 时代背景知识库（按项目）
- `protocols/` — 协议文档
- `templates/` — 组件创建模板

## LCM + RAG 分卷集成
详见主 `CLAUDE.md` 的 LCM 与 RAG 章节。

## 推荐设置
> 建议关闭思考模式 (thinking mode off)
