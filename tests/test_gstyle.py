#!/usr/bin/env python3
"""Tests for gstyle-check.py.

    python3 tests/test_gstyle.py

Each case writes a temporary file, runs the checker over it, and asserts on
which rules fired. Several of these exist because the checker got them wrong
against a real document first; those are marked as regressions.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / "scripts" / "gstyle-check.py"

PASS, FAIL = 0, 0


def run(text, mode="doc"):
    """Return the checker's output for a markdown document."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(text)
        path = f.name
    out = subprocess.run([sys.executable, str(CHECKER), path, "--mode", mode],
                         capture_output=True, text=True)
    Path(path).unlink(missing_ok=True)
    return out.stdout


def check(name, text, *, fires=(), silent=(), mode="doc"):
    """fires: substrings that must appear. silent: substrings that must not."""
    global PASS, FAIL
    out = run(text, mode)
    problems = []
    for want in fires:
        if want.lower() not in out.lower():
            problems.append(f"expected a hit for {want!r}")
    for unwanted in silent:
        if unwanted.lower() in out.lower():
            problems.append(f"false positive on {unwanted!r}")
    if problems:
        FAIL += 1
        print(f"  FAIL  {name}")
        for p in problems:
            print(f"        {p}")
    else:
        PASS += 1
        print(f"  ok    {name}")


print("word-list rules")
check("flags 'simply'", "# t\n\nSimply run the command.\n", fires=["simply"])
check("flags 'utilize'", "# t\n\nUtilize the API.\n", fires=["utilize"])
check("flags e.g. and etc.", "# t\n\nTools, e.g. one, two, etc.\n", fires=["e.g.", "etc."])
check("flags non-inclusive terms", "# t\n\nAdd it to the whitelist on the master node.\n",
      fires=["whitelist", "master"])
check("flags an ambiguous date", "# t\n\nShipped on 8/20/26 as planned.\n", fires=["ambiguous date"])
check("flags bare link text", "# t\n\nFor more, [click here](https://example.com).\n",
      fires=["link text"])

print("\nAmerican spelling")
check("flags -ise, -our, -re, -ce", "# t\n\nIt recognises the behaviour at the centre under licence.\n",
      fires=["recognises", "behaviour", "centre", "licence"])
check("accepts American forms", "# t\n\nIt recognizes the behavior at the center under license.\n",
      silent=["british"])

print("\nheadings")
check("flags Title Case", "# t\n\n## Set Up The Build Pipeline\n", fires=["title case"])
check("accepts sentence case", "# t\n\n## Set up the build pipeline\n", silent=["title case"])
check("flags two-word Title Case (regression)", "# t\n\n## Security Notes\n", fires=["title case"])
check("leaves ALL-CAPS emphasis alone (regression)",
      "# t\n\n## Things that do NOT belong here\n", silent=["title case"])

print("\ncode and quoting")
check("ignores fenced blocks",
      "# t\n\n```sh\ngit checkout master\nsimply run this\n```\n",
      silent=["master", "simply"])
check("ignores inline code", "# t\n\nThe `master` branch is fine.\n", silent=["master"])
check("ignores quoted terms (regression)",
      '# t\n\nNever write "sanity check" in a document.\n', silent=["sanity"])
check("honours the ignore block",
      "# t\n\n<!-- gstyle-ignore-start -->\nAvoid: whitelist, dummy, crazy.\n<!-- gstyle-ignore-end -->\n",
      silent=["whitelist", "dummy"])

print("\nregressions found against real documents")
check("a horizontal rule does not swallow the file",
      "# Title\n\nintro\n\n---\n\n## Section\n\nUtilize the API here.\n",
      fires=["utilize"])
check("'see below' is flagged",
      "# t\n\nSee below for the full story.\n", fires=["below"])
check("'below-average' is not flagged",
      "# t\n\nIt has below-average latency.\n", silent=["directional"])
check("'high-leverage' is not 'leverage'",
      "# t\n\nThis is the highest-leverage change available.\n", silent=["name the actual mechanism"])
check("'React Native' is not 'native'",
      "# t\n\nBuilt with React Native and Expo.\n", silent=["ambiguous"])
check("bare 'native' still fires",
      "# t\n\nIt has native support for that.\n", fires=["ambiguous"])

print("\nmode behaviour")
VOICED = "# t\n\nWe shipped it. It's great!\n"
check("doc mode flags 'we' and exclamations", VOICED, fires=["second person", "exclamation"])
check("voice mode suspends both", VOICED, silent=["second person", "exclamation"], mode="voice")
check("voice mode still flags clarity rules",
      "# t\n\nSimply utilize the API, e.g. like this!\n",
      fires=["simply", "utilize", "e.g."], mode="voice")

print("\nreporting")
# The notice only fires above 500 bytes, so the fixture has to be genuinely
# large; a small file that is 90% fence is not the situation being warned about.
check("reports a fence-heavy file",
      "# t\n\n```\n" + ("a line of code that is not prose\n" * 40) + "```\n\nOne short sentence of prose.\n",
      fires=["was not checked"])
out = run("# t\n\nA perfectly ordinary sentence about the build.\n")
if "0 fail" in out:
    PASS += 1
    print("  ok    a clean document reports zero failures")
else:
    FAIL += 1
    print(f"  FAIL  a clean document reports zero failures\n        got: {out.strip()[:80]}")

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
