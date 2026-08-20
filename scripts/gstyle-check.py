#!/usr/bin/env python3
"""Mechanical style check against the Google developer documentation style guide.

    python3 gstyle-check.py <file> [<file> ...] [--mode doc|voice]

doc   (default) the full ruleset, for documentation: READMEs, AGENTS.md,
      runbooks, API docs, procedures, specs, PR descriptions, code comments.
voice only the rules that do not collide with a personal or brand voice, for
      cover letters, email, blog posts, marketing copy. In this mode your own
      voice guide wins every conflict; see VOICE-GUIDE.example.md.

Reads .md, .txt, .html and .docx. Prose only: fenced code blocks, inline code
spans, URLs and HTML tags are stripped before checking, because these rules
govern prose and checking code produces nothing but false positives.

Skip a passage the checker misreads by wrapping it in
<!-- gstyle-ignore-start --> and <!-- gstyle-ignore-end -->, or by putting
"gstyle-ignore" on the line. A quoted term is skipped automatically: a guide
that says do not write "sanity check" is not writing it.

Exit 0 = no hard failures. Exit 1 = at least one FAIL.

THIS IS A FLOOR, NOT A CEILING. Passing does not mean the document is good. It
cannot tell whether the procedure works, whether the sections are in the right
order, or whether a reader can find what they need. Read the document.
"""
import argparse
import html
import re
import sys
import zipfile
from pathlib import Path

# --- Rule tables --------------------------------------------------------
# (regex, message, severity). Severity "fail" is a hard rule from the guide's
# Highlights or word list; "warn" is a rule with legitimate exceptions, where a
# human has to look. Every pattern is matched case-insensitively against prose
# with code stripped out.

# Rules that apply to any prose, in either mode.
UNIVERSAL = [
    (r"\bsimply\b", 'cut "simply" (word list: minimizes the reader\'s difficulty)', "fail"),
    (r"\bit'?s easy\b|\beasy\b|\beasily\b", 'avoid "easy/easily" (word list: if it were easy they would not be reading)', "warn"),
    (r"\bobviously\b|\bclearly\b|\bof course\b", "assumes reader knowledge; cut it", "fail"),
    (r"\bjust\b", '"just" is usually filler; keep only if it means "only" and that matters', "warn"),
    (r"\bplease\b", '"please" in instructions (voice and tone: "Click View", not "Please click View")', "warn"),
    (r"\butilize[sd]?\b", 'use "use"', "fail"),
    (r"(?<![-\w])leverag(e|es|ed|ing)\b", 'use "use", or name the actual mechanism', "fail"),
    (r"\ballows you to\b|\ballows the user to\b", 'use "lets you"', "fail"),
    (r"\band/or\b", 'use "and" or "or"; pick one, or write "A, B, or both"', "fail"),
    (r"\be\.g\.|\bi\.e\.", 'use "for example" or "that is" (translates better)', "fail"),
    (r"\betc\.|\band so on\b|\band so forth\b", "list the actual items, or say what the set is", "fail"),
    (r"\baka\b", 'write "also known as"', "fail"),
    (r"\bvia\b", 'prefer "with", "through", or "by using"', "warn"),
    (r"\bin order to\b", 'use "to"', "warn"),
    (r"\bwhite ?list|\bblack ?list|\bgrey ?list|\bgray ?list", 'use "allowlist" / "blocklist"', "fail"),
    (r"\bmaster\b|\bslave\b", 'use "primary/replica", "controller/node", or a term specific to the thing', "fail"),
    (r"\bsanity[- ]check", 'use "check", "validation", or "confidence check"', "fail"),
    (r"\bdummy\b", 'use "placeholder"', "fail"),
    (r"\bcraz(y|ier)\b|\binsane\b|\bbonkers\b|\bnuts\b", 'use "complex", "unexpected", or "baffling"', "fail"),
    (r"\bcripple[sd]?\b", "name the actual impact", "fail"),
    (r"\bdumb(ed)? down\b", 'use "simplify" or "remove jargon"', "fail"),
    (r"\bguys\b", 'use "everyone", "folks", or "people"', "fail"),
    (r"\bman[- ]hours?\b|\bmankind\b|\bmanpower\b", 'use "person-hours", "humanity", "staffing"', "fail"),
    (r"\bblind to\b", 'use "ignores", "unaware of"', "warn"),
    (r"\bfirst[- ]class citizen\b", "name the actual property", "warn"),
    # Negative lookbehind for React/Windows/Cloud: "React Native" is a product
    # name, not the ambiguous adjective the word list is about.
    (r"(?<!React )(?<!Windows )(?<!Cloud )\bnative(ly)?\b",
     'ambiguous; use "built-in", "in the SDK", or name the platform', "warn"),
    (r"\bcurrently\b|\bat this time\b|\bat present\b|\bas of this writing\b", "docs are read later; state the version or cut it", "warn"),
    (r"\bplease note\b|\bnote that\b|\bit'?s important to note\b", "filler; state the thing", "fail"),
    (r"\babove\b(?!-)|\bbelow\b(?!-)", "directional reference breaks on mobile and in translation; link to the section by name", "warn"),
    (r"\bclick here\b|\bread more\b|\bthis link\b|\bsee here\b|\blearn more\b(?= *[<\[])", "link text must describe the destination", "fail"),
    (r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "ambiguous date; write 2026-08-17 or 17 August 2026", "fail"),
    (r"\bhits?\b(?= (the|a|an)? ?(button|link|enter|endpoint))", 'use "click", "press", or "calls"', "warn"),
    (r"\bhangs?\b", 'use "stops responding" (also distinguishes hung from slow)', "warn"),
    (r"\bwe recommend\b|\bwe suggest\b", "attribute it or state it directly", "warn"),
    (r"\b\w*(?:recognis|organis|analys|initialis|optimis|customis|serialis|"
     r"normalis|apologis|authoris|categoris|emphasis(?=e)|minimis|maximis|"
     r"summaris|synchronis|utilis|standardis)(?:e|es|ed|ing|ation)\b",
     "British spelling; the guide requires American (-ize)", "fail"),
    (r"\b(behaviour|colour|favour|honour|labour|neighbour|flavour|rumour)s?\b",
     "British spelling; the guide requires American (-or)", "fail"),
    (r"\b(centre|metre|litre|fibre|calibre)s?\b",
     "British spelling; the guide requires American (-er)", "fail"),
    # Nouns where British keeps -ce and American uses -se. Found in a README
    # that wrote "license" six times and "licence" once, in the sentence
    # explaining its own license terms.
    (r"\b(licence|defence|offence|pretence)s?\b",
     "British spelling; the guide requires American (license, defense)", "fail"),
    (r"\b(cancelled|cancelling|travelled|travelling|modelled|modelling|"
     r"labelled|labelling|signalling)\b",
     "British spelling; American English single-l (canceled, labeled)", "warn"),
    (r"\b(whilst|amongst|towards)\b",
     'British; use "while", "among", "toward"', "warn"),
    # "the same" standing in for a noun ("revert on the same", "kindly find the
    # same attached"). A British administrative-legalese relic that survives in
    # commercial English precisely because it lets the writer avoid deciding
    # what they are referring to. Google's rule: replace ambiguous pronouns
    # with the noun. Only flagged after a preposition and only when no noun
    # follows, so "the same file" and "the same as before" stay clean.
    # Gated on both sides: a preposition before (so "I would do the same."
    # stays clean) and either punctuation or a function word after (so "the
    # same file" and "the same as before" stay clean, while "on the same at
    # your convenience" does not).
    (r"\b(?:on|for|with|to|from|in|at|of|upon|regarding|concerning|about)\s+"
     r"the\s+same\b(?=\s*[.,;:!?)]|\s*$|\s+(?:at|in|on|for|to|from|by|"
     r"with|and|or|but|so|then|before|after|until|please|kindly)\b)",
     'ambiguous "the same"; name the noun it stands for', "warn"),
    (r"\bthe same attached\b", 'name what is attached', "warn"),
]

# --- LLM tics ------------------------------------------------------------
# Phrases models reach for constantly and people almost never do. These fire in
# BOTH modes: Google's house rules are wrong for a personal essay, but a tic is
# wrong everywhere. See LLM-TICS.md for the reasoning and how to extend this.
LLM_TICS = [
    (r"\b(stated|put|stating|state it) plainly\b|\bplainly (stated|put)\b",
     "announces candour instead of being candid; say the thing", "fail"),
    (r"\bload[- ]bearing\b", "structural-engineering metaphor; name what breaks without it", "fail"),
    (r"\bthe honest (answer|version|truth|characterization|characterisation|read)\b",
     "implies the rest was less honest; just give the answer", "fail"),
    (r"\bit'?s worth noting\b|\bworth noting that\b|\bit'?s important to note\b",
     "filler that defers the point by a clause", "fail"),
    (r"\bthat said\b|\bhaving said that\b", 'pivot filler; use "but"', "fail"),
    (r"\bhere'?s the thing\b", "faux-conversational throat-clearing; delete it", "fail"),
    (r"\b(to be clear|let'?s be clear)\b", "announces clarity instead of being clear", "fail"),
    (r"\bthe real question is\b", "stages a reveal; just ask the question", "fail"),
    (r"\bdoes the heavy lifting\b|\bheavy lifting\b", "model metaphor; name what it does", "fail"),
    (r"\bthe short version\b|\bTL;?DR\b", "signals the long version was padding", "fail"),
    (r"\bat the end of the day\b", "empty summarizer; delete it", "fail"),
    (r"\bdelve\b|\blet'?s unpack\b|\bdeep dive\b|\bdive into\b",
     'model vocabulary for "look at"', "fail"),
    (r"\ba testament to\b|\bspeaks volumes\b|\bsheds light on\b",
     "review-copy register; say what the evidence shows", "fail"),
    (r"\bin today'?s [a-z]+\b|\bever[- ]evolving\b|\brapidly changing landscape\b",
     "filler opening carrying no information", "fail"),
    (r"\bnavigat(e|es|ing) the complexit|\bharness(es|ing)? the power\b|"
     r"\bunlock(s|ing)? the (potential|power)\b",
     'marketing verb for an ordinary action; use "use" or "handle"', "fail"),
    (r"\bgame[- ]changer\b|\bparadigm shift\b|\brevolutioni[sz]e\b",
     "hype with nothing behind it; state the measurable difference", "fail"),
    (r"\bseamless(ly)?\b|\bholistic\b|\bsynerg(y|ies|istic)\b",
     "adjective applied without evidence", "fail"),
    (r"\bwhich is exactly why\b|\bwhich is precisely (the point|why)\b",
     "self-congratulatory close; end the sentence", "fail"),
    (r"\b(genuinely|truly) \w+", "hedge-intensifier; delete it or be more specific", "warn"),
    (r"\bcrucially\b|\bimportantly\b|\bsignificantly\b(?! (better|worse|faster|slower|more|less|higher|lower))",
     "tells the reader what to care about; let the point carry it", "warn"),
    (r"\bin practice\b", "a tic when every claim gets one; delete unless contrasting with theory", "warn"),
    (r"\brobust\b|\bcomprehensive\b", "adjective without evidence; give the number or cut it", "warn"),
]

# Rules that collide with a personal or brand voice. Doc mode only.
DOC_ONLY = [
    (r"\bthe user (can|should|must|will|needs)\b", 'address the reader as "you"', "fail"),
    (r"(?<![\w'])(we|our|us)(?![\w'])", 'second person: "you", not "we" (Highlights)', "warn"),
    (r"!", "exclamation marks (voice and tone: no overwrought enthusiasm)", "warn"),
]

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being|gets?|got)\s+(\w+ly\s+)?"
    r"(\w+(?:ed|en|wn|ne|de|nt))\b(?=\s+by\b|\s*[.,;]|\s+(?:in|to|from|with|at|on)\b)",
    re.I,
)

FUTURE = re.compile(r"\bwill\s+(?:be\s+)?\w+", re.I)


def read_text(path):
    p = Path(path)
    if p.suffix.lower() == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf8")
        xml = re.sub(r"</w:p>", "\n", xml)
        xml = re.sub(r"<[^>]+>", "", xml)
        return html.unescape(xml)
    return p.read_text(encoding="utf8")


def blank(m):
    """Replace a match with its own newlines, so reported line numbers stay true.

    Collapsing a 40-line code fence to a single newline shifts every line number
    after it, which makes the output actively misleading in exactly the files
    that most need checking.
    """
    return "\n" * m.group(0).count("\n")


def strip_code(text):
    """Remove everything these rules do not govern.

    The guide is about prose. A shell command containing `master` or a JSON key
    named `blacklist` is not a style violation, it is the name of the thing.
    Order matters: fences before inline spans, or a fence's contents get half
    stripped and half kept.
    """
    # Explicit opt-out, stripped first so a marked block's own fences and quotes
    # cannot be reinterpreted. A document that teaches these rules has to name
    # the words it bans, and an "avoid X, use Y" table cannot quote its way out.
    # Without a block escape the checker flags its own guidance, and then people
    # stop reading its output.
    text = re.sub(r"<!--\s*gstyle-ignore-start\s*-->.*?<!--\s*gstyle-ignore-end\s*-->",
                  blank, text, flags=re.S | re.I)
    # YAML frontmatter, but only when the file opens with it. Anchoring to \A
    # matters: markdown uses --- as a horizontal rule, and a floating anchor
    # silently swallows everything between the first two rules.
    text = re.sub(r"\A---\s*$.*?^---\s*$", blank, text, flags=re.S | re.M, count=1)
    text = re.sub(r"^```.*?^```", blank, text, flags=re.S | re.M)   # fenced blocks
    text = re.sub(r"^~~~.*?^~~~", blank, text, flags=re.S | re.M)
    text = re.sub(r"^(?: {4}|\t)\S.*$", "", text, flags=re.M)       # indented blocks
    text = re.sub(r"<(pre|code|script|style)\b.*?</\1>", blank, text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " ", text)                          # inline spans
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def flat(s):
    """Collapse whitespace so a match spanning a line wrap prints on one line."""
    return " ".join(s.split())


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


QUOTED = re.compile(r"[\"“][^\"”\n]{1,60}[\"”]")


def is_quoted(text, start, end):
    """True if the match sits inside a quoted string on its own line.

    A style guide that says don't write "sanity check" is not writing "sanity
    check". Same for a doc quoting an error message or a UI label. Without this
    every guidance document flags itself, which is how a checker gets ignored.
    """
    ls = text.rfind("\n", 0, start) + 1
    le = text.find("\n", end)
    line = text[ls:le if le != -1 else len(text)]
    if "gstyle-ignore" in line:
        return True
    return any(m.start() < start - ls and m.end() > end - ls
               for m in QUOTED.finditer(line))


def headings(text):
    return [(i + 1, m.group(2)) for i, line in enumerate(text.split("\n"))
            if (m := re.match(r"^(#{1,6})\s+(.*)$", line))]


SMALL_WORDS = {"a", "an", "the", "and", "or", "but", "for", "to", "of", "in",
               "on", "at", "by", "with", "from", "as", "is", "are", "be",
               "your", "you", "it", "its", "up", "down", "out", "into",
               "over", "if", "when", "how", "what", "why", "not", "no"}


def title_case_heading(h):
    """Flag Title Case headings. Google wants sentence case.

    Two signals, because product names make this genuinely ambiguous. A
    capitalized small word ("The", "Of", "Up") is decisive: nothing but Title
    Case capitalizes those mid-heading. Otherwise fall back to density, tuned so
    that a heading which is mostly proper nouns passes. "Set up Cloud Storage"
    and "AGENTS.md - the working root (notes)" pass; "Don't Write Like
    This" and "Set Up The Project" fail.
    """
    words = re.findall(r"[A-Za-z][\w'-]*", h)
    # Two-word headings ("Security Notes", "Known Limitations") are the most
    # common Title Case form in a README and used to sail through, because the
    # density test below needs three content words to mean anything. Flag them,
    # but only as a warning: "Google Cloud" and "Migration Assistant" look
    # identical to a regex and only a human can tell them apart.
    if len(words) == 2:
        second = words[1]
        return "warn" if second[0].isupper() and not second.isupper() else False
    if len(words) < 3:
        return False
    rest = words[1:]
    # w.isupper() exempts ALL-CAPS emphasis ("do NOT ship this"), which is
    # a deliberate typographic choice, not Title Case.
    if any(w.lower() in SMALL_WORDS and w[0].isupper() and not w.isupper()
           for w in rest):
        return True
    content = [w for w in rest if w.lower() not in SMALL_WORDS and not w.isupper()]
    if len(content) < 3:
        return False
    caps = sum(1 for w in content if w[0].isupper())
    return caps / len(content) >= 0.7


def sentences(text):
    prose = re.sub(r"^\s*[#>|].*$", "", text, flags=re.M)   # headings, quotes, tables
    prose = re.sub(r"^\s*[-*+]\s+", "", prose, flags=re.M)  # list markers
    for m in re.finditer(r"[^.!?\n]{10,}[.!?]", prose):
        yield m.group(0).strip()


def check(path, mode):
    raw = read_text(path)
    text = strip_code(raw)
    fails, warns = [], []

    # A doc that is mostly fenced blocks got mostly skipped. Say so, because a
    # "clean" result on a file the checker barely read is worse than no result.
    if len(raw) > 500 and len(text) < len(raw) * 0.6:
        warns.append(f"{100 - int(100 * len(text) / len(raw))}% of this file is "
                     f"code, quotes, or fenced blocks and was not checked. If a "
                     f"fenced block holds prose, check it as its own file.")

    rules = UNIVERSAL + LLM_TICS + (DOC_ONLY if mode == "doc" else [])
    for pattern, msg, severity in rules:
        seen = set()
        for m in re.finditer(pattern, text, re.I):
            ln = line_of(text, m.start())
            if ln in seen or is_quoted(text, m.start(), m.end()):
                continue
            seen.add(ln)
            entry = f'L{ln}: "{flat(m.group(0))}" — {msg}'
            (fails if severity == "fail" else warns).append(entry)
        if len(seen) > 3:
            pass  # every hit is reported; the caller decides what to fix

    # Sentence case headings.
    for ln, h in headings(text):
        verdict = title_case_heading(h)
        if verdict == "warn":
            warns.append(f'L{ln}: heading "{h}" may be Title Case — use sentence '
                         f'case unless both words are a proper noun')
        elif verdict:
            fails.append(f'L{ln}: heading "{h}" is Title Case — use sentence case')

    # Condition after instruction. "Click Save to keep your changes" reads fine
    # in English and badly in translation; the guide wants the condition first.
    for s in sentences(text):
        if re.match(r"^(To|If|When|After|Before|Unless)\b", s):
            continue
        if m := re.search(r"^[A-Z]\w+[^,.]{0,60}?\s+(if you|to \w+ the|when you)\b", s):
            warns.append(f'condition after instruction: "{s[:80]}" — put the '
                         f"condition first (Highlights)")

    # Long sentences. The guide asks for short sentences for translation.
    for s in sentences(text):
        n = len(s.split())
        if n > 35:
            fails.append(f'{n}-word sentence: "{s[:70]}…" — split it')
        elif n > 28:
            warns.append(f'{n}-word sentence: "{s[:70]}…"')

    # Passive voice and future tense. Heuristics, so warn only.
    passives = {line_of(text, m.start()): flat(m.group(0)) for m in PASSIVE.finditer(text)}
    for ln, hit in list(passives.items())[:8]:
        warns.append(f'L{ln}: possible passive voice "{hit}" — say who does it')
    if len(passives) > 8:
        warns.append(f"…and {len(passives) - 8} more possible passives")

    futures = {line_of(text, m.start()): flat(m.group(0)) for m in FUTURE.finditer(text)}
    for ln, hit in list(futures.items())[:5]:
        warns.append(f'L{ln}: future tense "{hit}" — use present tense')
    if len(futures) > 5:
        warns.append(f"…and {len(futures) - 5} more future-tense verbs")

    # Serial comma. Only the clean three-noun case, because "X, which is Y and
    # Z" is a clause, not a list, and flagging those trains people to skim past
    # the whole category.
    CLAUSE_START = {"which", "that", "who", "whom", "where", "when", "it",
                    "they", "he", "she", "this", "there", "and", "but", "so",
                    "if", "because", "while", "although"}
    for m in re.finditer(r"\b\w+, ((?:\w+ ){0,2}\w+) (?:and|or) \w+", text):
        if m.group(1).split()[0].lower() in CLAUSE_START:
            continue
        warns.append(f'L{line_of(text, m.start())}: check serial comma in '
                     f'"{flat(m.group(0))}" (Highlights: use serial commas)')

    return fails, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--mode", choices=["doc", "voice"], default="doc")
    args = ap.parse_args()

    worst = 0
    for path in args.files:
        fails, warns = check(path, args.mode)
        print(f"\n=== {path}  [mode: {args.mode}] ===")
        for f in fails:
            print(f"  FAIL  {f}")
        for w in warns:
            print(f"  warn  {w}")
        if not fails and not warns:
            print("  clean")
        print(f"  {len(fails)} fail, {len(warns)} warn")
        worst = max(worst, 1 if fails else 0)

    print("\nThis is a floor, not a ceiling. Read the document.")
    sys.exit(worst)


if __name__ == "__main__":
    main()
