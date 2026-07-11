# 🤖 Reasonix Usage Guide

> Using LingJing Novel Creation System within [Reasonix](https://reasonix.dev) (AI coding agent environment).

---

## 🎯 Method 1: Direct Skill Invocation

After installation, this system is registered as a skill in Reasonix. Use it directly in any conversation:

```
/novel-writer I want to write a sci-fi novel about interstellar colonization
```

Reasonix will automatically load LingJing and enter creative mode.

---

## 🎯 Method 2: Step-by-Step Usage

Once you're already in a Reasonix conversation, you can use LingJing's features incrementally:

### Start Creating
```
Please launch the LingJing novel creation system, I want to start writing a novel
```
Or:
```
/novel-writer /novel:start
```

### Build a World
```
/novel-writer Help me build a sci-fi world, /
novel:world
```

### Design Characters
```
/novel-writer Design three main characters, /novel:characters
```

### Write the Body
```
/novel-writer Write the opening of Chapter 1, /novel:write
```

### De-AI Polish
```
/novel-writer Help me polish this text, remove the AI feel, /novel:anti-ai
```

---

## 🎯 Method 3: Install in a Reasonix Project

If you want to permanently integrate it into your Reasonix project:

```bash
# Clone the repository into your Reasonix workspace
cd your-reasonix-project
git clone https://github.com/Kernlix/novel-writer-system.git skills/novel-writer

# Reference it in AGENTS.md
echo "- [novel-writer](skills/novel-writer/SKILL.md) — LingJing Novel Creation System" >> AGENTS.md
```

---

## 📋 Quick Command Reference

| Command | Function |
|---------|----------|
| `/novel-writer` | Directly invoke LingJing system |
| `/novel-writer /novel:start` | Launch creation wizard |
| `/novel-writer /novel:world` | Build world |
| `/novel-writer /novel:characters` | Design characters |
| `/novel-writer /novel:outline` | Plan outline |
| `/novel-writer /novel:write` | Write body text |
| `/novel-writer /novel:review` | Review chapters |
| `/novel-writer /novel:anti-ai` | De-AI polish |
| `/novel-writer /novel:booming` | Plot acceleration |
| `/novel-writer /novel:progress` | Check progress |
| `/novel-writer /novel:help` | Show help |

> 💡 **Simplified usage**: Just describe what you need — you don't need to strictly follow the command format.
> For example: "Help me design a cultivation world" will automatically trigger `/novel:world`.
