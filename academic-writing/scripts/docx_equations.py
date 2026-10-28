r"""Native Word equations (OMML) from LaTeX, for Markdown-to-DOCX manuscript builds with python-docx.

A displayed equation written as formatted text runs is overwritten on every rebuild, and editors must redo it by
hand. This module writes Word's own equation markup instead, so the equation opens in Word's equation editor and
survives rebuilds unchanged. Edit equations in the Markdown source, never in Word.

Usage in a build script:

    from docx_equations import add_equation
    p = doc.add_paragraph(style="Displayed equation")      # a style with a centre tab and a right tab
    p.add_run("\t")
    add_equation(p, r"R_{\mathrm{lat}}(a) = N(a)")
    p.add_run("\t(6)")                                     # the equation number, from \tag{6} in the Markdown

Supported LaTeX subset: subscripts and superscripts (including both on one base), \mathrm, \mathit, \text, Greek
letters, the operators in OMML_TEXT, \min and \max, braces \{ \}, spacing commands, \left \right \middle (dropped,
Word sizes the delimiters), and \begin{cases} ... \end{cases}. Extend GREEK or OMML_TEXT for other symbols.

Self-test: python docx_equations.py writes equations_demo.docx next to this file.
"""

import re

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε", "varepsilon": "ε", "theta": "θ",
         "kappa": "κ", "lambda": "λ", "mu": "μ", "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "phi": "φ",
         "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω", "Delta": "Δ", "Sigma": "Σ", "Omega": "Ω"}

OMML_TEXT = {"cdot": "·", "in": "∈", "subseteq": "⊆", "cup": "∪", "forall": "∀", "leftarrow": "←",
             "langle": "⟨", "rangle": "⟩", "dots": "…", "mid": "|", "qquad": "  ", "quad": " "}
OMML_SKIP = {"left", "right", "middle", "tag"}


def omml_nodes(tex, plain=False):
    """Parse a small LaTeX subset into nodes for a Word equation: ("r", text, plain), ("sub"|"sup", base, script),
    ("subsup", base, sub, sup), and ("cases", [(value, condition), ...])."""
    nodes, i, n = [], 0, len(tex)

    def group(j):
        depth = 0
        for k in range(j, n):
            depth += {"{": 1, "}": -1}.get(tex[k], 0)
            if depth == 0:
                return tex[j + 1:k], k + 1
        return tex[j + 1:], n

    def atom(j):
        """The next single argument of _ or ^: a {group}, a command, or one character."""
        if tex[j] == "{":
            g, j = group(j)
            return omml_nodes(g, plain), j
        m = re.match(r"\\([A-Za-z]+)", tex[j:])
        if m:
            return omml_nodes(m.group(0), plain), j + len(m.group(0))
        return omml_nodes(tex[j], plain), j + 1

    while i < n:
        c = tex[i]
        if c in "_^":
            script, i = atom(i + 1)
            base = [nodes.pop()] if nodes else []
            if c == "^" and base and base[0][0] == "sub":
                nodes.append(("subsup", base[0][1], base[0][2], script))
            else:
                nodes.append(("sub" if c == "_" else "sup", base, script))
            continue
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)", tex[i:])
            if not m:                                   # \{ \} \, \  and similar
                nxt = tex[i + 1] if i + 1 < n else ""
                nodes.append(("r", nxt if nxt in "{}|" else " ", True))
                i += 2
                continue
            cmd = m.group(1)
            i += len(m.group(0))
            if cmd in ("mathrm", "text", "mathit"):
                g, i = group(i)
                nodes += omml_nodes(g, plain=cmd != "mathit")
            elif cmd in ("min", "max"):
                nodes.append(("r", cmd, True))
            elif cmd == "tag":
                _, i = group(i)
            elif cmd == "begin":
                _, i = group(i)
                end = tex.find("\\end{cases}", i)
                rows = [r.split("&") for r in tex[i:end].split("\\\\")]
                nodes.append(("cases", [(omml_nodes(r[0].strip(), plain),
                                         omml_nodes(r[1].strip(), plain) if len(r) > 1 else []) for r in rows]))
                i = end + len("\\end{cases}")
            elif cmd in GREEK:
                nodes.append(("r", GREEK[cmd], plain))
            elif cmd in OMML_TEXT:
                nodes.append(("r", OMML_TEXT[cmd], True))
            elif cmd not in OMML_SKIP:
                nodes.append(("r", cmd, plain))
            continue
        if c in "{}":
            g, i = group(i)
            nodes += omml_nodes(g, plain)
            continue
        if c != " ":
            nodes.append(("r", c, plain or not c.isalpha()))
        i += 1
    return nodes


def omml(tag, *children, **attrs):
    el = OxmlElement(f"m:{tag}")
    for k, v in attrs.items():
        el.set(qn(f"m:{k}"), v)
    for ch in children:
        el.append(ch)
    return el


def omml_elements(nodes):
    out = []
    for node in nodes:
        kind = node[0]
        if kind == "r":
            r = omml("r")
            if node[2]:
                r.append(omml("rPr", omml("sty", val="p")))
            t = omml("t")
            t.text = node[1]
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            r.append(t)
            out.append(r)
        elif kind in ("sub", "sup"):
            out.append(omml(f"s{kind.capitalize()}", omml("e", *omml_elements(node[1])),
                            omml(kind, *omml_elements(node[2]))))
        elif kind == "subsup":
            out.append(omml("sSubSup", omml("e", *omml_elements(node[1])), omml("sub", *omml_elements(node[2])),
                            omml("sup", *omml_elements(node[3]))))
        elif kind == "cases":
            rows = [omml("e", *omml_elements(v), *omml_elements([("r", " if ", True)] if c else []),
                         *omml_elements(c)) for v, c in node[1]]
            out.append(omml("d", omml("dPr", omml("begChr", val="{"), omml("endChr", val="")),
                            omml("e", omml("eqArr", *rows))))
    return out


def add_equation(p, tex):
    """Append tex to paragraph p as a native Word equation, editable in Word's equation editor."""
    p._p.append(omml("oMath", *omml_elements(omml_nodes(tex))))




if __name__ == "__main__":
    from pathlib import Path

    import docx

    demo = [r"c_r(f) = I_r(\varphi_f, \lambda_f)",
            r"R_{\mathrm{in}}(a) = \begin{cases} \{c_{r_{\max}}(a)\} & a \in A_F \\ F(a) & a \in A_G \end{cases}",
            r"M_a^t = \left(S_a^t,\ H_a^t\right)"]
    d = docx.Document()
    for n, tex in enumerate(demo, 1):
        p = d.add_paragraph()
        add_equation(p, tex)
        p.add_run(f"\t({n})")
    out = Path(__file__).with_name("equations_demo.docx")
    d.save(out)
    print(f"wrote {out}")
