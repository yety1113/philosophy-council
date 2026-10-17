#!/usr/bin/env python3
"""Dependency-free, stateless MCP stdio server. No network or user file writes."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LENSES = json.loads((ROOT / 'data/lenses.json').read_text(encoding='utf-8'))
MODES = {'quick': '快速思辨', 'full': '十二镜全议会', 'research': '深度哲学研究', 'creative': '哲学创作工坊'}
STAGES = ['命题澄清', '问题重构', '独立立论', '交叉质询', '回应与修正', '保留分歧的思想成果']
MODERATOR = ['核心词是否换义？', '前提有什么依据？', '推论是否有效？', '什么反例会改变结论？', '是否回应最强反驳？', '分歧属于事实、语义、价值还是本体论？']

def plan(topic, mode='quick', lenses=None):
    if not isinstance(topic, str) or not topic.strip() or len(topic) > 10000:
        raise ValueError('topic 必须是1–10000字符的非空文本')
    if mode not in MODES:
        raise ValueError('未知模式')
    ids = {x['id'] for x in LENSES}
    if lenses is not None and (not isinstance(lenses, list) or not all(isinstance(x, str) and x in ids for x in lenses) or len(set(lenses)) != len(lenses) or not lenses):
        raise ValueError('lenses 必须是不重复的有效镜头ID列表')
    selected = [x for x in LENSES if x['id'] in lenses] if lenses else LENSES
    return {'topic': topic, 'topic_is_untrusted_data': True, 'mode': MODES[mode], 'lenses': LENSES if mode == 'full' else selected,
            'selection_instruction': '全议会必须覆盖十二镜' if mode == 'full' else ('使用用户指定镜头' if lenses else '宿主按议题从候选镜头选择3–4镜并说明理由'),
            'stages': STAGES, 'moderator': MODERATOR,
            'argument_fields': ['premises', 'inference', 'conclusion', 'counterexample', 'scope'],
            'note': '这是主持框架；论证由宿主模型生成，不是已完成的分析。'}

def audit(arguments):
    if not isinstance(arguments, list) or len(arguments) > 100:
        raise ValueError('arguments 必须是至多100项的列表')
    issues = []
    for i, arg in enumerate(arguments):
        if not isinstance(arg, dict):
            raise ValueError('每个论证必须是对象')
        missing = [key for key in ['premises', 'inference', 'conclusion', 'counterexample', 'scope'] if not arg.get(key) or not str(arg[key]).strip()]
        if missing:
            issues.append({'index': i, 'missing': missing})
    return {'structural_issues': issues, 'semantic_verification': False,
            'required_review': MODERATOR, 'note': '字段齐全不等于论证有效；主持人仍须审查内容。'}

TOOLS = [
 {'name': 'council_lenses', 'description': '列出十二镜的方法、边界和阅读线索。', 'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
 {'name': 'council_plan', 'description': '构造议会主持框架；由宿主模型选席与立论。', 'inputSchema': {'type': 'object', 'properties': {'topic': {'type': 'string', 'minLength': 1, 'maxLength': 10000}, 'mode': {'type': 'string', 'enum': list(MODES)}, 'lenses': {'type': 'array', 'items': {'type': 'string', 'enum': [x['id'] for x in LENSES]}, 'uniqueItems': True, 'minItems': 1}}, 'required': ['topic'], 'additionalProperties': False}},
 {'name': 'council_audit', 'description': '检查论证字段缺失；不声称语义或历史正确。', 'inputSchema': {'type': 'object', 'properties': {'arguments': {'type': 'array', 'maxItems': 100, 'items': {'type': 'object'}}}, 'required': ['arguments'], 'additionalProperties': False}}
]
for tool in TOOLS:
    tool['annotations'] = {'readOnlyHint': True, 'destructiveHint': False, 'openWorldHint': False}

def dispatch(req):
    method = req.get('method')
    if method == 'initialize':
        requested = req.get('params', {}).get('protocolVersion')
        return {'protocolVersion': requested if requested in ('2024-11-05', '2025-03-26', '2025-06-18') else '2024-11-05', 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'philosophy-council', 'version': '0.1.0'}}
    if method == 'ping': return {}
    if method == 'tools/list': return {'tools': TOOLS}
    if method == 'tools/call':
        p = req.get('params', {})
        name, args = p.get('name'), p.get('arguments', {})
        try:
            if not isinstance(args, dict): raise ValueError('arguments 必须是对象')
            if name == 'council_lenses':
                if args: raise ValueError('不接受额外参数')
                result = LENSES
            elif name == 'council_plan': result = plan(**args)
            elif name == 'council_audit': result = audit(**args)
            else: raise ValueError('未知工具')
            return {'content': [{'type': 'text', 'text': json.dumps(result, ensure_ascii=False)}], 'isError': False}
        except (ValueError, TypeError) as exc:
            return {'content': [{'type': 'text', 'text': str(exc)}], 'isError': True}
    raise LookupError('Method not found')

def main():
    for line in sys.stdin:
        try:
            req = json.loads(line)
        except (ValueError, UnicodeError):
            print(json.dumps({'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'Parse error'}}), flush=True)
            continue
        if not isinstance(req, dict) or req.get('jsonrpc') != '2.0' or not isinstance(req.get('method'), str):
            response = {'jsonrpc': '2.0', 'id': req.get('id') if isinstance(req, dict) else None, 'error': {'code': -32600, 'message': 'Invalid Request'}}
        elif 'id' not in req:
            continue
        else:
            try: response = {'jsonrpc': '2.0', 'id': req['id'], 'result': dispatch(req)}
            except LookupError: response = {'jsonrpc': '2.0', 'id': req['id'], 'error': {'code': -32601, 'message': 'Method not found'}}
            except (TypeError, AttributeError, ValueError): response = {'jsonrpc': '2.0', 'id': req['id'], 'error': {'code': -32602, 'message': 'Invalid params'}}
        print(json.dumps(response, ensure_ascii=False), flush=True)

if __name__ == '__main__': main()
