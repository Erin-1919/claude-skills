# -*- coding: utf-8 -*-
"""Locate and load revision.json.

Every script in this skill reads its paths from one config file so that nothing is
hard-coded to a project. Paths inside revision.json are relative to the directory holding
revision.json. Scripts search upward from the working directory, or take --config.
"""
import io
import json
import os
import sys

NAME = 'revision.json'

TEMPLATE = {
    'manuscript': 'paper/Manuscript_WORKING.docx',
    'supplementary': None,
    'baseline_manuscript': 'paper/Manuscript_SUBMITTED.docx',
    'baseline_supplementary': None,
    'letter': 'revision_plan/response_letter.docx',
    'answers': 'revision_plan/answers.py',
    'plan': 'revision_plan/REVISION_PLAN.md',
    'principles': 'revision_plan/REVISION_PRINCIPLES.md',
    'citation_style': 'numeric',
    'letter_style': {'font': 'Times New Roman', 'size_pt': 12, 'color': '3EAFC2'},
}

PATH_KEYS = ('manuscript', 'supplementary', 'baseline_manuscript',
             'baseline_supplementary', 'letter', 'answers', 'plan', 'principles')


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
    cfg.setdefault('letter_style', TEMPLATE['letter_style'])
    cfg.setdefault('citation_style', 'numeric')
    cfg['_root'] = root
    cfg['_config'] = cfg_path
    return cfg


def docs(cfg):
    """The manuscript and, when there is one, the supplementary file."""
    return [p for p in (cfg['manuscript'], cfg['supplementary']) if p]


def init(target_dir):
    path = os.path.join(os.path.abspath(target_dir), NAME)
    if os.path.exists(path):
        raise SystemExit('%s already exists' % path)
    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(TEMPLATE, indent=2, ensure_ascii=False) + '\n')
    print('wrote %s\nEdit the paths to match this project, then delete any key that '
          'does not apply (for example supplementary).' % path)


if __name__ == '__main__':
    if '--init' in sys.argv:
        args = [a for a in sys.argv[1:] if a != '--init']
        init(args[0] if args else os.getcwd())
    else:
        cfg = load()
        print('config: %s' % cfg['_config'])
        for key in PATH_KEYS:
            if cfg.get(key):
                mark = 'ok ' if os.path.exists(cfg[key]) else 'MISSING'
                print('  %-24s %s  %s' % (key, mark, cfg[key]))
        print('  %-24s     %s' % ('citation_style', cfg['citation_style']))
        print('  %-24s     %s' % ('letter_style', cfg['letter_style']))
