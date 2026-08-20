# agent-style-guide

The Google developer documentation style guide, as a skill an AI coding agent
can apply to your docs — plus a checker that catches the mechanical half.

```
$ python3 scripts/gstyle-check.py README.md

=== README.md  [mode: doc] ===
  FAIL  L34: "e.g." — use "for example" or "that is" (translates better)
  FAIL  L7: heading "What and Why" is Title Case — use sentence case
  warn  L58: "just" — "just" is usually filler; keep only if it means "only"
  2 fail, 1 warn

This is a floor, not a ceiling. Read the document.
```

## The idea

Google's guide is excellent for what it targets: reference docs read by
developers under time pressure, often non-native English speakers, often
through machine translation. Its best rules improve almost any technical prose.

But a chunk of it is a documentation *house style*, not a general writing
standard, and applying it to a cover letter or a blog post sands the voice out
of the writing. So this skill classifies the document first and picks a mode:

| Document | Mode | Result |
|---|---|---|
| README, runbook, API doc, spec, PR description | **doc** | Full ruleset |
| Cover letter, blog post, marketing copy, email | **voice** | Clarity rules only; your voice guide overrides the rest |
| Scratch notes | neither | It says so and stops |

That routing is the point. A style checker that cannot tell the difference
between a runbook and a personal essay will damage one of them.

## Install

### As a Claude Code skill

```bash
git clone https://github.com/mpommrehn/agent-style-guide.git
mkdir -p ~/.claude/skills
ln -s "$PWD/agent-style-guide" ~/.claude/skills/google-style
```

Then invoke it with `/google-style path/to/file.md`, or ask for a style pass in
plain language.

**To make it opt-in only**, add `disable-model-invocation: true` to the
frontmatter in `SKILL.md`. With that set, only you can run it, and its
description stays out of the model's context entirely. Worth doing while you
decide whether you trust the classification step on your own writing.

### As a standalone checker

The checker has no dependencies beyond Python 3 and does not need the skill:

```bash
python3 scripts/gstyle-check.py doc.md another.md
python3 scripts/gstyle-check.py letter.md --mode voice
```

Exit code is 0 when nothing failed, 1 otherwise, so it drops into CI or a
pre-commit hook.

## Configure your voice

Voice mode needs to know what your voice is. Copy the example and fill it in:

```bash
cp VOICE-GUIDE.example.md my-voice.md
export VOICE_GUIDE="$PWD/my-voice.md"
```

The example is a skeleton with four sections: signature moves, anti-patterns,
which Google rules to suspend, and register by content type. Delete every line
you do not mean — a guide full of unedited placeholder text is worse than none,
because it will be followed.

If no voice guide is configured, the skill says so and stays in doc mode rather
than guessing at a voice.

## What the checker catches

Word-level rules, which is the smaller half of the job:

<!-- gstyle-ignore-start -->
- Words that minimize the reader's difficulty: simply, easy, obviously, just
- Latin and vagueness: e.g., i.e., etc., and/or, utilize, leverage
<!-- gstyle-ignore-end -->
- Non-inclusive terms, with the substitutions the guide names
- British spellings where American is required
- Title Case headings, including the two-word case
- Ambiguous dates, bare link text, directional references
- Sentences over 25 words, likely passive voice, future tense
- Missing serial commas

It strips fenced code, inline code spans, URLs, and quoted terms first, because
a shell command containing `master` is not a style violation. Wrap anything
else it misreads in `<!-- gstyle-ignore-start -->` and `<!-- gstyle-ignore-end -->`.

## What the checker cannot catch

This matters more than the word-level rules do.

Across the first documents this was used on, the word-level rules found very
little — the vocabulary was already fine. Every finding that mattered came from
a human or a model actually reading the document:

- A section organized as a changelog, three debugging attempts in chronological
  order, with what the tool does *today* buried at the bottom
- A cross-reference saying "see the section above" that pointed 108 lines the
  other way
- An ASCII architecture diagram carrying information no screen reader could
  reach, and available nowhere else in the document
- A heading rename that would have silently broken every link pointing at it
- A document that was 64% fenced block, so most of it had never been checked at
  all by any run

None of those are findable by regex. The skill's workflow puts "read the
document" and "check fenced blocks separately" between running the checker and
editing, for exactly this reason.

**The checker is a floor, not a ceiling.** It says so in its own output.

## Departures from Google

Stated rather than silently applied:

- **Some inclusive substitutions lose meaning.** "Hangs" and "doesn't respond"
  describe different failures, and a runbook needs the distinction. Prefer the
  substitution where it is accurate; keep the precise term where changing it
  would mislead someone on call.
- **The word list carries Google product branding.** Skipped entirely. That is
  house naming, not style.
- **"Just" and "via" are warnings, not failures.** "Just" meaning "only" is
  often the precise word, and it is the most common false positive here.
- **Quoted material is never edited**, including a guide's own bad examples.
  The exclamation marks in `"Great question!"` are the point of the example.

## Tests

```bash
python3 tests/test_gstyle.py
```

27 tests. Six are regressions for bugs found by running the checker against
real documents rather than by testing it: a stray `---` horizontal rule that
silently swallowed half a file, `see below` never firing, `leverage` matching
inside `high-leverage`, `native` matching inside `React Native`, two-word Title
Case headings passing, and missing British-spelling rules.

That pattern is worth stating plainly: every bug in this checker was found by
using it, not by writing tests for it.

## License

Apache 2.0. See [LICENSE](LICENSE).
