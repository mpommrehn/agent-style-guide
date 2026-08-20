---
name: google-style
description: Use when asked to apply, check, or rewrite something against the Google developer documentation style guide, or when /google-style is typed. Applies to READMEs, AGENTS.md, runbooks, API docs, procedures, project docs, specs, and PR descriptions. Never apply this to a cover letter, email, or personal post unless asked for it by name.
---

# Google developer documentation style

Edit a document to the Google developer documentation style guide
(developers.google.com/style). Optimizes for a reader who is skimming under
time pressure, may not be a native English speaker, and may be reading a
machine translation.

Target: `$ARGUMENTS`. If no file was named, ask which document, or apply the
rules to the reply being written in this turn.

## First: classify the document, then pick the mode

This guide is a technical-documentation house style. It is right for docs and
wrong for anything carrying a personal or brand voice. Applying it everywhere
produces exactly the bloodless register that makes writing sound machine-made.

| The document is | Mode | What applies |
|---|---|---|
| README, AGENTS.md, runbook, API doc, procedure, how-to, project doc, PR description, code comment, spec | **doc** | Everything below |
| Cover letter, personal essay, marketing copy, email, social post, positioning doc, resume | **voice** | Clarity rules only. The configured voice guide wins every conflict, no exceptions. |
| Meeting notes, journal, scratch file | neither | Say so and stop. Don't polish a scratch file. |

**In voice mode, these Google rules are suspended.** They are house rules for
reference documentation, and enforcing them on voiced writing is a failure,
not a compromise:

- No exclamation points.
- Second person only, never "we" or "I".
- No parenthetical asides.
- No coinages or figurative language.
- No "currently" or "as of this writing".

Which of these matter, and what replaces them, is the voice guide's job — not
this skill's.

## Configure your voice guide

Voice mode needs one file describing how the writing should sound. Copy
`VOICE-GUIDE.example.md`, fill it in, and point at it:

```
VOICE_GUIDE=path/to/your-voice-guide.md
```

**Before editing anything in voice mode, read that file.** If no voice guide is
configured, say so and stay in doc mode rather than guessing at a voice.

The strongest version of this pairs the guide with a folder of samples the
person actually wrote. A style guide describes a voice abstractly, and text can
satisfy every rule in it and still read as machine-written. Samples are the
thing itself.

## Workflow

1. **Classify** the document and state the mode out loud before editing.
2. **Run the checker** on the current file to get a baseline:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/gstyle-check.py <file> [--mode voice]`
3. **Read the document.** The checker finds words. It cannot tell whether the
   procedure works, whether the sections are in the right order, or whether a
   reader can find what they need. Those are the edits that matter most, and
   in practice they are where every worthwhile finding has come from.
4. **Check any fenced block that holds prose separately.** The checker strips
   code fences to avoid false positives, so a document that is mostly fenced
   is a document that mostly went unchecked. Extract and run it as its own
   file. This has repeatedly been where the real errors were.
5. **Edit**, applying the rules below. Show the diff and the reasoning before
   overwriting anything you did not write.
6. **Re-run the checker.** Every remaining failure needs a stated reason to
   keep, not silence.

## The rules that matter most

Ranked by how often they actually improve a document.

1. **Put the condition before the instruction.** "To save your changes, click
   Save", not "Click Save to save your changes." The reader who already knows
   they want to save stops reading at the comma; the reader who doesn't needs
   the condition first to know whether the sentence is for them.
2. **Second person, active voice, present tense.** "You configure the token",
   not "The token is configured by the user" or "The token will be
   configured." Name who does the thing.
3. **Sentence case for every heading and title.** "Set up the build pipeline",
   not "Set Up The Build Pipeline".
4. **Descriptive link text.** The link text must say where it goes. Never
   "click here", "this link", "read more", or a bare URL.
<!-- gstyle-ignore-start -->
5. **Cut the words that minimize the reader's difficulty**: simply, easy,
   easily, just, obviously, clearly, of course. If it were obvious they would
   not be reading this line.
6. **Spell out the Latin and the vagueness**: "for example" not e.g., "that
   is" not i.e., a real list not etc. or "and so on", "and" or "or" not
   and/or, "use" not utilize or leverage.
7. **Short sentences and simple words.** Under about 25 words. "Start" not
   "commence". At most two nouns stacked as modifiers.
8. **Serial commas.** "tokens, secrets, and keys".
9. **Unambiguous dates.** 2026-08-20 or 20 August 2026. Never 8/20/26.
10. **No directional references.** "See Configure the token", not "see above".
    Layout changes; section names don't, and a pointer that says "above" is
    wrong the moment anything moves.
11. **Define every abbreviation on first use**, then use it consistently. Use
    one word for one thing throughout, even where a synonym would read better.
12. **Formatting carries meaning**: code font for filenames, commands, class
    and method names, placeholders, and console output. Bold for UI elements
    the reader clicks. Italic for a term being introduced. Underline for links
    only.
13. **Numbered lists for sequences, bulleted lists for sets, description lists
    for term-definition pairs.** Don't number a set.
14. **Inclusive terms**: allowlist/blocklist, primary/replica, placeholder
    (not dummy), person-hours, "stops responding" (not hangs). Drop crazy,
    insane, sanity check, cripple, guys.
<!-- gstyle-ignore-end -->
15. **Don't pre-announce.** No "coming soon", "in a future release", "we plan
    to". Document what exists.

Fuller detail is in `reference.md` in this skill's directory. Load it when a
specific question comes up, not by default.

## Where this departs from Google

State these rather than silently following either side:

- **Some inclusive substitutions lose meaning.** "Hangs" and "doesn't respond"
  are different failures, and a runbook needs the distinction. Prefer the
  substitution where it is accurate; keep the precise term where changing it
  would mislead an on-call engineer, and say why.
- **The word list carries Google product branding.** Skip that section
  entirely. It is house naming, not style.
- **"Just" and "via" are warnings, not failures.** "Just" meaning "only" is
  often the precise word, and it is the most common false positive here.
- **Quoted material is never edited.** Error messages, UI labels, log output,
  and other people's words stay verbatim, including when they violate every
  rule above. A guide's own bad examples are the point of the example.

## Common mistakes

| Mistake | Fix |
|---|---|
| Running the checker and stopping there | It checks words, not structure. Read the document; fix the ordering and the gaps too. |
| Trusting a clean result on a fence-heavy file | The checker skipped the fences. Extract prose blocks and check them separately. |
| Applying doc mode to voiced writing | Classify first. In voice mode the voice guide wins. |
| Rewriting quoted material | Examples, error text, and quotations stay exactly as they are. |
| Editing imperatives in a file that governs behavior | Rewording an instruction the system depends on, to satisfy a style rule, is a bad trade. Leave it. |
| Chasing every warning to zero | Warnings need judgment. A stated reason to keep one is a valid outcome. |

## Real-world note

Across the first several documents this was run on, the checker's word-level
rules found little: the vocabulary was already fine. Every finding that
mattered came from step 3 or step 4 — a section organized as a changelog
instead of by what the reader needs first, a cross-reference pointing at a
section 108 lines the wrong way, an ASCII diagram carrying information no
screen reader could reach, and a heading rename that would have silently
broken every link to it.

Treat the checker as the floor it is.
