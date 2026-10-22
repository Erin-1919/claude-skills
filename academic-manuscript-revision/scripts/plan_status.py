# -*- coding: utf-8 -*-
"""Keep the revision plan current as each item lands.

The plan is the working record, not a document written once at the start. Update it the
moment an item is applied, while the reasoning is still to hand: what was changed, what
was decided and why, and anything found along the way that the plan did not predict. A
plan updated at the end is a plan rewritten from memory.

    python plan_status.py --status                  show every item and its state
    python plan_status.py --done C7 --record "..."  mark applied and file the record
    python plan_status.py --done C7 --record-file note.md --write

Without --write it prints what it would change. The item table row is marked, and the
record is appended to the records section, created if absent.
"""
import io
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revision_config

DONE = u'✅'
ROW = re.compile(r'^\|\s*\*\*(?P<id>[A-Za-z]+\d+)\*\*\s*(?P<mark>[^|]*?)\|')
RECORDS_HEAD = u'### Records for applied items'
RECORDS_INTRO = (u'The item table gives one line per item. The full record of what was '
                 u'changed, what was decided, and anything found along the way is kept '
                 u'here.')


def rows(text):
    out = []
    for i, line in enumerate(text.split('\n')):
        m = ROW.match(line)
        if m:
            out.append((i, m.group('id'), DONE in m.group('mark')))
    return out


def show(text):
    items = rows(text)
    if not items:
        print('no item rows found. Rows must look like:  | **C7** | ... |')
        return
    width = max(len(i) for _, i, _ in items) + 1
    for _, item, done in items:
        print('  %-*s %s' % (width, item, 'applied' if done else 'outstanding'))
    print('\n%d of %d applied' % (sum(1 for _, _, d in items if d), len(items)))


def mark(text, item):
    lines = text.split('\n')
    for i, ident, done in rows(text):
        if ident != item:
            continue
        if done:
            print('%s already marked applied' % item)
            return text
        line = lines[i]
        head = '| **%s**' % item
        lines[i] = line.replace(head, '%s %s' % (head, DONE), 1)
        print('%s marked applied' % item)
        return '\n'.join(lines)
    raise SystemExit('no row for %s. Rows must look like:  | **%s** | ... |' % (item, item))


def add_record(text, item, record):
    entry = u'**%s.** %s\n\n' % (item, record.strip())
    if RECORDS_HEAD not in text:
        text = text.rstrip('\n') + u'\n\n---\n\n%s\n\n%s\n\n' % (RECORDS_HEAD, RECORDS_INTRO)
        print('created the records section')
    head = text.index(RECORDS_HEAD)
    nxt = text.find('\n## ', head)
    end = len(text) if nxt == -1 else nxt
    print('record for %s: %d characters' % (item, len(record.strip())))
    return text[:end].rstrip('\n') + '\n\n' + entry + text[end:]


if __name__ == '__main__':
    cfg = revision_config.load()
    path = cfg['plan']
    text = io.open(path, encoding='utf-8').read()

    if '--status' in sys.argv or len(sys.argv) == 1:
        show(text)
        sys.exit(0)

    if '--done' not in sys.argv:
        raise SystemExit(__doc__)
    item = sys.argv[sys.argv.index('--done') + 1]
    record = None
    if '--record' in sys.argv:
        record = sys.argv[sys.argv.index('--record') + 1]
    elif '--record-file' in sys.argv:
        record = io.open(sys.argv[sys.argv.index('--record-file') + 1],
                         encoding='utf-8').read()

    new = mark(text, item)
    if record:
        new = add_record(new, item, record)
    else:
        print('no --record given; the table row is marked but nothing is recorded')

    if '--write' in sys.argv:
        shutil.copyfile(path, path + '.bak')
        io.open(path, 'w', encoding='utf-8').write(new)
        print('written (backup at %s.bak)' % os.path.basename(path))
    else:
        print('\ndry run - pass --write to apply')
