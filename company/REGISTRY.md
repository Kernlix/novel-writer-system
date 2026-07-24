---
id: company-registry
name: 灵境AI公司注册表
type: company-org
description: 虚拟AI小说创作公司完整组织架构
updated: 2026-07-24 (batch 72, +2 skills, +2 upgraded)
---

# 🏢 灵境AI公司注册表

## 组织架构

```
负责人 (Manager)
├── 写作部门 (Writing Dept)
├── 审核部门 (Review Dept)
├── 学习部门 (Learning Dept)
├── 修错部门 (Debug Dept)
├── 招募部门 (Recruitment Dept)
└── 知识图书馆 (Knowledge Library)
```

---

## 部门总览

### 负责人部门 (Manager)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| manager | 负责人智能体 | 🏢 | 需求理解、任务分解、部门协调、质量把关 | 自动激活 |
| knowledge-retrieval | 知识检索智能体 | 🔎 | 统一LCM+RAG检索，写作前/审查时提供上下文 | Agent调用 |

**Skills:** `novel-setup`, `novel-discuss`, `archive`, `knowledge-graph`, `memory-system`, `progress-track`, `rag-search`, `knowledge-retrieval`, `obsidian-sync`, `probability-persuasion-narrative`, `wall-confrontation-tension`, `invisible-wise-ally`, `value-confrontation-climax`
**Hooks:** `session-init`, `session-end`, `pre-archive`, `post-archive`, `pre-discuss`

### 写作部门 (Writing)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| writer | 写手智能体 | ✍️ | 正文章节写作、场景描写、对话 | Agent(prompt=...) |
| character-designer | 角色设计师 | 👤 | 角色创建、关系网、成长弧光 | Agent(prompt=...) |
| plot-architect | 剧情架构师 | 📖 | 大纲规划、分卷、情节设计 | Agent(prompt=...) |
| humor-writer | 喜剧写手 | 😂 | 喜剧场景设计、吐槽节奏、缺陷引爆 | Agent(prompt=...) |
| romance-writer | 恋爱写手 | 🤍 | 恋爱喜剧感情线渐进写作、反高潮告白、行动替代告白 | Agent(prompt=...) |
| identity-suspense-writer | 身份悬疑写手 | 🎭 | 秘密身份作为跨章叙事引擎——多重误认、揭露时机管理、信息防火墙 | Agent(prompt=...) |
| pseudo-family-writer | 疑似家族写手 | 👨‍👧 | 非恋爱疑似家族关系——哥哥-妹妹/养父-养女/师徒如父子等疑似亲情动力学 | Agent(prompt=...) |
| skill-matcher | 技法检索Agent | 🧩 | 按章节类型智能匹配技法，输出推荐表 | Agent调用 |
| story-setup | 创作设定 | 🏗️ | 世界观、角色、剧情一体化设定 | `/novel:writing:world` |
| short-story | 短故事专项 | ⚡ | 中短篇快速创作→投稿 | `/novel:writing:short` |
| outline-guardian | 大纲守护者 | 🧭 | 监控章节与大纲一致性，防止偏离主线 | Agent(prompt=...) |
| timeline-architect | 时间线架构师 | ⏰ | 时间线设计、事件排序、时间矛盾检测、多线程时间管理 | Agent(prompt=...) |

#### Skills分册（共296个，12子目录）
> 📋 **快速查找**：[skills-index.md](skills-index.md) — 所有技能的核心机制摘要索引，≤20字指纹，用于快速判断新建/升级/跳过

**⚔️ 战斗/对抗 (battle/)** — 17个
`ammo-countdown-tension`, `bystander-combat-narrative`, `combat-choreography-narrative`, `cost-escalating-physical-crisis`, `existential-threat-reversal`, `fear-curve-power-display`, `former-foe-rescue`, `pre-battle-narrative-engine`, `process-violence`, `reverse-pursuit-strategy`, `ritualized-confrontation`, `sacrifice-as-weapon-narrative`, `survivor-punishment-mechanic`, `threat-narrative`, `three-threat-physical-stacking`, `ultimate-underdog-showdown`, `violent-rescue-narrative`

**📖 剧情/结构 (plot/)** — 51个
`body-as-message-carrier`, `booming-plot`, `chapter-writing`, `cognitive-failure-staircase`, `commitment-degradation`, `complete-reversal-twist`, `cross-chapter-distributed-revelation`, `cultural-symbol-chapter-title`, `deathbed-info-compression`, `decoupled-writing`, `dream-imperfect-restoration`, `dual-layer-gameplay`, `dual-layer-reversal`, `environmental-narrative-info-layer`, `environmental-state-chain`, `fairy-tale-framework-mapping`, `flashback-emotional-bomb`, `foreshadow-tragedy`, `foreshadowing-judgment-narrative`, `four-word-revelation`, `gold-quote-destiny-reversal`, `lesson-intertextual-contrast`, `minimal-info-max-impact`, `minimal-trust-confirmation`, `narrative-pacing-engine`, `narrative-rhythm-control`, `narrative-structure-techniques`, `outcome-before-rules-reversal`, `parallel-climax-threads`, `person-by-person-judgment`, `plot-rhythm`, `post-game-narrative`, `pressure-catalyst-leadership`, `prop-as-humanity-symbol`, `returning-character-worldbuilding-dump`, `beast-riding-trio`, `scene-as-weapon`, `scene-emotional-mapping`, `self-hypnosis-narrative`, `self-versus-self-nested-narrative`, `sensory-activation-marker`, `sensory-beat-narrative`, `sensory-inversion-prop`, `sensory-leading-scene-building`, `starry-imagery-brutalization`, `strategic-failure-narrative`, `three-cycle-escalation`, `triple-meaning-stacking`, `truth-layer-revelation`, `truth-nested-in-lie-deception`, `v-shaped-emotional-reversal`

**💬 对话技法 (dialogue/)** — 11个
`cognitive-overload-dialogue`, `comedic-dialogue`, `dialect-subtext-dialogue`, `dialogue-as-judgment`, `dialogue-as-warfare`, `dialogue-escalation-games`, `dialogue-info-planting`, `identity-reveal-dialogue`, `layered-deception-dialogue`, `philosophical-dialogue`, `pure-dialogue-scene`

**👻 恐怖/悬疑 (horror/)** — 21个
`benevolence-violence-narrative`, `body-part-concretization`, `closed-space-suspense`, `cognitive-dissonance-horror-dialogue`, `cognitive-horror`, `control-desire-driven-violence`, `criminal-confession-narration`, `document-as-horror`, `effect-without-explanation-suspense`, `everyday-horror-substitution`, `everyday-warm-horror-contrast`, `flat-cruelty-narrative`, `identity-suspense`, `mundane-amid-horror`, `poetic-terror-dialogue`, `progressive-animalization`, `progressive-madness-curve`, `rational-killing-intent-narrative`, `ritual-religious-suspense`, `sensory-substitution-narrative`, `zero-emotion-violence`

**💕 情感/恋爱 (emotion/)** — 17个
`accomplice-reconciliation`, `action-substitute-confession`, `death-monologue`, `emotional-anchor-object`, `emotional-arc-design`, `existential-alliance`, `guardian-motivation-narrative`, `guiding-light-extinction`, `love-triangle-romance`, `masochistic-sacrificial-character`, `master-apprentice-progression`, `promise-exposes-power`, `pseudo-family`, `reverse-dignity-charity`, `romance-anti-climax`, `romance-progression`, `vulnerable-confession-impact`

**♟️ 博弈/推理 (game/)** — 55个
`abnormal-reaction-instead-of-answer`, `ability-breaker`, `ability-channel-deception`, `blind-bet-info-strategy`, `coincidence-evidence-chain-reasoning`, `cold-knowledge-vs-omniscience`, `cognitive-baseline-trick`, `commander-role-design`, `correct-reasoning-wrong-premise`, `counter-intuitive-strategy`, `cross-team-progress-contrast`, `data-driven-crisis`, `dilemma-karnaugh-map`, `ensemble-game-narrative`, `five-steps-ahead`, `game-theory-narrative`, `hard-reasoning-narrative`, `hidden-motive-bomb`, `honest-deception`, `honest-manipulation`, `indirect-derivation-questioning`, `instinct-breaks-mind-reading`, `instinctive-deduction`, `knowledge-dimension-reduction`, `logic-paradox-behavioral-breaker`, `meta-game-rule-trap`, `meta-rule-gambling`, `meta-rule-side-bet`, `micro-expression-warfare`, `multi-party-debate-progression`, `negative-inference-deduction`, `omniscient-eye-deception`, `paradoxical-negotiation-gambit`, `performative-deduction`, `precedent-reasoning-strategy`, `probability-persuasion-narrative`, `pyramid-scheme-survival-rule`, `reasoning-anchor-shift`, `reverse-intention-deduction`, `reverse-rule-loophole`, `rule-as-weapon`, `rule-reconstruction-gambit`, `rule-silence-trap`, `sacrificial-bait`, `scent-moral-label-system`, `second-level-game-theory-inducement`, `second-order-deception-trap`, `sensory-subtraction-scene`, `signal-game-weakness-leverage`, `simple-question-destruction`, `subtraction-strategy`, `sunk-cost-reversal`, `team-decision-triangle-suspense`, `vague-directive`, `vortex-multi-party-game`

**👤 角色设计 (character/)** — 24个
`absent-protagonist-inner-world`, `anthropomorphic-object-character`, `character-fatigue-handover`, `character-weakness-narrative`, `child-moral-awakening-triple-arc`, `child-narrative-filter`, `created-being-existential-narrative`, `echo-refuser-narrative`, `everyday-contrast-narrative`, `everyday-cover-secret`, `evil-evolution-path-narrative`, `hero-declaration`, `identity-suspicion-narrative`, `infiltrator-villain-narrative`, `label-reversal-explosion`, `letter-character-narrative`, `mask-impersonation-conspiracy`, `reverse-character-design`, `rough-wisdom-character`, `save-the-cat`, `self-reflexive-identity-declaration`, `silent-bond-relationship`, `weakness-to-strength`, `white-sketch-character`

**🌍 世界观/超自然 (world/)** — 32个
`ability-awakening-progressive-reveal`, `ability-counter-system-narrative`, `ability-identity-value-trinity`, `ability-inversion-curse`, `afterlife-tripartite-narrative`, `belief-dependent-ability`, `belief-driven-disguise`, `binary-system-contrast`, `cross-time-self-synergy`, `demon-contract-reversal`, `existence-hierarchy-quantification`, `existential-crisis-escalation`, `existential-crisis-reversal`, `godhood-dwarfing`, `language-guide-ability-boost`, `memory-codon`, `memory-erasure-recovery`, `memory-identity-paradox-narrative`, `narrative-authority-contention`, `narrative-premise-negation`, `negation-paradox-narrative`, `reincarnation-growth-arc`, `reincarnator-psychology`, `self-hypnosis-protection-mechanism`, `sensory-key-memory-trigger`, `sensory-reversal-identity`, `shadow-narrative-tricks`, `shell-copy-existential`, `supernatural-awakening`, `three-layer-ability-reveal`, `time-loop-practical`, `triggered-personality-switch`

**😂 喜剧技法 (comedy/)** — 10个
`black-humor-title`, `cognitive-mismatch-comedy`, `comedy-pattern-library`, `comedy-scene-design`, `comedy-suspension-earned-payoff`, `comedy-tragedy-interweave`, `defect-comedy-engine`, `pain-comedy-narrative`, `system-comedy`, `theological-depravity-comedy`

**🔄 反转/揭示 (reversal/)** — 28个
`absence-as-reversal`, `absent-mirror-narrative`, `asymmetric-logic-conflict`, `cognitive-manipulation-narrative`, `cognitive-reversal-narrative`, `concept-pre-deployment`, `enemy-to-learner`, `false-hope-reversal`, `five-layer-continuous-reversal`, `four-layer-nested-reversal`, `host-as-player-reversal`, `identity-reversal-three-chapters`, `invisible-wise-ally`, `meta-twist-narrative`, `name-as-clue`, `named-quote-revelation`, `naming-dimensional-strike`, `natural-disaster-breaking-gameplay`, `performative-breakdown`, `perspective-drifting`, `reverse-provocation-trap`, `rule-staircase-revelation`, `rule-true-face-revelation`, `silent-knower`, `silent-preparatory-action`, `triple-nested-reversal`, `trust-credit-transfer`, `value-confrontation-climax`

**🔧 工具/技术 (meta/)** — 29个
`causal-retrospection-narrative`, `death-game-narrative`, `docx-publish`, `first-person-shameless-narration`, `frank-manipulation-narrative`, `game-scene-writing`, `isekai-culture-clash`, `machine-metaphor-collapse`, `market-stall-narrative`, `meta-narrative-reflection`, `meta-rule-destruction`, `numerical-anchor-info`, `physiological-psychology`, `power-display-leisure`, `protagonist-fantasy-deconstruction`, `psychological-game-depth`, `ring-information-chain-murder`, `short-story-quick`, `snowflake-method`, `space-limit-narrative`, `story-within-story`, `theory-revelation-narrative`, `timeline-design`, `unsentimental-finale`, `wall-confrontation-tension`, `webnovel-goldfinger`, `webnovel-submit`, `webnovel-suspense`, `webnovel-trend`

**Hooks:** `guard-runtime-write`, `pre-write`, `post-write`

### 审核部门 (Review)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| reviewer | 审查官 | 🔍 | 多维度质量审查（12项审查维度） | Agent(prompt=...) |
| polish | 润色师 | 🎨 | 去AI化（四步流水线：检测→标记→改写→验证）、文风统一、语言优化 | `/novel:review:style` |
| setting-qa | 设定质检员 | 🔬 | 设定逻辑质检、矛盾发现 | `/novel:review:logic` |
| era-consistency | 时代审查官 | 🏛️ | 技术/知识合理性审查 | `/novel:review:era` |
| logic-review | 逻辑审核员 | ⚖️ | 设定矛盾、时间线、因果链 | `/novel:review:logic` |
| style-review | 文风审核员 | ✨ | 文风统一、去AI化、阅读体验 | `/novel:review:style` |
| character-review | 角色审核员 | 🎭 | 人设崩坏、行为合理性 | `/novel:review:character` |
| plot-review | 剧情审核员 | 📊 | 节奏、爽点密度、情绪起伏 | `/novel:review:plot` |

**Skills:** `anti-ai-polish`, `consistency-check`, `plot-hole-check`, `banned-words`, `setting-qa`, `adversarial-review`
**Hooks:** `pre-review`, `post-review`, `adversarial-review`

### 学习部门 (Learning)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| external-study | 外部学习智能体 | 📚 | 学习优秀作品、提取技法 | `/novel:learn:study` |
| internal-analysis | 内部分析智能体 | 📝 | 分析反馈、创作结果、审核报告 | `/novel:learn:analyze` |
| epub-extractor | 电子书提取员 | 📦 | epub/mobi文本提取，按章分块 | Agent调用 |
| evolve-agent | 本能进化Agent | 🧬 | 聚类≥3条同domain本能，进化为正式知识 | 自动触发 |
| knowledge-pipeline | 知识管线Agent | 🔗 | 从分析结果自动提取技法→生成Skill→注册到Agent | `/novel:learn:pipeline` / 学习部门完成后自动触发 |
| **dimension-framework** | **维度分析Agent** | 📐 | 确定作品类型→选择/设计分析框架→输出维度文档→监督分析一致性 | `/novel:learn:dimension` / 学习开始时自动触发 |

**Skills:** `multi-agent-learning`, `style-learning`, `external-study`, `epub-to-text`, `story-deconstruction`, `knowledge-pipeline`
**Hooks:** `pre-learn`, `post-learn`

### 修错部门 (Debug)

| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| debug-agent | 修错智能体 | 🔧 | 根因分析、修复执行、知识库入库 | 自动激活（pre-commit报错时）/ 用户指派 |
| error-logger-agent | 错误记录智能体 | 📝 | 错误知识库维护、计数同步、条目归档 | 定期（pre-commit时）/ 手动 |
| debug-evolve-agent | 错误进化智能体 | 🧬 | 定期扫描 entries_since_baseline，达到阈值(≥3)后自动进化 | pre-commit时自动扫描 / 手动触发 |

**Skills:** `root-cause-analysis`, `error-entry-standard`
**Hooks:** `pre-debug`, `post-debug`

### 招募部门 (Recruitment)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| gap-analysis | 差距分析智能体 | 🔭 | 分析工作流、Agent质量、系统瓶颈 | `/novel:recruit:gap` |
| job-designer | 岗位设计智能体 | 📋 | 定义新Agent/Skill/Hook需求 | `/novel:recruit:job` |
| skill-engineer | 技能研发智能体 | 🔧 | 设计新Skill（用skill-template） | `/novel:recruit:skill` |
| agent-integrator | 智能体集成智能体 | 🔗 | 配置权限、知识库访问、协作 | `/novel:recruit:integrate` |
| skill-deployer | 技能部署Agent | 🔁 | 学习后自动部署新Skill到写作/审核部门 | 自动触发 |

**Skills:** `recruitment-workflow`
**Hooks:** `pre-recruit`, `post-recruit`

### 知识图书馆 (Knowledge Library)
见 `knowledge/REGISTRY.md`


## 错误知识库

> 系统自省能力——记录每一次错误，防止同类问题。

| 路径 | 用途 |
|:-----|:------|
| `knowledge/errors/entries/` | 每次错误的完整记录 |
| `knowledge/errors/categories/` | 7类根因定义与对策模板 |
| `knowledge/errors/root-causes.json` | 结构化根因数据 |
| `knowledge/errors/README.md` | 库门面+快速索引 |
