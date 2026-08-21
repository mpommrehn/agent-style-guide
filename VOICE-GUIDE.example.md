# Voice guide (example)

Copy this, fill it in, and point the skill at it with `VOICE_GUIDE=path/to/it`.
Voice mode reads this file and lets it override any Google rule it conflicts
with. Delete every line you do not mean; a guide full of unedited placeholder
text is worse than none, because it will be followed.

## Who is writing

One paragraph. Role, background, and the stance the writing takes. What the
reader should feel about the author after two sentences.

## Signature moves (do these)

The specific, repeatable habits that make the writing recognizable. Be
concrete enough that someone could check whether a draft has them.

1. **Example: sincere exclamation points.** Used for genuine enthusiasm or
   thanks, never sarcasm. Their absence reads as machine-written restraint.
2. **Example: explicit confidence markers.** "I expect", "I'd guess",
   "I believe". Predictions are owned, never stated as anonymous fact.
3. **Example: parenthetical asides.** Frequent and helpful, sometimes long.
4. **Example: quoted coinages.** Invented or borrowed terms go in quotes.

## Anti-patterns (never do these)

The tells that make text read as machine-written in this particular voice.

- Uniform paragraph lengths and uniform bullet rhythm
- Every bullet shaped "**Bolded phrase:** explanation"
- Scaffolding words: "moreover", "furthermore", "it's important to note"
- Anonymous certainty: "It is widely known that..."
- Claims of value with no number, example, or named mechanism behind them
- Hedging boilerplate and throat-clearing openings

## Which Google rules are suspended, and why

List them explicitly. The skill suspends all five by default in voice mode;
say which ones actually matter here and what replaces them.

| Google says | This voice says |
|---|---|
| No exclamation points | Several per piece, always sincere |
| Second person only | First person, opinions owned |
| No parenthetical asides | Asides are a signature move |
| No figurative language | Coined terms in quotes are a fingerprint |

## Register by content type

Different documents need different settings of the same voice.

| Content type | How it sounds |
|---|---|
| Informal email | Warmest register; generous detail |
| Professional thank-you | Gratitude first, with specifics |
| Long-form persuasion | Story-driven, quantified, high energy |
| Analysis or opinion | Hypothesis-driven, hedged, mechanism-level |

## Samples

Point at a folder of material the person actually wrote, and keep it to
human-written work so it stays a clean baseline. Read the sample matching the
content type **before** drafting, not after. The guide describes the voice;
the samples are the voice.

    samples/

## Mechanical check

If you have a script that catches this voice's specific tells, name it here so
it runs alongside the Google check. A mechanical check is a floor, not a
ceiling: passing does not mean it sounds right.
