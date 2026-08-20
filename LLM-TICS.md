# LLM tics

Phrases that large language models reach for constantly and human writers
almost never do. They are not wrong English. They are *identifying* — a reader
who has seen enough model output recognizes them instantly, and the writing
stops sounding like a person.

This list is separate from any personal style guide on purpose. A voice guide
describes how one writer sounds; this describes how the model sounds when it is
not being anyone. The two are different problems, and only this one is
shareable.

**These rules apply in both doc mode and voice mode.** Google's house rules
(no exclamation points, second person only) are right for a runbook and wrong
for a personal essay. A tic is wrong in both.

## How to extend it

Add a line to the table below, then add the pattern to `LLM_TICS` in
`scripts/gstyle-check.py`. Keep the two in step: the table explains, the code
enforces, and neither is the source of truth alone.

The test for inclusion is not "is this bad writing." It is **would a person
writing naturally produce this phrase at this frequency.** Plenty of these
words are fine in isolation. What marks them is that a model reaches for them
in every third paragraph.

## The list

<!-- gstyle-ignore-start -->
| Tic | Why it reads as machine-written | Write instead |
|---|---|---|
| stated plainly, put plainly, worth stating plainly | Announces candour rather than being candid. A person who is being plain does not narrate that they are | Say the thing |
| load-bearing | Borrowed from structural engineering and applied to words, assumptions, and arguments. Vanishingly rare in human prose, ubiquitous in model output | "essential", "the argument depends on it", or name what breaks without it |
| the honest answer, the honest version, honest characterization | Implies the surrounding text was less honest. A tell disguised as candour | Just give the answer |
| it's worth noting, it's important to note, notably | Filler that defers the point by one clause | State the point |
| that said, having said that | Pivot filler. A person writes "but" | "but", "however", or start the new sentence |
| here's the thing | Faux-conversational throat-clearing | Delete it |
| to be clear, let's be clear | Announces clarity instead of being clear | Delete it and be clear |
| the real question is | Dismisses what came before to stage a reveal | Ask the question |
| does the heavy lifting | Metaphor a model reaches for whenever one component matters more | Name what it does |
| the short version, the TL;DR | Signals that the long version was padding | Lead with the short version and skip the label |
| at the end of the day | Empty summarizer | Delete it |
| delve, unpack, dive into, deep dive | Model vocabulary for "look at" | "examine", "look at", "read" |
| a testament to, speaks volumes, sheds light on | Review-copy register that shows up unprompted | Say what the evidence shows |
| in today's landscape, ever-evolving, rapidly changing | Filler openings that carry no information | Delete the clause |
| navigate the complexities, harness the power, unlock the potential | Marketing verbs applied to ordinary actions | "use", "handle", "solve" |
| game-changer, paradigm shift, revolutionary | Hype with nothing behind it | State the measurable difference |
| robust, seamless, comprehensive, holistic | Adjectives applied without evidence | Give the number or cut the word |
| genuinely, actually, truly, really (as intensifiers) | Hedge-intensifiers a model sprinkles for emphasis it has not earned | Delete. If the sentence needs them, it is not specific enough |
| crucially, importantly, significantly | Tells the reader what to care about instead of showing why | Delete, or make the point itself carry the weight |
| in practice | Fine occasionally; a tic when every claim gets one | Delete unless contrasting with theory |
| which is exactly why, which is precisely the point | Self-congratulatory closing on an argument | End the sentence |
<!-- gstyle-ignore-end -->

## Structural tics a regex cannot catch

These need a human or a careful read. They are worth knowing because they are
more identifying than any single word:

- **The contrastive reframe.** "This isn't a style problem, it's a structure
  problem." "It's not that it fails, it's that it fails silently." One is fine.
  Three in a document is a signature.
- **"Not just X, but Y."** The same move in a different coat.
- **The rule of three.** Three parallel clauses, three bullet points, three
  examples, every time. Human writing has lopsided lists.
- **Numbered throat-clearing.** "Two things are worth noting here:" followed by
  two things that did not need announcing.
- **The pre-summary.** A paragraph that says what the next paragraph will say.
- **Uniform paragraph length.** Every block four to six lines. Real writing has
  one-line paragraphs and long ones next to each other.
- **Ending every section on a lesson.** A tidy closing moral on each section
  rather than only where one was earned.
