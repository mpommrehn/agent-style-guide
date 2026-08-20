# Google style: fuller reference

Loaded on demand from `SKILL.md`. Source: developers.google.com/style. The compressed top-15 list in `SKILL.md` covers the
rules that fire most often; this file covers the rest and the detail behind
them.

## Voice and tone

Write as a knowledgeable friend who understands what the reader wants to do.
Conversational and friendly without being frivolous, pedantic, or pushy.

Avoid: jargon and buzzwords, "please" in instructions, figurative language and
metaphors, filler ("please note", "at this time"), exclamation marks, pop
culture references, internet slang, and anything that minimizes the reader's
difficulty ("simply", "it's easy", "quickly").

Google's own calibration examples:

| Too informal | Right | Too formal |
|---|---|---|
| "Dude! This API is totally awesome!" | "This API lets you collect data about user preferences." | "The API may enable acquisition of information pertaining to user preferences." |
| "Just garbage-collect, and you're golden." | "To clean up, call the `collectGarbage` method." | "Completion requires executing an automated memory management function." |

Two techniques the guide recommends: ask "what am I trying to say?" when a
sentence is muddled, and read the section aloud.

## Writing for a global audience

The single highest-leverage section, because most of it improves English prose
for native readers too.

- Use the simple word. "Start", not "commence". "Some" or "many", not "a
  number of".
- Shorter sentences. Long sentences compound translation errors.
- Avoid phrasal verbs where a single verb exists. Exceptions the guide
  explicitly allows: "set up", "log in", "sign in".
- At most two nouns as modifiers. "Cloud-native DevSecOps pipeline" is at the
  limit; adding "hybrid" is past it.
- Place "only" immediately before what it modifies. "Request only one token",
  not "Only request one token".
- Don't use one word for two meanings anywhere in the document.
- Replace ambiguous pronouns with the noun. "Make sure that the ad is
  targeted", not "make sure that it's targeted".
- The same rule catches "the same" used as a noun: "revert on the same",
  "please find the same attached". It is a British administrative-legalese
  construction that survives in commercial English because it lets the writer
  avoid deciding what they are referring to. Name the thing.
- Define abbreviations on first use.
- Use text, not images, to convey new information. Images don't get
  translated.
- Diverse example names. No colloquialisms, idioms, humor, or culturally
  specific references. No seasonal references ("in the summer" is a different
  half of the year in Sydney).

## Language and grammar

- **Second person.** "You" rather than "we" or "the user". "We" is acceptable
  only for the authoring organization making a recommendation, and even then
  prefer stating the recommendation directly.
- **Active voice.** Make clear who performs the action. Passive is acceptable
  when the actor is genuinely unknown or irrelevant, or when the object is the
  real subject of the sentence.
- **Present tense.** "The service returns a token", not "will return".
- **Standard American spelling and punctuation.**
- **Contractions are fine** and help the conversational tone.
- **"That" versus "which":** "that" for restrictive clauses with no comma,
  "which" for non-restrictive clauses with a comma.
- **Articles.** Don't drop "a", "an", "the" to save space. Missing articles
  are one of the top sources of translation ambiguity.

## Punctuation

- Serial (Oxford) comma, always.
- Em dashes: no surrounding spaces in Google's own style. If your own voice
  guide takes a different line on em dashes, your guide wins.
- Colons introduce lists and explanations. Capitalize after a colon only if
  what follows is a complete sentence.
- Quotation marks: American convention, closing punctuation inside. Place
  quotation marks outside link text.
- Avoid ampersands as conjunctions, except when naming an actual UI element
  that uses one.
- Avoid slashes as "or". Write the word.

## Formatting and organization

**Text formatting summary:**

| Element | Format |
|---|---|
| Filenames, paths, class names, method names, HTTP status codes, console output, inline code, user input, placeholders | code font (backticks) |
| UI elements the reader interacts with, run-in headings, the start of a notice | bold |
| A term being introduced or discussed, a word used as a word, book and film titles, math variables, version variables | italic |
| Titles of short works (articles, episodes) | quotation marks |
| Link text | underline, and nothing else is ever underlined |
| Placeholders in all-caps | `PROJECT_ID` |

- Sentence case for headings, titles, and navigation.
- Headings should be descriptive and parallel in structure within a section.
- Numbered lists for sequences. Bulleted lists for everything else.
  Description lists for pairs of related data.
- Keep list items parallel in grammatical structure.
- Introduce a list with a sentence ending in a colon.
- Tables need a header row and a caption or introduction.

## Linking

- Link text describes the destination. It should make sense read out of
  context, because screen reader users often navigate by link list.
- Never "click here", "here", "this link", "read more", or a bare URL as link
  text.
- Don't say "click the link" or "see the following link". Just link the words.
- Link to the section by name, never "above" or "below".

## Computer interfaces

- Code samples should be complete, runnable, and correct. Test them.
- Use placeholders in caps, and explain each one.
- Command-line syntax: show the command exactly as typed, don't include the
  prompt character in copyable text.
- UI element names in bold, matching the capitalization the UI uses.
- Describe what the reader does, not what they see: "Click Save", not "A Save
  button appears, which you click".
- Don't document the obvious parts of a UI.

## Accessibility

- Alt text on every meaningful image; empty alt on purely decorative ones.
- Don't convey information by color, position, or shape alone.
- Descriptive link text (repeated here because it is the most common
  accessibility failure in developer docs).
- Don't use directional language ("the button on the right") as the only
  identifier.
- High-resolution or vector images where practical.

## Inclusive language

Replacements the guide names, with the caveat from `SKILL.md` that a
substitution which loses technical meaning is worse than the original:

<!-- gstyle-ignore-start -->
| Avoid | Use |
|---|---|
| whitelist / blacklist / graylist | allowlist / blocklist / provisional list |
| master / slave | primary / replica, controller / node, or a term specific to the system |
| sanity check | check, validation, confidence check |
| dummy value, dummy variable | placeholder |
| crazy, insane, bonkers, nuts | complex, unexpected, baffling |
| cripples | slows down, degrades, name the impact |
| dumb down | simplify, remove jargon |
| blind to | ignores, unaware of |
| guys | everyone, folks, people |
| man-hours, mankind, manpower | person-hours, humanity, staffing |
| hit (a button) | click, press |
| hangs | stops responding |
| native (feature, speaker) | built-in, or name the platform; restructure |
| first-class citizen | name the actual property |
| grandfathered | legacy, exempt |
| the disabled, the elderly | people with disabilities, older adults |
| normal / healthy person | nondisabled person |
| brown bag | learning session |
<!-- gstyle-ignore-end -->

## Things not to document

- Don't pre-announce. No "coming soon", "in a future release", "we plan to".
- Don't document unreleased features, deprecation dates that aren't final, or
  internal-only behavior.
- Don't include "currently" or "as of this writing"; state a version instead.

## The escape hatch

The guide opens with Orwell: "Break any of these rules sooner than say
anything outright barbarous." Clarity outranks consistency, and consistency
outranks the rule. If following a rule makes the sentence worse, don't.

The guide's own precedence order: project-specific style first, then this
guide, then Merriam-Webster and the Chicago Manual of Style. With this skill
the order is: your own voice guide first, then this guide.
