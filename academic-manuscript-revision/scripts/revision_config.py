# -*- coding: utf-8 -*-
"""Locate and load revision.json.

Every script in this skill reads its paths from one config file so that nothing is
hard-coded to a project. Paths inside revision.json are relative to the directory holding
revision.json. Scripts search upward from the working directory, or take --config.

Documents. A round may carry any number of .docx targets: a manuscript, a supplementary
file, an anonymised copy of each, a cover file. List them under "documents", each with the
working copy that is edited and the submitted file it will be compared against:

    "documents": [
      {"name": "manuscript",    "working": "...", "baseline": "..."},
      {"name": "supplementary", "working": "...", "baseline": "..."}
    ]

The older flat keys (manuscript, supplementary, baseline_manuscript,
baseline_supplementary) are still read and become two documents, so an existing
revision.json keeps working.
"""
import io
import json
import os
import sys

NAME = 'revision.json'

TEMPLATE = {
    'documents': [
        {'name': 'manuscript',
         'working': 'paper/Manuscript_WORKING.docx',
         'baseline': 'paper/Manuscript_SUBMITTED.docx'},
        {'name': 'supplementary',
         'working': 'paper/Supplementary_WORKING.docx',
         'baseline': 'paper/Supplementary_SUBMITTED.docx'},
    ],
    'letter': 'revision_plan/response_letter.docx',
    'answers': 'revision_plan/answers.py',
    'plan': 'revision_plan/REVISION_PLAN.md',
    'principles': 'revision_plan/REVISION_PRINCIPLES.md',
    'citation_style': 'numeric',
    'letter_style': {'font': 'Times New Roman', 'size_pt': 12, 'color': '3EAFC2'},
}

PATH_KEYS = ('letter', 'answers', 'plan', 'principles')

LEGACY = (('manuscript', 'manuscript', 'baseline_manuscript'),
          ('supplementary', 'supplementary', 'baseline_supplementary'))


def find(start=None):
    d = os.path.abspath(start or os.getcwd())
    while True:
        candidate = os.path.join(d, NAME)
        if os.path.exists(candidate):
            return candidate
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit(
                'no %s found above %s. Create one with:\n'
                '  python <skill>/scripts/revision_config.py --init' % (NAME, os.getcwd()))
        d = parent


def _documents(cfg, root):
    """Normalise to a list of {name, working, baseline} with absolute paths."""
    items = []
    for entry in cfg.get('documents') or []:
        if not entry.get('working'):
            continue
        items.append({
            'name': entry.get('name') or os.path.basename(entry['working']),
            'working': os.path.join(root, entry['working']),
            'baseline': os.path.join(root, entry['baseline']) if entry.get('baseline') else None,
        })
    if items:
        return items
    for name, work_key, base_key in LEGACY:      # revision.json written before documents
        if cfg.get(work_key):
            items.append({
                'name': name,
                'working': os.path.join(root, cfg[work_key]),
                'baseline': (os.path.join(root, cfg[base_key])
                             if cfg.get(base_key) else None),
            })
    return items


def load(argv=None):
    argv = sys.argv if argv is None else argv
    path = None
    if '--config' in argv:
        path = argv[argv.index('--config') + 1]
    cfg_path = os.path.abspath(path or find())
    root = os.path.dirname(cfg_path)
    with io.open(cfg_path, encoding='utf-8') as fh:
        cfg = json.load(fh)
    for key in PATH_KEYS:
        value = cfg.get(key)
        cfg[key] = os.path.join(root, value) if value else None
    cfg['documents'] = _documents(cfg, root)
    cfg.setdefault('letter_style', TEMPLATE['letter_style'])
    cfg.setdefault('citation_style', 'numeric')
    cfg['_root'] = root
    cfg['_config'] = cfg_path
    return cfg


def docs(cfg):
    """Every working copy, in the order they are listed."""
    return [d['working'] for d in cfg['documents']]


def baselines(cfg):
    """Every submitted file that has one, for the end-of-round comparison."""
    return [d['baseline'] for d in cfg['documents'] if d['baseline']]


def numeric_citations(cfg):
    """True when references are numbered, which is what manage_references.py handles."""
    return str(cfg.get('citation_style', 'numeric')).lower().startswith('numer')


def init(target_dir):
    path = os.path.join(os.path.abspath(target_dir), NAME)
    if os.path.exists(path):
        raise SystemExit('%s already exists' % path)
    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(TEMPLATE, indent=2, ensure_ascii=False) + '\n')
    print('wrote %s\nList every .docx this round edits under "documents" — manuscript, '
          'supplementary, anonymised copies — and set citation_style to numeric or '
          'author-date.' % path)


if __name__ == '__main__':
    if '--init' in sys.argv:
        args = [a for a in sys.argv[1:] if a != '--init']
        init(args[0] if args else os.getcwd())
    else:
        cfg = load()
        print('config: %s' % cfg['_config'])
        if not cfg['documents']:
            print('  no documents listed — add a "documents" list')
        for d in cfg['documents']:
            for role in ('working', 'baseline'):
                if d[role]:
                    mark = 'ok ' if os.path.exists(d[role]) else 'MISSING'
                    print('  %-24s %s  %s' % ('%s (%s)' % (d['name'], role), mark, d[role]))
        for key in PATH_KEYS:
            if cfg.get(key):
                mark = 'ok ' if os.path.exists(cfg[key]) else 'MISSING'
                print('  %-24s %s  %s' % (key, mark, cfg[key]))
        print('  %-24s     %s' % ('citation_style', cfg['citation_style']))
        print('  %-24s     %s' % ('letter_style', cfg['letter_style']))
