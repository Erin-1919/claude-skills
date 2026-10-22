# -*- coding: utf-8 -*-
"""Check and renumber numeric citations in first-appearance order.

Journals using numbered citations (MDPI, Elsevier numeric, IEEE) require the reference
list to run in order of first appearance. Adding or removing one citation can renumber
dozens, so never renumber by hand.

Numeric styles only. Under an author-date style, such as Taylor & Francis or APA, there
is no ordering to keep and nothing to renumber: the reference list is alphabetical and
in-text citations carry names, not positions. Set "citation_style": "author-date" in
revision.json and this script reports that it does not apply rather than scanning for
markers it will never find. Neither --check nor --renumber is part of the per-item checks
in that case.

    python manage_references.py --check
    python manage_references.py --renumber          # dry run, prints the mapping
    python manage_references.py --renumber --write

Markers understood: [3], [3,4], [3-5], [3–5], and any mix, such as [2,5-7].
The reference list is the run of paragraphs after a heading of "References" that begin
with "N." or "N<tab>".
"""
import os
import re
import shutil
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revision_config
from docx_util import all_runs, iter_document_order, ptext, splice

MARKER = re.compile(r'\[(\d+(?:\s*[,–-]\s*\d+)*)\]')
ENTRY = re.compile(r'^(\d+)[.\t]\s*')
DASH = u'–'


def expand(body):
    out = []
    for part in body.split(','):
        part = part.strip()
        m = re.match(r'^(\d+)\s*[–-]\s*(\d+)$', part)
        if m:
            out.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            out.append(int(part))
    return out


def compress(nums):
    nums = sorted(set(nums))
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            parts.append(u'%d%s%d' % (nums[i], DASH, nums[j]))
        else:
            parts.extend(str(n) for n in nums[i:j + 1])
        i = j + 1
    return u'[%s]' % ','.join(parts)


def read(path):
    """Ordering comes from body paragraphs, which carry document order. Table cells are
    read only for coverage, since a table can cite a reference the prose never does and
    numeric table data would otherwise be mistaken for reference entries."""
    doc = docx.Document(path)
    paras = list(doc.paragraphs)
    texts = [ptext(p) for p in paras]
    ordered = list(iter_document_order(doc))

    head = None
    for i, t in enumerate(texts):
        if t.strip().lower() in ('references', 'reference list'):
            head = i
    entries, order = {}, []
    if head is not None:
        for t in texts[head + 1:]:
            m = ENTRY.match(t.strip())
            if m:
                entries[int(m.group(1))] = t.strip()
                order.append(int(m.group(1)))

    # markers in true document order, stopping at the reference list
    stop_text = texts[head].strip() if head is not None else None
    first, seq = {}, []
    for i, p in enumerate(ordered):
        t = ptext(p)
        if stop_text and t.strip() == stop_text:
            break
        for m in MARKER.finditer(t):
            for n in expand(m.group(1)):
                seq.append(n)
                first.setdefault(n, i)
    return doc, paras, texts, head, entries, order, first, seq, set()


def check(path):
    _, _, _, head, entries, order, first, seq, in_tables = read(path)
    name = os.path.basename(path)
    print(name)
    if head is None:
        print('  no References heading found; skipping')
        return True
    print('  in-text markers: %d | distinct cited: %d | reference entries: %d'
          % (len(seq), len(set(first) | in_tables), len(entries)))
    ok = True
    appearance = sorted(first, key=lambda n: first[n])
    if appearance != sorted(appearance):
        ok = False
        bad = [n for k, n in enumerate(appearance) if k and n < appearance[k - 1]]
        print('  ordering: OUT OF ORDER at %s' % bad[:8])
    else:
        print('  ordering: OK - ascending order of first appearance')
    cited = set(first) | in_tables
    missing = sorted(cited - set(entries))
    unused = sorted(set(entries) - cited)
    if missing or unused:
        ok = False
        print('  coverage: cited but not listed %s | listed but not cited %s'
              % (missing, unused))
    else:
        print('  coverage: OK - every reference cited, every citation listed')
    if order != sorted(order):
        ok = False
        print('  list numbering is not ascending: %s' % order[:10])
    print('\n%s' % ('No issues found.' if ok else 'Issues found.'))
    return ok


def renumber(path, write):
    doc, paras, texts, head, entries, order, first, _, in_tables = read(path)
    if head is None:
        raise SystemExit('no References heading in %s' % path)
    appearance = sorted(first, key=lambda n: first[n])
    mapping = {old: i + 1 for i, old in enumerate(appearance)}
    unused = sorted(set(entries) - (set(first) | in_tables))
    if unused:
        raise SystemExit('listed but never cited, resolve first: %s' % unused)
    if all(k == v for k, v in mapping.items()):
        print('already in first-appearance order; nothing to do')
        return
    for old in sorted(mapping):
        if mapping[old] != old:
            print('  [%d] -> [%d]  %s' % (old, mapping[old], entries[old][:70]))

    if not write:
        print('\ndry run - pass --write to apply')
        return

    for i in range(head):
        p = paras[i]
        for raw in sorted({m.group(0) for m in MARKER.finditer(ptext(p))},
                          key=len, reverse=True):
            nums = [mapping[n] for n in expand(raw[1:-1])]
            while raw in ptext(p):
                splice(p, raw, compress(nums))

    body = {mapping[old]: ENTRY.sub('', entries[old]) for old in mapping}
    k = 0
    for p in paras[head + 1:]:
        if not ENTRY.match(ptext(p).strip()):
            continue
        k += 1
        runs = all_runs(p)
        runs[0].text = u'%d.\t%s' % (k, body[k])
        for r in runs[1:]:
            r._r.getparent().remove(r._r)

    shutil.copyfile(path, path + '.bak')
    doc.save(path)
    print('\nwritten (backup at %s.bak)' % os.path.basename(path))


if __name__ == '__main__':
    cfg = revision_config.load()
    if not revision_config.numeric_citations(cfg):
        print('citation_style is %s, so first-appearance ordering does not apply. '
              'Under an author-date style the reference list is alphabetical and in-text '
              'citations carry names, not positions. Skip this check.'
              % cfg['citation_style'])
        sys.exit(0)
    targets = revision_config.docs(cfg)
    if '--renumber' in sys.argv:
        renumber(targets[0], '--write' in sys.argv)
    else:
        ok = all([check(t) for t in targets])
        sys.exit(0 if ok else 1)
