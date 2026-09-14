# -*- coding: utf-8 -*-
"""Every passage the letter quotes must exist in the manuscript.

A response letter quotes revised text so the reviewer can see the change without opening
the manuscript. Those quotes go stale silently: a later edit rewords the sentence, the
figure moves, a citation marker shifts, and the letter now quotes text the reviewer will
not find. Run this before sending, and after any round of manuscript edits.

    python verify_letter.py

Reports each quoted passage that does not resolve. Some misses are deliberate, such as
quoting a phrase the revision deleted in order to say it was removed. Record those in the
plan rather than silencing the check.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revision_config
from docx_util import doc_text, normalize
from letter_io import blocks, counts

OPEN, CLOSE, ELLIPSIS = chr(0x201c), chr(0x201d), chr(0x2026)
MIN = 25


def main():
    cfg = revision_config.load()
    haystack = normalize(' '.join(doc_text(p) for p in revision_config.docs(cfg)))
    letter = blocks(cfg['letter'])

    bad = 0
    pattern = re.compile(u'%s(.+?)%s' % (OPEN, CLOSE), re.S)
    for tag, body in sorted(letter.items()):
        for quote in pattern.findall(' '.join(body)):
            # a quote broken by an ellipsis is checked segment by segment
            segments = [s for s in quote.split(ELLIPSIS) if len(normalize(s)) > MIN]
            if all(normalize(s) in haystack for s in segments):
                continue
            bad += 1
            print('MISSING  [%s]\n         %s\n' % (tag, normalize(quote)[:160]))

    print('quoted passages checked; %d missing' % bad)
    placeholders, written = counts(cfg['letter'])
    print('placeholders: %d | written: %d' % (placeholders, written))
    return bad


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
