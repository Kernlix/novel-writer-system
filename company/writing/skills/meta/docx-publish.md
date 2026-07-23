---
id: docx-publish
name: DOCX生成与投稿 Skill
category: 04-工具集成
description: 打包为DOCX并生成投稿材料
source: 灵境系统自动化工具流程
---

# 📄 DOCX生成与投稿准备 Skill

## 命令
`/novel:package`

## 功能
将完成的正文打包为DOCX文档，并生成投稿材料。

## 前置条件
- Node.js 已安装（`node --version`）
- docx 包已安装（`npm install -g docx`）

## 使用方法

### 1. 生成DOCX

使用 docx-js 生成 Word 文档。基本步骤：

**a）安装依赖**
```bash
cd 项目目录
npm install docx
```

**b）编写生成脚本**

参考以下模板创建 Node.js 脚本：

```javascript
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun,
  Header, Footer, AlignmentType, HeadingLevel, PageNumber, PageBreak
} = require("docx");

// 读取章节文件
const dir = "正文目录路径";
const chapterFiles = fs.readdirSync(dir)
  .filter(f => f.endsWith(".md"))
  .sort();

const chapters = chapterFiles.map(fn => {
  const text = fs.readFileSync(path.join(dir, fn), "utf-8");
  const lines = text.split("\n").filter(l => !l.startsWith("# ") && !l.startsWith("---") && l.trim());
  const title = text.match(/^# (.+)/m)?.[1] || fn.replace(".md","");
  return { title, lines, fn };
});

// 构建文档内容
const children = [];

// 封面页
children.push(new Paragraph({ spacing: { before: 4000 }, children: [] }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "作品标题", size: 48, bold: true, font: "微软雅黑" })]
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 400 },
  children: [new TextRun({ text: "作者：笔名", size: 24, font: "微软雅黑" })]
}));
children.push(new Paragraph({ children: [new PageBreak()] }));

// 各章节内容（简化示例）
chapters.forEach(ch => {
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: ch.title, font: "微软雅黑" })]
  }));
  ch.lines.forEach(line => {
    children.push(new Paragraph({
      spacing: { after: 60, line: 360 },
      children: [new TextRun({ text: line, size: 22, font: "宋体" })]
    }));
  });
  children.push(new Paragraph({ children: [new PageBreak()] }));
});

// 创建文档
const doc = new Document({
  styles: {
    default: { document: { run: { font: "宋体", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal",
        run: { size: 36, bold: true, font: "微软雅黑" },
        paragraph: { spacing: { before: 400, after: 300 }, outlineLevel: 0 } }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "作品标题", size: 18, color: "999999", font: "微软雅黑" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "— ", size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
            new TextRun({ text: " —", size: 18 })
          ]
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("输出路径/作品标题（投稿稿）.docx", buffer);
  console.log("✅ DOCX 已生成");
});
```

### 2. 生成投稿材料

```markdown
## 投稿材料模板

### 基本信息
- 标题：（作品名）
- 作者：笔名
- 篇幅：超短篇/中短篇（约 XX,XXX 字 / XX 章）
- 题材：悬疑惊悚 · 时间循环 · 心理反转
- 投稿平台：番茄小说「千字万金」第X期

### 作品简介（50-200字）
> ...

### 作品亮点
1. ...
2. ...

### 投稿邮件
收件人：责编邮箱
主题：保底投稿 + 作者笔名 + 题材《作品标题》
附件：DOCX文件
正文：简介+亮点+章节数+总字数+联系方式
```

### 3. 番茄责编邮箱

| 责编 | 邮箱 |
|------|------|
| 大米 | 695684975@qq.com |
| 花花 | 106277767@qq.com |
| 七月 | 3449580381@qq.com |
| 九山 | 1479546675@qq.com |
| 小舟 | 846152539@qq.com |

**公共邮箱**：fanqiexiaoshuoduangushi@bytedance.com

> 📌 已有责编直接联系责编，勿重复投公共邮箱
> 📌 邮件标题格式：保底投稿 + 作者笔名 + 历史成绩


## 关联Skill
- **`webnovel-submit`**
- **`short-story-quick`**
- **`chapter-writing`**
