---
id: epub-to-text
name: epub转文本技能
type: skill
department: learning
---

# epub转文本技能

> epub提取员的核心skill。将epub电子书转为基础文本，按章分块。

## 依赖安装

```bash
pip install ebooklib beautifulsoup4 lxml
```

## 提取脚本

```python
#!/usr/bin/env python3
"""epub → 按章分块的纯文本"""
import os, sys, re
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_epub(epub_path: str, out_dir: str):
    """提取epub到out_dir目录，按章分块"""
    os.makedirs(out_dir, exist_ok=True)
    book = epub.read_epub(epub_path)
    
    chapters = []
    for item in book.get_items():
        if item.get_type() != 9:  # ITEM_DOCUMENT
            continue
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        
        # 去插图标记
        for tag in soup.find_all(['img', 'figure', 'figcaption']):
            tag.decompose()
        
        text = soup.get_text()
        text = re.sub(r'\n{3,}', '\n\n', text)  # 合并多余空行
        text = text.strip()
        
        if len(text) < 100:
            continue  # 跳过版权页等短内容
        
        # 尝试从文本中提取章节标题
        title_match = re.search(r'第[一二三四五六七八九十百千万\d]+章\s*[^\n]*', text)
        title = title_match.group() if title_match else f"ch{len(chapters)+1:02d}"
        
        chapters.append((title, text))
    
    # 保存
    for i, (title, text) in enumerate(chapters, 1):
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
        fname = f"{i:02d}-{safe_title}.txt"
        with open(os.path.join(out_dir, fname), 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{text}")
    
    print(f"提取完成：{len(chapters)} 章 → {out_dir}")
    return chapters

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python epub_extract.py <epub路径> <输出目录>")
        sys.exit(1)
    extract_epub(sys.argv[1], sys.argv[2])
```

## 使用方式

```bash
python epub_extract.py "D:/allproject/训练学习库/素晴小说/01.epub" "D:/allproject/训练学习库/素晴小说/extracted/01/"
```
