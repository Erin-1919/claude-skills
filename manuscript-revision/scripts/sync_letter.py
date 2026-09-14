# -*- coding: utf-8 -*-
"""Mirror hand edits made in Word back into answers.py.

The author edits responses in the letter, not in the data file. Without this the next
fill_responses run, or any later regeneration, would quietly restore the older wording.
Run it whenever the author says they edited the letter.

Matching is by text similarity, not by opening words, so an entry is still recognised
after its first sentence has been rewritten.

    python sync_letter.py           # report only
    python sync_letter.py --write
"""
import difflib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revision_config
from letter_io import blocks, load_answers, rewrite_answer

FLOOR = 0.45


def ratio(a, b):
    return difflib.SequenceMatcher(None, ' '.join(a), ' '.join(b)).ratio()


def main(write):
    cfg = revision_config.load()
    letter = blocks(cfg['letter'])
    answers = load_answers(cfg['answers'])

    used, changed, unmatched = set(), [], []
    for tag, body in letter.items():
        best, score = None, 0.0
        for key, stored in answers.items():
            if key in used:
                continue
            r = ratio(body, stored)
            if r > score:
                best, score = key, r
        if best is None or score < FLOOR:
            unmatched.append(tag)
            continue
        used.add(best)
        if [p.strip() for p in answers[best]] != [p.strip() for p in body]:
            changed.append((tag, best, body, score))

    for tag in unmatched:
        print('?        letter block %r matches no answers entry' % tag)
    for key in answers:
        if key not in used:
            print("?        answers entry %r matches no letter block" % key[:44])

    if not changed:
        print('letter and answers agree, %d written response(s)' % len(letter))
        return

    for tag, key, body, score in changed:
        print('%-8s edited (%.0f%% similar) -> key %r' % (tag, score * 100, key[:44]))
        for p in body:
            print('        %s' % p[:150])
    if not write:
        print('\nreport only, pass --write to apply')
        return
    for _, key, body, _ in changed:
        rewrite_answer(cfg['answers'], key, body)
    print('\nrewrote %d entry(ies) in %s' % (len(changed), os.path.basename(cfg['answers'])))


if __name__ == '__main__':
    main('--write' in sys.argv)
