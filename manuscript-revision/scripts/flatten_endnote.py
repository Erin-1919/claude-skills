# -*- coding: utf-8 -*-
"""Turn EndNote (or Zotero/Mendeley) citation fields into plain text.

Why this runs before any editing. Reference managers store citations and the reference
list as Word fields. Ordinary prose editing then breaks fields, no reference can be added
without returning to the manager, and python-docx edits can land inside field code where
they are invisible. Flattening makes the visible text the only text.

Two modes:

  --working    flatten the working copies in place, once, before editing starts
  --baseline   write plain-citation COPIES of the submitted files, leaving them untouched

Run --baseline before using Word's Compare. The working copies are flattened, so comparing
them against unflattened originals reports every citation as a change.

    python flatten_endnote.py --working --write
    python flatten_endnote.py --baseline --write

Left alone: TOC, PAGEREF, SEQ and any other Word field that is not a citation ADDIN.
Idempotent: re-running on a flattened file changes nothing.
"""
import os
import shutil
import sys
import zipfile

import docx
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revision_config

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARTS = ['word/document.xml', 'word/footnotes.xml', 'word/endnotes.xml']
# instruction text that marks a citation field, by reference manager
ADDINS = ('ADDIN EN.', 'ADDIN ZOTERO', 'ADDIN CSL_CITATION', 'ADDIN Mendeley')


def flatten_part(xml_bytes):
    """Return (xml, fields_flattened, runs_removed).

    Field layout: begin -> instrText (the code) -> [separate] -> result runs -> end.
    The control runs and everything in the code portion go; the result runs, which are
    the visible "[42,43]" and the formatted reference list, stay exactly as they are.
    Nested data fields sit inside the outer field's code portion and go with it.
    """
    root = etree.fromstring(xml_bytes)

    runs, kinds, stack, next_id = [], {}, [], 0
    for r in root.iter(W + 'r'):
        fld = r.find(W + 'fldChar')
        instr = r.find(W + 'instrText')
        is_control = False

        if fld is not None:
            t = fld.get(W + 'fldCharType')
            if t == 'begin':
                stack.append([next_id, 'code'])
                kinds[next_id] = ''
                next_id += 1
            runs.append((r, tuple(f[0] for f in stack), True,
                         stack[-1][1] if stack else None))
            if t == 'separate' and stack:
                stack[-1][1] = 'result'
            elif t == 'end' and stack:
                stack.pop()
            continue

        if instr is not None and stack:
            kinds[stack[-1][0]] += (instr.text or '')
            is_control = True

        runs.append((r, tuple(f[0] for f in stack), is_control,
                     stack[-1][1] if stack else None))

    citation = {fid for fid, instr in kinds.items()
                if any(a in instr for a in ADDINS)}

    removed = 0
    for r, snapshot, is_control, state in runs:
        if not any(fid in citation for fid in snapshot):
            continue
        depth = next(i for i, fid in enumerate(snapshot) if fid in citation)
        if is_control or state == 'code' or len(snapshot[depth:]) > 1:
            parent = r.getparent()
            if parent is not None:
                parent.remove(r)
                removed += 1

    return (etree.tostring(root, xml_declaration=True, encoding='UTF-8',
                           standalone=True), len(citation), removed)


def process(path):
    zin = zipfile.ZipFile(path)
    items = zin.infolist()
    payload, stats = {}, {}
    for it in items:
        data = zin.read(it.filename)
        if it.filename in PARTS:
            data, nf, nr = flatten_part(data)
            stats[it.filename] = (nf, nr)
        payload[it.filename] = data
    zin.close()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in items:
            zout.writestr(it, payload[it.filename])
    return stats


def counts(path):
    raw = zipfile.ZipFile(path).read('word/document.xml').decode('utf8')
    return sum(raw.count(a) for a in ADDINS), raw.count('<w:fldChar')


def report(path, stats, before_text, before_tables):
    after = docx.Document(path)
    addin, fld = counts(path)
    for part, (nf, nr) in stats.items():
        print('      %-22s fields flattened: %-3d runs removed: %d' % (part, nf, nr))
    print('      residual citation ADDIN: %d | residual fldChar: %d (TOC/PAGEREF only)'
          % (addin, fld))
    print('      paragraphs %d -> %d | tables %d -> %d | visible text identical: %s'
          % (len(before_text), len(after.paragraphs), before_tables, len(after.tables),
             before_text == [p.text for p in after.paragraphs]))


def run(pairs, write, backup_suffix):
    for src, dst in pairs:
        if not os.path.exists(src):
            raise SystemExit('missing: %s' % src)
        addin, fld = counts(src)
        print('%s\n   citation fields: %d | fldChar: %d' % (os.path.basename(src),
                                                            addin, fld))
        if not write:
            print('   would write %s\n' % os.path.basename(dst))
            continue
        if src != dst:
            shutil.copyfile(src, dst)
        else:
            shutil.copyfile(src, src + backup_suffix)
        doc = docx.Document(dst)
        before_text = [p.text for p in doc.paragraphs]
        before_tables = len(doc.tables)
        stats = process(dst)
        print('   -> %s' % os.path.basename(dst))
        report(dst, stats, before_text, before_tables)
        print()


def baseline_name(path):
    stem, ext = os.path.splitext(path)
    return stem + '_plaincite' + ext


if __name__ == '__main__':
    cfg = revision_config.load()
    write = '--write' in sys.argv
    if '--baseline' in sys.argv:
        pairs = [(p, baseline_name(p)) for p in
                 (cfg['baseline_manuscript'], cfg['baseline_supplementary']) if p]
        run(pairs, write, '')
        if write:
            print('Compare each _plaincite baseline against its working copy in Word.')
    elif '--working' in sys.argv:
        pairs = [(p, p) for p in revision_config.docs(cfg)]
        run(pairs, write, '.preflatten.bak')
    else:
        raise SystemExit(__doc__)
