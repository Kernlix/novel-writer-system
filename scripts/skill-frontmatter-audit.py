#!/usr/bin/env python3
"""
灵境系统 Skill Frontmatter Audit & Patch Tool
==============================================
扫描 company/writing/skills/ 下所有 Skill 文件，
输出字段覆盖统计报告，并智能推断补充缺失的 triggers、sessionKinds、contextNeeds 字段。

用法:
  # 仅审计
  python scripts/skill-frontmatter-audit.py --audit

  # 审计 + 补全缺失字段
  python scripts/skill-frontmatter-audit.py --patch

  # 指定目录
  python scripts/skill-frontmatter-audit.py --audit --skills-dir /path/to/skills
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 1. YAML Frontmatter Parser (lightweight, no dependency)
# ============================================================

def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str, int]:
    """
    Parse YAML frontmatter from markdown content.
    Returns (frontmatter_dict, body_text, end_of_frontmatter_line).
    """
    lines = content.split('\n')
    title = ''
    first_para = ''
    if not lines or lines[0].strip() != '---':
        # Try to extract info from markdown header for files without frontmatter
        for line in lines:
            if line.startswith('# ') and not title:
                title = line[2:].strip()
            elif line.strip() and not title:
                continue
            elif line.strip() and title and not first_para:
                first_para = line.strip()
                break
        return None, content, 0, title, first_para

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break

    if end_idx == -1:
        return None, content, 0, '', ''

    yaml_lines = lines[1:end_idx]
    body = '\n'.join(lines[end_idx + 1:])

    # Simple YAML parser (handles the subset used in this project)
    frontmatter = {}
    current_key = None
    current_list = None
    in_list = False
    in_dict = False
    current_dict_key = None
    current_dict = None
    dict_list = []

    for line in yaml_lines:
        # Check for top-level key: value
        m = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if m and not line.startswith(' ') and not line.startswith('\t'):
            if current_key and in_list and current_list:
                frontmatter[current_key] = current_list
            elif current_key and in_dict and current_dict and dict_list:
                # Finish previous dict item
                pass
            current_key = m.group(1)
            value = m.group(2).strip()
            in_list = False
            in_dict = False

            if value == '':
                # Could be a list or dict next
                frontmatter[current_key] = None
            elif value.startswith('[') and value.endswith(']'):
                # Inline list: [a, b, c]
                items = [item.strip().strip("'").strip('"') for item in value[1:-1].split(',') if item.strip()]
                frontmatter[current_key] = items
            elif value.startswith('{') and value.endswith('}'):
                # Inline dict: {k: v, k2: v2} - simplified
                try:
                    frontmatter[current_key] = json.loads(value.replace("'", '"'))
                except:
                    frontmatter[current_key] = value
            else:
                # Scalar value
                value = value.strip("'\"").strip()
                frontmatter[current_key] = value
            continue

        # List item: - value or - key: value
        list_m = re.match(r'^\s*-\s+(.*)', line)
        if list_m and current_key:
            list_item = list_m.group(1).strip()
            if list_item.startswith('{') and list_item.endswith('}'):
                # Dict in list: {id: '...', purpose: '...', sources: [...]}
                try:
                    # Fix single quotes to double quotes for JSON
                    json_str = list_item.replace("'", '"')
                    # Fix trailing comma before }
                    json_str = re.sub(r',\s*}', '}', json_str)
                    # Fix unquoted keys
                    json_str = re.sub(r'(\s+)(\w[\w-]*)(\s*):', r'\1"\2"\3:', json_str)
                    d = json.loads(json_str)
                    if current_key not in frontmatter or not isinstance(frontmatter[current_key], list):
                        frontmatter[current_key] = []
                    frontmatter[current_key].append(d)
                except json.JSONDecodeError:
                    # Manual parse
                    d = parse_inline_dict(list_item)
                    if current_key not in frontmatter or not isinstance(frontmatter[current_key], list):
                        frontmatter[current_key] = []
                    frontmatter[current_key].append(d)
            else:
                # Simple list item
                if current_key not in frontmatter or not isinstance(frontmatter[current_key], list):
                    frontmatter[current_key] = []
                list_item = list_item.strip("'\"").strip()
                frontmatter[current_key].append(list_item)
            continue

        # Indented key: value (for dict items in a list)
        indent_m = re.match(r'^\s{2,}(\w[\w-]*)\s*:\s*(.*)', line)
        if indent_m and current_key:
            # This might be part of a dict in a list, but for our frontmatter this is rare
            # We'll handle it as continuation
            pass

    # Flush last list
    if current_key and in_list and current_list:
        frontmatter[current_key] = current_list

    return frontmatter, body, end_idx, title, first_para


def parse_inline_dict(text: str) -> Dict:
    """Parse a dict string like {id: 'abc', purpose: '...', sources: [...]}"""
    result = {}
    # Extract key-value pairs
    pairs = re.findall(r"(\w[\w-]*)\s*:\s*'([^']*)'", text)
    for k, v in pairs:
        result[k] = v
    # Extract list values like sources: ['a', 'b']
    list_match = re.search(r'sources\s*:\s*\[([^\]]*)\]', text)
    if list_match:
        items = [item.strip().strip("'").strip('"') for item in list_match.group(1).split(',') if item.strip()]
        result['sources'] = items
    return result


def reconstruct_frontmatter(fm: Dict) -> str:
    """Reconstruct YAML frontmatter from dict."""
    lines = ['---']
    for key, value in fm.items():
        if isinstance(value, list):
            if value and isinstance(value[0], dict):
                # List of dicts (contextNeeds)
                lines.append(f'{key}:')
                for item in value:
                    item_str = ', '.join(f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}" for k, v in item.items())
                    lines.append(f'  - {{{item_str}}}')
            else:
                # Simple list
                items_str = ', '.join(f"'{v}'" for v in value)
                lines.append(f'{key}: [{items_str}]')
        elif isinstance(value, dict):
            # Inline dict (rare)
            lines.append(f'{key}: {json.dumps(value, ensure_ascii=False)}')
        else:
            lines.append(f'{key}: {value}')
    lines.append('---')
    return '\n'.join(lines)


# ============================================================
# 2. Field Inference Engine
# ============================================================

# Mapping from filename/skill topics to triggers
TRIGGER_MAP = {
    # Death game / 博弈 / 规则
    'death-game': ['死亡游戏', '规则', '博弈', '生存'],
    'game-theory': ['博弈', '策略', '游戏理论'],
    'meta-game': ['规则', '元游戏', '规则陷阱'],
    'rule': ['规则', '规则漏洞', '规则武器'],
    'game-scene': ['游戏场景', '博弈', '竞技'],
    'natural-disaster': ['灾难', '生存', '逃生'],
    'ensemble-game': ['群像', '多人博弈', '团队'],
    'space-limit': ['空间限制', '封闭空间', '密室'],
    'time-loop': ['时间循环', '轮回', '重置'],

    # 叙事 / 结构
    'narrative': ['叙事', '结构', '故事设计'],
    'narrative-pacing': ['叙事节奏', '节奏控制', '铺陈'],
    'narrative-rhythm': ['叙事节奏', '节奏控制'],
    'narrative-structure': ['叙事结构', '章节结构'],
    'foreshadow': ['伏笔', '铺垫', '预示'],
    'plot-rhythm': ['情节节奏', '叙事节奏'],
    'booming-plot': ['剧情爆发', '高潮', '转折'],
    'causal-retrospection': ['因果', '回溯', '倒叙'],
    'premise-negation': ['前提否定', '反转', '颠覆'],
    'story-within-story': ['套层叙事', '故事嵌套'],
    'chapter-writing': ['章节写作', '正文章节'],
    'scene-emotional': ['场景情绪', '情感映射'],
    'emotional-arc': ['情感弧线', '情绪曲线'],
    'emotional-anchor': ['情感锚点', '情感物件'],

    # 喜剧
    'comedy': ['喜剧', '搞笑', '幽默'],
    'comedic': ['喜剧', '搞笑', '幽默'],
    'comedy-scene': ['喜剧场景', '搞笑场面'],
    'comedy-pattern': ['喜剧模式', '笑点'],
    'defect-comedy': ['缺陷喜剧', '角色缺陷'],
    'system-comedy': ['系统喜剧', '系统流搞笑'],
    'theological': ['神学喜剧', '宗教喜剧'],

    # 对话
    'dialogue': ['对话', '对白', '台词'],
    'dialogue-as-warfare': ['对话博弈', '信息战', '对话攻防'],
    'dialogue-escalation': ['对话升级', '对话博弈'],
    'dialogue-info': ['信息植入', '对话埋线'],
    'pure-dialogue': ['纯对话', '对话场景'],
    'layered-deception': ['多层欺骗', '欺骗对话'],

    # 角色
    'character': ['角色', '人物', '角色塑造'],
    'character-weakness': ['角色弱点', '缺陷角色'],
    'reverse-character': ['反套路角色', '角色反转'],
    'white-sketch': ['白描角色', '简洁角色'],
    'protagonist-fantasy': ['主角幻想', '主角解构'],
    'masochistic-sacrificial': ['受虐角色', '牺牲角色'],

    # 反转
    'reversal': ['反转', '逆转', '反预期'],
    'false-hope': ['虚假希望', '希望反转'],
    'cognitive-reversal': ['认知反转', '认知颠覆'],
    'premise-negation': ['前提否定', '反转'],

    # 心理 / 认知
    'cognitive': ['认知', '心理', '思维'],
    'cognitive-horror': ['认知恐怖', '心理恐怖'],
    'cognitive-manipulation': ['认知操控', '心理操控'],
    'cognitive-mismatch': ['认知错位', '思维差异'],
    'psychology': ['心理', '心理学', '心理描写'],
    'psychological-game': ['心理博弈', '心理游戏'],
    'reincarnator-psychology': ['转生者心理', '重生心理'],

    # 悬疑 / 恐怖
    'suspense': ['悬疑', '悬念', '推理'],
    'identity-suspense': ['身份悬疑', '身份之谜'],
    'closed-space': ['封闭空间', '密室'],
    'cognitive-horror': ['认知恐怖', '心理恐怖'],
    'ritual-religious': ['仪式悬疑', '宗教悬疑'],
    'document-as-horror': ['文档恐怖', '档案恐怖'],

    # 战斗
    'combat': ['战斗', '打斗', '动作'],
    'pre-battle': ['战前叙事', '战斗铺垫'],
    'process-violence': ['过程暴力', '暴力描写'],
    'violent-rescue': ['暴力营救', '营救'],

    # 网文
    'webnovel': ['网文', '网络小说', '网络文学'],
    'webnovel-submit': ['投稿', '平台适配', '网文投稿'],
    'webnovel-suspense': ['网文悬念', '连载悬念'],
    'webnovel-trend': ['网文趋势', '热门题材'],
    'webnovel-goldfinger': ['金手指', '网文金手指'],

    # 工具方法
    'snowflake': ['雪花法', '大纲', '小说结构'],
    'save-the-cat': ['救猫咪', '节拍表', '故事结构'],
    'short-story': ['短篇', '短篇小说'],
    'timeline': ['时间线', '时间轴'],
    'decoupled-writing': ['解耦写作', '模块化写作'],

    # 恋爱
    'romance': ['恋爱', '言情', '爱情'],
    'love-triangle': ['三角恋', '恋爱关系'],

    # 其他叙事概念
    'ability-counter': ['能力克制', '能力对抗'],
    'absent-mirror': ['缺席之镜', '缺失叙事'],
    'action-substitute': ['行动替代', '动作替代'],
    'afterlife': ['死后世界', '轮回', '三界'],
    'anthropomorphic': ['拟人化', '物拟人'],
    'belief-dependent': ['信念能力', '信念系统'],
    'benevolence-violence': ['仁爱与暴力', '正义暴力'],
    'black-humor': ['黑色幽默', '地狱笑话'],
    'concept-pre-deployment': ['概念预置', '概念铺垫'],
    'counter-intuitive': ['反直觉', '反常识'],
    'created-being': ['造物', '创生物'],
    'demon-contract': ['恶魔契约', '契约交易'],
    'dialect-subtext': ['方言潜台词', '方言'],
    'evil-evolution': ['恶之进化', '反派进化'],
    'existential-alliance': ['存在主义联盟', '存在同盟'],
    'first-person-shameless': ['第一人称无耻', '无耻叙事'],
    'frank-manipulation': ['坦率操控', '真诚操控'],
    'godhood-dwarfing': ['神性矮化', '神格解构'],
    'guardian-motivation': ['守护动机', '守护者'],
    'hard-reasoning': ['硬核推理', '逻辑推理'],
    'infiltrator-villain': ['卧底反派', '潜入反派'],
    'isekai-culture': ['异世界文化冲突', '异世界'],
    'machine-metaphor': ['机器隐喻', '机械隐喻'],
    'mask-impersonation': ['面具冒充', '身份冒充'],
    'master-apprentice': ['师徒传承', '师徒'],
    'memory-codon': ['记忆密码', '记忆编码'],
    'memory-erasure': ['记忆擦除', '失忆恢复'],
    'micro-expression': ['微表情', '微表情博弈'],
    'named-quote': ['名句揭晓', '名场面'],
    'narrative-authority': ['叙事权威', '叙事权'],
    'negation-paradox': ['否定悖论', '悖论叙事'],
    'numerical-anchor': ['数字锚点', '数字信息'],
    'performative-deduction': ['表演性推理', '表演推理'],
    'pseudo-family': ['伪家庭', '虚假家庭'],
    'rational-killing': ['理性杀意', '理性杀戮'],
    'reincarnation-growth': ['转生成长', '重生'],
    'sensory-inversion': ['感官倒置', '感官反转'],
    'sensory-subtraction': ['感官剥离', '感官缺失'],
    'shadow-narrative': ['影子叙事', '暗线叙事'],
    'silent-knower': ['沉默知情者', '沉默者'],
    'supernatural-awakening': ['超自然觉醒', '觉醒'],
    'theory-revelation': ['理论揭露', '理论揭示'],
    'threat-narrative': ['威胁叙事', '威胁'],
    'truth-layer': ['真理层次', '真相层次'],
    'ultimate-underdog': ['终极逆袭', '逆袭', '弱者逆袭'],
    'unsentimental-finale': ['无情结局', '残酷结局'],
    'weakness-to-strength': ['弱点转优势', '弱点转化'],
    'dual-layer-gameplay': ['双层博弈', '双层结构'],
    'dual-space-narrative': ['双空间叙事', '平行叙事'],
    'docx-publish': ['DOCX', '投稿', '文档生成'],
    'mask-impersonation': ['面具', '冒充', '身份替换'],
}


def infer_triggers(skill_id: str, description: str, skill_name: str) -> List[str]:
    """Infer trigger keywords from skill ID, name, and description."""
    triggers = set()

    # 1. Check direct mapping from skill_id
    if skill_id in TRIGGER_MAP:
        triggers.update(TRIGGER_MAP[skill_id])

    # 2. Check partial matches in TRIGGER_MAP
    for key, vals in TRIGGER_MAP.items():
        if key in skill_id or skill_id.startswith(key) or skill_id.endswith(key):
            triggers.update(vals)

    # 3. Extract from description keywords
    desc_keywords = {
        '死亡游戏': '死亡游戏', '无限流': '无限流', '规则怪谈': '规则怪谈',
        '博弈': '博弈', '心理': '心理', '反转': '反转', '喜剧': '喜剧',
        '悬疑': '悬疑', '推理': '推理', '恐怖': '恐怖', '战斗': '战斗',
        '对话': '对话', '角色': '角色', '叙事': '叙事', '情感': '情感',
        '网文': '网文', '投稿': '投稿', '大纲': '大纲', '冲突': '冲突',
        '笑点': '笑点', '搞笑': '搞笑', '幽默': '幽默',
        '认知': '认知', '操控': '操控', '信息战': '信息战',
    }
    for kw, tag in desc_keywords.items():
        if kw in description:
            triggers.add(tag)

    # 4. Extract from skill name
    name_keywords = {
        '死亡游戏': '死亡游戏', '规则': '规则', '博弈': '博弈',
        '反转': '反转', '喜剧': '喜剧', '对话': '对话',
        '角色': '角色', '微表情': '微表情', '希望': '希望',
        '叙事': '叙事', '双层': '双层', '双空间': '双空间',
        '战斗': '战斗', '悬疑': '悬疑', '网文': '网文',
        '投稿': '投稿', '情感': '情感',
    }
    for kw, tag in name_keywords.items():
        if kw in skill_name:
            triggers.add(tag)

    # Ensure minimum of 2-3 triggers
    if not triggers:
        # Fallback: use first meaningful words from description
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', description)
        seen = set()
        for w in words:
            if w not in seen and len(triggers) < 5:
                triggers.add(w)
                seen.add(w)

    # Convert to sorted list, limit to 6
    result = list(triggers)
    # Prioritize by placing description-derived keywords first
    result.sort()
    return result[:6]


def infer_session_kinds(skill_id: str, description: str, skill_name: str) -> List[str]:
    """Infer session kinds based on skill type."""
    session_kinds = ['writing']

    # Check if this is a review/analysis oriented skill
    review_indicators = ['review', '分析', '评价', '审阅', '审核', '评估', 'audit']
    for ind in review_indicators:
        if ind in skill_id.lower() or ind in description:
            if 'review' not in session_kinds:
                session_kinds.append('review')
            break

    # Check if this is a planning/design skill (not writing itself)
    planning_indicators = ['大纲', '设计', '方法论', '结构', 'snowflake', 'timeline', 'plot']
    for ind in planning_indicators:
        if ind in skill_id.lower() or ind in description:
            if 'planning' not in session_kinds:
                session_kinds.append('planning')
            break

    return session_kinds


def infer_context_needs(skill_id: str, description: str, skill_name: str,
                        skills_dir: str) -> List[Dict]:
    """Infer context needs based on skill type."""
    needs = []
    skills_path = Path(skills_dir)

    # Default context need based on skill itself
    needs.append({
        'id': f'{skill_id}-context',
        'purpose': f'参考{skill_name}的完整内容',
        'sources': [f'company/writing/skills/{skill_id}.md']
    })

    # Check for companion skills that this one likely references
    companion_patterns = {
        'death-game': ['rule-as-weapon', 'game-theory'],
        'dual-layer-gameplay': ['dual-space-narrative', 'five-steps-ahead'],
        'dual-space-narrative': ['dual-layer-gameplay'],
        'false-hope-reversal': ['cognitive-reversal'],
        'dialogue-as-warfare': ['micro-expression-warfare', 'layered-deception-dialogue'],
        'micro-expression-warfare': ['dialogue-as-warfare'],
        'five-steps-ahead': ['dual-layer-gameplay'],
        'rule-as-weapon': ['death-game-narrative'],
        'cognitive-reversal': ['false-hope-reversal'],
        'defect-comedy-engine': ['comedy-scene-design', 'comedy-pattern-library'],
        'comedy-scene-design': ['defect-comedy-engine', 'comedy-pattern-library'],
        'comedy-pattern-library': ['defect-comedy-engine', 'comedy-scene-design'],
        'character-weakness-narrative': ['weakness-to-strength', 'emotional-anchor-object'],
        'weakness-to-strength': ['character-weakness-narrative'],
        'emotional-anchor-object': ['character-weakness-narrative'],
    }

    if skill_id in companion_patterns:
        for comp in companion_patterns[skill_id]:
            comp_file = skills_path / f'{comp}.md'
            if comp_file.exists():
                needs.append({
                    'id': f'{comp}-reference',
                    'purpose': f'参考关联Skill：{comp}',
                    'sources': [f'company/writing/skills/{comp}.md']
                })

    return needs


# ============================================================
# 3. Audit Functions
# ============================================================

ALL_FIELDS = ['id', 'name', 'skill', 'agent', 'description', 'created',
              'source', 'category', 'command', 'triggers', 'sessionKinds', 'contextNeeds']
REQUIRED_FIELDS = ['triggers', 'sessionKinds', 'contextNeeds']

def audit_skills(skills_dir: str) -> Dict:
    """Scan all skill files and produce coverage report."""
    skills_path = Path(skills_dir)
    md_files = sorted(skills_path.glob('*.md'))

    results = []
    field_counts = {f: 0 for f in ALL_FIELDS}
    field_values = {f: [] for f in ALL_FIELDS}

    for mf in md_files:
        content = mf.read_text(encoding='utf-8')
        fm, body, _, title, first_para = parse_frontmatter(content)

        info = {
            'file': mf.name,
            'id': fm.get('id', mf.stem) if fm else mf.stem,
            'title': title,
            'first_para': first_para,
            'fields': {},
            'has_frontmatter': fm is not None,
        }

        if fm:
            for field in ALL_FIELDS:
                present = field in fm and fm[field] is not None
                info['fields'][field] = present
                if present:
                    field_counts[field] += 1
                    v = fm[field]
                    if isinstance(v, list):
                        field_values[field].append((mf.name, v))
                    elif isinstance(v, dict):
                        field_values[field].append((mf.name, v))
                    else:
                        field_values[field].append((mf.name, str(v)[:60]))
        else:
            for field in ALL_FIELDS:
                info['fields'][field] = False

        results.append(info)

    return {
        'total_files': len(md_files),
        'results': results,
        'field_counts': field_counts,
        'field_values': field_values,
    }


def print_audit_report(report: Dict):
    """Print formatted audit report."""
    total = report['total_files']
    fc = report['field_counts']

    print('=' * 72)
    print(f'  灵境系统 Skill Frontmatter 字段覆盖审计报告')
    print(f'  扫描文件数: {total}')
    print('=' * 72)
    print()
    print(f'{"字段名":<20} {"覆盖数":<10} {"覆盖率":<10} {"状态":<10}')
    print('-' * 50)
    for field in ALL_FIELDS:
        count = fc[field]
        pct = count / total * 100 if total > 0 else 0
        status = '✅' if count == total else ('⚠️' if count >= total * 0.5 else '❌')
        print(f'{field:<20} {count:<10} {pct:<8.1f}% {status:<10}')
    print('-' * 50)
    print()

    # Missing required fields
    print('--- 缺失关键字段的 Skill 文件 ---')
    print()
    for field in REQUIRED_FIELDS:
        missing = [r for r in report['results'] if not r['fields'].get(field)]
        if missing:
            print(f'  [{field}] 缺失数: {len(missing)}')
            for m in missing[:10]:
                print(f'    - {m["file"]}  (id: {m["id"]})')
            if len(missing) > 10:
                print(f'    ... 还有 {len(missing) - 10} 个')
            print()
        else:
            print(f'  [{field}] ✅ 全部覆盖')
            print()

    # Summary
    print('--- 汇总 ---')
    fully_covered = sum(1 for r in report['results']
                        if all(r['fields'].get(f) for f in REQUIRED_FIELDS))
    partial = sum(1 for r in report['results']
                  if any(r['fields'].get(f) for f in REQUIRED_FIELDS) and
                     not all(r['fields'].get(f) for f in REQUIRED_FIELDS))
    none_covered = sum(1 for r in report['results']
                       if not any(r['fields'].get(f) for f in REQUIRED_FIELDS))

    print(f'  完全覆盖: {fully_covered}')
    print(f'  部分覆盖: {partial}')
    print(f'  完全缺失: {none_covered}')


# ============================================================
# 4. Patch Functions
# ============================================================

def patch_skills(skills_dir: str, dry_run: bool = False) -> Dict:
    """Patch missing triggers, sessionKinds, contextNeeds fields."""
    skills_path = Path(skills_dir)
    md_files = sorted(skills_path.glob('*.md'))

    stats = {
        'total': len(md_files),
        'patched': 0,
        'skipped': 0,
        'errors': [],
        'details': [],
    }

    for mf in md_files:
        content = mf.read_text(encoding='utf-8')
        fm, body, end_line, title, first_para = parse_frontmatter(content)

        if fm is None:
            # Generate frontmatter for files that don't have one
            skill_id = mf.stem
            skill_name = title if title else skill_id
            description = first_para if first_para else f'{skill_name}的写作技法'

            # Build new frontmatter
            fm = {
                'id': skill_id,
                'name': skill_name,
                'skill': skill_id,
                'agent': 'writer',
                'description': description,
            }
            triggers = infer_triggers(skill_id, description, skill_name)
            session_kinds = infer_session_kinds(skill_id, description, skill_name)
            context_needs = infer_context_needs(skill_id, description, skill_name, skills_dir)
            fm['triggers'] = triggers
            fm['sessionKinds'] = session_kinds
            fm['contextNeeds'] = context_needs

            new_fm_str = reconstruct_frontmatter(fm)
            new_content = new_fm_str + '\n\n' + content.lstrip('\n')

            if dry_run:
                stats['details'].append({
                    'file': mf.name,
                    'id': skill_id,
                    'changes': {'(no frontmatter)': 'created frontmatter + triggers/sessionKinds/contextNeeds'},
                    'new_frontmatter': fm,
                })
                stats['patched'] += 1
            else:
                mf.write_text(new_content, encoding='utf-8')
                stats['details'].append({
                    'file': mf.name,
                    'id': skill_id,
                    'changes': {'(no frontmatter)': 'created frontmatter + triggers/sessionKinds/contextNeeds'},
                })
                stats['patched'] += 1
            continue

        skill_id = fm.get('id', mf.stem)
        description = fm.get('description', '')
        skill_name = fm.get('name', skill_id)

        has_triggers = 'triggers' in fm and fm['triggers'] is not None
        has_session_kinds = 'sessionKinds' in fm and fm['sessionKinds'] is not None
        has_context_needs = 'contextNeeds' in fm and fm['contextNeeds'] is not None

        changes = {}

        if not has_triggers:
            triggers = infer_triggers(skill_id, description, skill_name)
            changes['triggers'] = triggers

        if not has_session_kinds:
            session_kinds = infer_session_kinds(skill_id, description, skill_name)
            changes['sessionKinds'] = session_kinds

        if not has_context_needs:
            context_needs = infer_context_needs(skill_id, description, skill_name, skills_dir)
            changes['contextNeeds'] = context_needs

        if not changes:
            stats['skipped'] += 1
            continue

        # Apply changes to frontmatter dict
        for key, value in changes.items():
            fm[key] = value

        # Reconstruct file
        new_fm_str = reconstruct_frontmatter(fm)
        new_content = new_fm_str + '\n' + body.lstrip('\n')

        if dry_run:
            stats['details'].append({
                'file': mf.name,
                'id': skill_id,
                'changes': changes,
            })
            stats['patched'] += 1
        else:
            # Write back
            mf.write_text(new_content, encoding='utf-8')
            stats['details'].append({
                'file': mf.name,
                'id': skill_id,
                'changes': changes,
            })
            stats['patched'] += 1

    return stats


def print_patch_report(stats: Dict):
    """Print patch execution report."""
    print('=' * 72)
    print(f'  Skill Frontmatter 补全报告')
    print('=' * 72)
    print()
    print(f'  总文件数:    {stats["total"]}')
    print(f'  已补全:      {stats["patched"]}')
    print(f'  无需修改:    {stats["skipped"]}')
    print(f'  错误:        {len(stats["errors"])}')
    print()

    if stats['errors']:
        print('--- 错误 ---')
        for e in stats['errors']:
            print(f'  ⚠️  {e}')
        print()

    print('--- 修改详情 (前20项) ---')
    print()
    for detail in stats['details'][:20]:
        print(f'  📄 {detail["file"]}')
        for key, value in detail['changes'].items():
            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    print(f'    + {key}: {json.dumps(value, ensure_ascii=False, indent=6)}')
                else:
                    print(f'    + {key}: {value}')
            else:
                print(f'    + {key}: {value}')
        print()
    if len(stats['details']) > 20:
        print(f'  ... 还有 {len(stats["details"]) - 20} 个文件')
        print()


# ============================================================
# 5. Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='灵境系统 Skill Frontmatter 审计与补全工具')
    parser.add_argument('--audit', action='store_true', help='执行字段覆盖审计')
    parser.add_argument('--patch', action='store_true', help='补全缺失字段')
    parser.add_argument('--dry-run', action='store_true', help='预览模式（不实际修改文件）')
    parser.add_argument('--skills-dir', type=str, default=None,
                        help='Skill 文件目录 (默认自动探测)')

    args = parser.parse_args()

    # Auto-detect skills directory
    if args.skills_dir:
        skills_dir = args.skills_dir
    else:
        # Try to find from script location or cwd
        script_dir = Path(__file__).resolve().parent
        candidates = [
            script_dir.parent / 'company' / 'writing' / 'skills',
            Path.cwd() / 'company' / 'writing' / 'skills',
        ]
        skills_dir = None
        for c in candidates:
            if c.exists():
                skills_dir = str(c)
                break
        if skills_dir is None:
            print('❌ 无法自动定位 skills 目录，请通过 --skills-dir 指定')
            sys.exit(1)

    print(f'📂 Skills 目录: {skills_dir}')
    print()

    # Default: run audit if nothing specified
    if not args.audit and not args.patch:
        args.audit = True

    if args.audit:
        print('🔍 正在审计字段覆盖...')
        report = audit_skills(skills_dir)
        print_audit_report(report)

    if args.patch:
        print()
        mode = '🔮 预览模式' if args.dry_run else '🛠  正在补全'
        print(f'{mode} (dry_run={args.dry_run})...')
        stats = patch_skills(skills_dir, dry_run=args.dry_run)
        print_patch_report(stats)

        if not args.dry_run and stats['patched'] > 0:
            print()
            print('✅ 补全完成！建议重新运行 --audit 验证覆盖效果。')


if __name__ == '__main__':
    main()
