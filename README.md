# 📚 LingJing — Novel Creation Multi-Agent System / 灵境 · 小说创作智能体系统

> **LingJing** — An AI-powered novel creation system integrating multi-agent collaboration, modular Skills, and a knowledge graph.
>
> **灵境** — 集多智能体协作、模块化 Skills、知识图谱于一体的 AI 小说创作系统。

A unified creative toolbox built from the best open-source novel-writing projects on GitHub, tailored for you.
整合 GitHub 上最优秀的开源小说写作项目精华，为你量身打造的统一创作工具箱。

---

## ✨ Features / 系统特色

| 🇬🇧 Feature | 🇨🇳 特性 | Description / 说明 |
|:--|:--|:--|
| 🧠 **Multi-Agent Collaboration** | 🧠 **多 Agent 协作** | 7 specialized agents working together / 7 个专业智能体分工协作 |
| 🧩 **Modular Skills** | 🧩 **模块化 Skills** | 30+ independent skills covering the full creative workflow / 30+ 独立 skill 覆盖创作全流程 |
| 📖 **Dual-Mode Support** | 📖 **双模式支持** | Long-form novel pipeline + short story rapid creation / 长篇小说流水线 + 短篇快速创作 |
| 🎭 **De-AI Engine** | 🎭 **去AI化引擎** | Multi-layer detection and polish for natural, human-like output / 多层检测与润色，输出自然流畅 |
| 📊 **Knowledge Graph** | 📊 **知识图谱** | Persistent relationships between characters, locations, and events / 角色/地点/事件关系持久化 |
| 🌐 **Multi-Platform** | 🌐 **多平台适配** | Optimized for Qidian, Fanqie, Jinjiang, and more / 起点/番茄/晋江等平台优化 |

---

## 🚀 Quick Install / 快速安装

### Windows
```powershell
iex "& { $(irm https://raw.githubusercontent.com/nosoultool/novel-writer-system/main/install.ps1) }"
```

### macOS / Linux
```bash
bash <(curl -s https://raw.githubusercontent.com/nosoultool/novel-writer-system/main/install.sh)
```

---

## 📖 7 Ways to Use / 7 种使用方式

### 🥇 Reasonix (Recommended / 推荐)

```bash
/novel-writer I want to write a cultivation novel     # 我想写一本修仙小说
/novel-writer /novel:world    Build a world           # 搭建世界观
/novel-writer /novel:write    Write the body          # 写正文
```

> 🇬🇧 See [REASONIX.md](REASONIX.md) for detailed usage.
>
> 🇨🇳 详细用法见 [REASONIX.zh-CN.md](REASONIX.zh-CN.md)

### 🥇 Claude Code (Full Feature / 全功能推荐)

```bash
cd novel-writer-system
claude
# Enter /novel:start  / 输入 /novel:start
```

### 🥈 Codex CLI · 🥉 Cursor IDE · 🏅 Windsurf · 📱 ChatGPT/Kimi · 📄 Manual Reading / 手动阅读

🇬🇧 See platform-specific instructions for details.
🇨🇳 详见各平台说明。

---

## 📜 Command Reference / 完整命令一览

```
🚀 创作流程 / Writing Flow      🌍 设定管理 / World Building     📋 大纲 / Outline
  /novel:start                     /novel:world                    /novel:outline
  /novel:discuss                   /novel:characters               /novel:snowflake

✍️ 写作 / Writing                 🔍 审查 / Review                 🎨 润色 / Polish
  /novel:write                     /novel:review                   /novel:anti-ai
  /novel:decoupled                 /novel:check                    /novel:booming
                                   /novel:quality                  /novel:style-learn
                                   /novel:deslop
                                   /novel:plot-hole

📦 网文专项 / Web Novel            🛠️ 工具 / Tools
  /novel:hook                      /novel:archive
  /novel:shuang                    /novel:knowledge
  /novel:trend                     /novel:memory
  /novel:goldfinger                /novel:progress
  /novel:submit
```

---

## 🙏 Acknowledgements & License / 致谢与许可证

### License / 许可证
🇬🇧 This system is licensed under the **MIT License** — you are free to use, modify, and distribute it, including for commercial purposes.
🇨🇳 本系统采用 **MIT License** — 你可以自由使用、修改、分发，包括商业用途。

### Design Inspiration / 设计启发
🇬🇧 The design of this system was inspired by the following open-source projects:
🇨🇳 本系统的设计思路受以下开源项目启发，在此致谢：

| 🇬🇧 Project / 🇨🇳 项目 | License / 许可证 | 🇬🇧 Contribution / 🇨🇳 贡献 |
|:--|:--|:--|
| [awesome-novel-skill](https://github.com/modoojunko/awesome-novel-skill) | GPL-3.0 | Multi-Agent collaboration workflow & memory system / 多 Agent 协作工作流与记忆系统 |
| [tianming-skill](https://github.com/zy-zmc/tianming-skill) | CC BY-NC-SA 4.0 | Modular prompt engineering & quality gates / 模块化提示词工程与质量门禁 |
| [chinese-webnovel-skills](https://github.com/tance-mang/chinese-webnovel-skills) | MIT | 33 web novel skills & platform adaptation / 33 个网文 Skills 与平台适配 |
| [claude-novel-skills](https://github.com/fnb666888/claude-novel-skills) | MIT | Decoupled writing method & style learning / 解耦写作法与风格学习 |
| [story-skills](https://github.com/ati9527/story-skills) | — | Web novel AI agent toolset / 网文 AI Agent 工具集 |
| [vibe-noveling](https://github.com/TulanCN/vibe-noveling) | MIT | Web novel creation workflow & SSoT revision / 网文创作工作流与 SSoT 修订 |

🇬🇧 This system is an independent creation and does not copy source code from the above projects.
🇨🇳 本系统为独立创作，未复制上述项目的源代码。
