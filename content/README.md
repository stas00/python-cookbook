# Stas' Python Cookbook

> How to read this: skim the Table of Contents, jump to what you need. Each chapter is self-contained. Snippets are written to be copy-paste friendly — imports are shown the first time they're needed in a block.

## Table of Contents

**[Part I: Language Core](#part-i-language-core)**
- [Strings and Text](#strings-and-text)
- [String Formatting](#string-formatting)
- [Numbers and Math](#numbers-and-math)
- [Regular Expressions](#regular-expressions)
- [Lists](#lists)
- [Tuples](#tuples)
- [Sets](#sets)
- [Dictionaries](#dictionaries)
- [Comprehensions, Iterators and itertools](#comprehensions-iterators-and-itertools)
- [Functions](#functions)
- [Classes and Objects](#classes-and-objects)
- [Dates and Times](#dates-and-times)

**[Part II: Runtime and Environment](#part-ii-runtime-and-environment)**
- [Modules and Imports](#modules-and-imports)
- [Files, Paths and I/O](#files-paths-and-io)
- [Environment Variables and Program Arguments](#environment-variables-and-program-arguments)
- [Subprocess and Shell Integration](#subprocess-and-shell-integration)
- [Serialization: JSON, CSV, Pickle, XML, gzip](#serialization-json-csv-pickle-xml-gzip)
- [Concurrency: Processes, Threads and the GIL](#concurrency-processes-threads-and-the-gil)
- [Networking](#networking)

**[Part III: Debugging, Profiling and Testing](#part-iii-debugging-profiling-and-testing)**
- [Printing, Logging and Output Control](#printing-logging-and-output-control)
- [Debugging](#debugging)
- [Introspection and Object Inspection](#introspection-and-object-inspection)
- [Profiling CPU and Memory](#profiling-cpu-and-memory)
- [Exceptions and Error Handling](#exceptions-and-error-handling)
- [Testing with pytest and unittest](#testing-with-pytest-and-unittest)

**[Part IV: Packaging and Tooling](#part-iv-packaging-and-tooling)**
- [Versions and Dependencies](#versions-and-dependencies)
- [Packaging and Requirements](#packaging-and-requirements)
- [Code Quality and Formatting](#code-quality-and-formatting)
- [Big Data and Scaling Pointers](#big-data-and-scaling-pointers)
- [Appendix: One-liners and Resources](#appendix-one-liners-and-resources)

---

## Part I: Language Core

### Strings and Text

Strings are immutable sequences of Unicode code points. Every "mutation" returns a *new* string, which is why chains of transformations are common and cheap to reason about.

#### Case conversion and checks

```python
s.lower()         # "abc"
s.upper()         # "ABC"
s.capitalize()    # "Abc"  - first char upper, rest lower (like Perl's ucfirst)
s.title()         # "Abc Def" - capitalize each word
s.swapcase()

s.isupper()       # bool
s.islower()
s.istitle()
```

Python exposes a whole family of `is*` predicates for classifying string content. They operate on the whole string and return `False` for the empty string (except where noted):

```python
"1".isdigit()        # True
"a".isdigit()        # False
"café".isalpha()     # True  - Unicode aware
"123".isnumeric()    # True  - roughly /^\d+$/, but also matches ² ½ etc.
"var_1".isidentifier()  # True - valid Python name?
"  ".isspace()       # True
"Hello".isprintable()
```

Full set: `isalnum`, `isalpha`, `isascii`, `isdecimal`, `isdigit`, `isidentifier`, `islower`, `isnumeric`, `isprintable`, `isspace`, `istitle`, `isupper`. Note the subtle differences: `isdecimal ⊂ isdigit ⊂ isnumeric`.

#### Containment, prefixes and suffixes

```python
if "the" in text: ...          # substring test, fastest way

text.startswith("The")
text.endswith(".csv")
text.lower().endswith(".csv")  # case-insensitive

# startswith/endswith accept a tuple of options
fname.endswith((".jpg", ".png", ".gif"))

# and an optional start/end window
text.startswith(needle, start, end)
```

#### Splitting and joining

```python
"a b  c".split()          # ['a', 'b', 'c']  - splits on runs of whitespace
"a-b-c".split("-")        # ['a', 'b', 'c']
"a-b-c".rsplit("-", 1)    # ['a-b', 'c']  - split only the last occurrence
"a\nb\nc".splitlines()    # ['a', 'b', 'c']  - newline-aware, handles \r\n

"-".join(["a", "b", "c"]) # 'a-b-c'   - join iterable of *strings*
```

`partition`/`rpartition` split *once* and always return a 3-tuple `(before, sep, after)`, which avoids index errors:

```python
"key=value=x".partition("=")   # ('key', '=', 'value=x')
"key=value=x".rpartition("=")  # ('key=value', '=', 'x')
```

For shell-like tokenization (respecting quotes), reach for `shlex` instead of `split`:

```python
import shlex
shlex.split('program --name="two words" -v')
# ['program', '--name=two words', '-v']
```

#### Stripping

`strip`/`lstrip`/`rstrip` remove *sets of characters* from the ends — not a prefix/suffix substring, which surprises people:

```python
"  hi  ".strip()              # 'hi'
"www.example.com".strip("cmowz.")   # 'example'  - strips ANY of those chars
```

Python 3.9+ adds proper prefix/suffix removal:

```python
"unittest".removeprefix("unit")   # 'test'
"config.py".removesuffix(".py")   # 'config'
```

#### Replacing

```python
s = s.replace("foo", "bar")       # all occurrences
s = s.replace("foo", "bar", 1)    # first occurrence only
```

For pattern-based replacement, see [Regular Expressions](#regular-expressions).

#### Encoding and decoding

Strings are text; bytes are bytes. Convert explicitly:

```python
b"a string".decode("utf-8")       # bytes -> str
"café".encode("utf-8")            # str -> bytes

# strip non-ASCII / broken UTF-8 (lossy)
s.encode("ascii", "ignore").decode("utf-8", "ignore")
"".join(c for c in s if ord(c) < 128)   # ASCII-only
```

Detecting or repairing encodings:

```python
import chardet                    # pip install chardet
chardet.detect(open("f.txt", "rb").read())
# {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

import ftfy                       # pip install ftfy - "fixes text for you"
ftfy.fix_text("âœ” No problems")  # '✔ No problems'
```

#### Comparing strings with a readable diff

When two strings should be equal but aren't, a character-level diff with context saves time:

```python
import difflib

def str_compare(a, b):
    """Print a contextual diff; return True if equal."""
    if len(a) != len(b):
        print(f"length mismatch: a={len(a)}, b={len(b)}")
    match = True
    for i, d in enumerate(difflib.ndiff(a, b)):
        if d[0] == " ":
            continue
        match = False
        ctx = (a if d[0] == "-" else b)[max(0, i - 10):i + 10]
        print(f'{"del" if d[0]=="-" else "add"} {d[-1]!r} at {i}, ctx=[{ctx}]')
    return match
```

#### Wrapping and templating

```python
import textwrap
print(textwrap.fill(long_text, width=100))
print(textwrap.dedent(indented_block))   # strip common leading whitespace

from string import Template
Template("Hey, $name!").substitute(name="Peter")   # 'Hey, Peter!'
```

`Template` is handy for user-supplied templates because it can't execute arbitrary code the way f-strings and `str.format` can.

---

### String Formatting

Modern Python has three formatting styles. Prefer **f-strings** for readability; fall back to `str.format` when the template is separate from the data (e.g. loaded from config), and avoid `%` except in legacy code and logging.

```python
name, n = "Ada", 42
f"{name} scored {n}"                 # f-string (3.6+)
"{} scored {}".format(name, n)       # str.format
"%s scored %d" % (name, n)           # printf-style (legacy)
```

#### The format spec mini-language

The part after `:` is `[[fill]align][sign][#][0][width][grouping][.precision][type]`.

| Input     | Format     | Output      | Meaning |
|-----------|------------|-------------|---------|
| `3.14159` | `{:.2f}`   | `3.14`      | 2 decimal places |
| `3.14159` | `{:8.2f}`  | `    3.14`  | width 8, right-aligned |
| `3.14159` | `{:+.2f}`  | `+3.14`     | always show sign |
| `1000000` | `{:,}`     | `1,000,000` | thousands separator |
| `1000000` | `{:_}`     | `1_000_000` | underscore separator |
| `0.25`    | `{:.2%}`   | `25.00%`    | percentage |
| `1000000` | `{:.2e}`   | `1.00e+06`  | scientific |
| `255`     | `{:#x}`    | `0xff`      | hex with prefix |
| `5`       | `{:04d}`   | `0005`      | zero-pad to width 4 |
| `13`      | `{:<9d}`   | `13       ` | left align |
| `13`      | `{:^9d}`   | `   13    ` | center |
| `13`      | `{:_^9d}`  | `___13___`  | center, `_` fill |
| `"text"`  | `{:>10}`   | `      text`| right align string |
| `"text"`  | `{:.2}`    | `te`        | truncate to 2 chars |

Conversion flags use `!` instead of `:`:

```python
f"{obj!r}"   # repr(obj)
f"{obj!s}"   # str(obj)
f"{obj!a}"   # ascii(obj)
```

#### f-string tricks

```python
# self-documenting expressions (3.8+): prints "x=42"
x = 42
print(f"{x=}")

# nested / dynamic format spec
width = 10
f"{value:>{width}.2f}"

# escape literal braces by doubling
f"{{literal}} and {x}"        # '{literal} and 42'

# coerce non-strings before aligning (booleans, numbers)
f"{True!s:>5}"                # '  True'
```

Backslashes can't appear inside the `{}` of an f-string before 3.12. Work around it with `chr(10)` for newlines, or build the string outside:

```python
nl = chr(10)
f"items:{nl}{nl.join(items)}"
# or just:
print("items:", *items, sep="\n")
```

#### Number and byte humanization

Two frequently needed helpers — human-readable byte sizes and next power of two:

```python
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

sizeof_fmt(1536)          # '1.5KiB'

import math
def next_power_of_2(x):
    return 1 << (math.ceil(x) - 1).bit_length()   # 7.5->8, 9->16
```

Base conversions in one format call:

```python
"{0:d} {0:x} {0:o} {0:b}".format(21)   # '21 15 25 10101'
```

---

### Numbers and Math

```python
import math

math.floor(4.7)     # 4
math.ceil(4.1)      # 5
round(5.5)          # 6   - but round(2.5) == 2 (banker's rounding!)
round(3.14159, 2)   # 3.14
abs(-3), 3 ** 2, 7 // 2, 7 % 2, divmod(7, 2)   # 3, 9, 3, 1, (3, 1)
```

> Gotcha: `round()` uses *banker's rounding* (round-half-to-even), so `round(0.5) == 0` and `round(2.5) == 2`. For money, use `decimal.Decimal`.

Rounding to an arbitrary base:

```python
base = 8
base * round(x / base)       # nearest multiple of 8
base * math.ceil(x / base)   # round up to a multiple of 8
```

Floating point is not exact — a classic source of bugs:

```python
0.1 + 0.2 == 0.3             # False!
math.isclose(0.1 + 0.2, 0.3) # True  - use this for float equality

from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True
```

#### Statistics without NumPy

The stdlib `statistics` module covers the basics:

```python
from statistics import mean, median, mode, stdev, multimode
mean([1, 2, 3, 4])          # 2.5
median([1, 2, 3, 4])        # 2.5
mode([1, 1, 2, 3])          # 1  (StatisticsError if tie on <3.8; first on 3.8+)
multimode("aabbbcc")        # ['b']  - all winners

from collections import Counter
Counter([1, 1, 2, 3, 3, 3]).most_common(1)   # [(3, 3)]
```

`Counter.most_common` is the robust "majority vote" tool — see [Dictionaries](#dictionaries).

#### Special values

```python
float("inf"), float("-inf"), float("nan")
math.inf, -math.inf, math.nan

math.isnan(x)      # NaN is never == to anything, including itself
math.isinf(x)
```

---

### Regular Expressions

The `re` module implements Perl-style regexes. Compile patterns you reuse; use raw strings (`r"..."`) so backslashes reach the regex engine intact. For building and debugging complex patterns, [regex101.com](https://regex101.com/) and [pythex.org](https://pythex.org/) are invaluable.

#### The core functions

```python
import re

re.search(pat, s)      # first match anywhere -> Match or None
re.match(pat, s)       # match anchored at the START of s
re.fullmatch(pat, s)   # the whole string must match
re.findall(pat, s)     # list of all matches (or groups)
re.finditer(pat, s)    # iterator of Match objects
re.sub(pat, repl, s)   # substitute
re.split(pat, s)       # split on the pattern
```

```python
re.search(r"\db", "a1bc")   # <Match span=(1, 3), match='1b'>
re.match(r".*\db.*", "a1bc")# needs to describe the whole string
```

#### Flags

Pass via the `flags=` argument or inline as `(?i)` at the start of the pattern.

| Flag  | Long form       | Effect |
|-------|-----------------|--------|
| `re.I`| `re.IGNORECASE` | case-insensitive |
| `re.M`| `re.MULTILINE`  | `^`/`$` match at each line |
| `re.S`| `re.DOTALL`     | `.` matches newlines too |
| `re.X`| `re.VERBOSE`    | ignore whitespace, allow comments in pattern |
| `re.U`| `re.UNICODE`    | Unicode `\w \b` (default in py3) |

#### Groups and assertions

```
(...)         capturing group
(?P<name>...) named capturing group
(?:...)       non-capturing group
(?=...)       positive lookahead      (?!...)  negative lookahead
(?<=...)      positive lookbehind     (?<!...) negative lookbehind
\b  \B        word / non-word boundary
\A  \Z        start / end of string (ignore re.M)
```

Accessing groups on a match:

```python
m = re.search(r"(?P<proto>\w+)://(?P<host>[^/]+)", url)
m.group(0)          # whole match
m.group("host")     # named group
m.groupdict()       # {'proto': ..., 'host': ...}
```

#### Substitution with backreferences and callables

```python
re.sub(r"(\d)", r"\1_t", "a5b")          # 'a5_tb'  - \1 = group 1
re.sub(r"^.*\r", "", buf, count=0, flags=re.M)   # strip tqdm-style \r lines

# a function receives the Match and returns the replacement
lookup = {"1": "one", "2": "two"}
re.sub(r"\d", lambda m: lookup[m.group()], "1 and 2")   # 'one and two'
```

#### Splitting on patterns

```python
re.split(r"[>=<]+", "foo>=1")      # ['foo', '1']
re.split(r" *, *", "a, b ,c")      # ['a', 'b', 'c']  - tolerant of spaces
```

A neat trick — split *before* a delimiter using a zero-width lookahead:

```python
reqs = ["c<1.2.3", "aa==1.3", "bb>=2.4.1"]
{k: v for k, v in (re.split(r"(?=[=<>])", d, maxsplit=1) for d in reqs)}
# {'c': '<1.2.3', 'aa': '==1.3', 'bb': '>=2.4.1'}
```

#### Escaping literal text

When part of your pattern is data, escape it so its metacharacters are literal:

```python
re.escape("a.b*c")                       # 'a\\.b\\*c'
re.findall(rf"torch\s+: {re.escape(ver)}", buf)
```

#### A worked example: text normalization

Combining several ideas — lowercase, strip punctuation, drop stop words, unescape HTML/URL encodings, and tokenize:

```python
import re, string, html, urllib.parse

STOP = {"the", "a", "in", "to", "of", "and", "is", "on", "for"}
_punct = re.compile(f"[{re.escape(string.punctuation)}]")
_stops = re.compile(rf"\b(?:{'|'.join(STOP)})\b", re.I)

def text2words(s):
    s = urllib.parse.unquote(s)   # %20 -> space
    s = html.unescape(s)          # &amp; -> &
    s = _punct.sub("", s.lower())
    s = _stops.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.split(" ")

text2words("The QUICK, brown fox!")   # ['quick', 'brown', 'fox']
```

---

### Lists

Lists are mutable, ordered, and the default general-purpose sequence.

#### Adding and removing

```python
s.append(x)          # add one item at the end
s.extend([a, b])     # add many (in place)
s.insert(0, x)       # prepend (O(n) - shifts everything)
s += [a, b]          # same as extend
s = s + [a, b]       # NEW list (copy) - slower

s.remove(x)          # delete first item == x  (ValueError if missing)
del s[i]             # delete by index
val = s.pop()        # remove & return last (stack: LIFO)
val = s.pop(0)       # remove & return first (queue: FIFO, but O(n))
```

For heavy prepend/pop-left workloads use `collections.deque`, which is O(1) at both ends:

```python
from collections import deque
d = deque([1, 2, 3])
d.appendleft(0)          # O(1) - a list.insert(0, ...) would be O(n)
d.extendleft("abc")      # note: inserts reversed -> deque(['c','b','a',1,2,3])
d.popleft()
```

#### Copying (shallow vs deep)

```python
b = a[:]            # shallow copy
b = list(a)         # shallow copy
import copy
b = copy.copy(a)    # shallow
b = copy.deepcopy(a)# deep - recursively copies nested objects
b = a               # NOT a copy - both names point to the same list!
```

> The classic bug: `listB = listA` then `listB.append(1)` mutates `listA` too, because both names reference one object.

#### Slicing and splicing

Slices read *and* write:

```python
l = [0, 10, 20, 30, 40]
l[1:3]                 # [10, 20]
l[::-1]                # reversed copy
l[2:4] = [200, 300, 400]   # replace a range (can change length)
l[1:1] = [99]              # insert at index 1 without deleting
del l[1:3]                 # delete a range
```

#### Searching and aggregating

```python
l.index(x)               # first index of x (ValueError if missing)
l.count(x)
max(l), min(l), sum(l)
l.index(max(l))          # argmax (position of the largest)

set(a).intersection(b)   # overlap of two lists
[x for x in set(l) if l.count(x) > 1]   # duplicated values

all(v == 0 for v in l)   # all zeros?
any(l)                   # any truthy?
len(max(l, key=len))     # length of the longest sub-item
```

#### Splitting and chunking

```python
# fixed-size chunks, last one may be short
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# python 3.12+
import itertools
list(itertools.batched(range(10), 3))   # [(0,1,2),(3,4,5),(6,7,8),(9,)]

# n roughly-equal chunks
def split(a, n):
    k, m = divmod(len(a), n)
    return [a[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]
```

#### Ranges

```python
range(1, 10, 2)            # 1 3 5 7 9  (lazy, integer only)

import numpy as np         # for float steps
np.arange(0.0, 1.0, 0.1)
np.linspace(0, 1, 11)      # 11 evenly spaced points, endpoint included
```

See [Comprehensions, Iterators and itertools](#comprehensions-iterators-and-itertools) for flattening, zipping, products and more.

---

### Tuples

Tuples are immutable sequences. Because they're immutable they're **hashable** (usable as dict keys and set members), slightly faster than lists, and signal intent ("this collection won't change").

```python
t = (1, 2, 3)
t = 1, 2, 3          # parentheses optional
singleton = (1,)     # the trailing comma is what makes it a tuple
empty = ()

a, b, c = t          # unpacking
first, *rest = t     # first=1, rest=[2, 3]  (star capture)
t2 = t + (4,)        # "append" = build a new tuple

t.count(1)           # occurrences
t.index(2)           # first position
```

Named tuples give you readable field access while staying a tuple:

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
p.x, p[0]            # 1, 1
p._asdict()          # {'x': 1, 'y': 2}

# typed alternative (3.6+)
from typing import NamedTuple
class Point(NamedTuple):
    x: int
    y: int = 0
```

---

### Sets

Sets are unordered collections of unique, hashable items — ideal for membership tests (O(1)) and de-duplication.

```python
a = {1, 2, 3, 4}        # set literal (but {} is an empty DICT!)
empty = set()
b = set([3, 4, 5, 6])

{s**2 for s in range(4)}   # set comprehension -> {0, 1, 4, 9}
```

#### Algebra

```python
a | b   # union                {1,2,3,4,5,6}     a.union(b)
a & b   # intersection         {3,4}             a.intersection(b)
a - b   # difference           {1,2}             a.difference(b)
a ^ b   # symmetric difference {1,2,5,6}         a.symmetric_difference(b)
a <= b  # subset?                                a.issubset(b)
a >= b  # superset?                              a.issuperset(b)
```

#### Mutation

```python
a.add(5)
a.update([6, 7])
a.discard(99)   # no error if missing
a.remove(99)    # KeyError if missing
```

Use `frozenset` for an immutable (hashable) set — e.g. to put sets inside sets or use them as dict keys:

```python
nested = {frozenset({1, 2}), frozenset({3, 4})}
```

---

### Dictionaries

The workhorse mapping. Since **3.7** dicts preserve insertion order as a language guarantee (CPython did so in 3.6). Keys must be hashable.

#### Construction and merging

```python
d = {"a": 1, "b": 2}
d = dict(a=1, b=2)                 # keyword form (string keys only)
d = dict(zip(keys, values))
d = dict.fromkeys(["a", "b"], 0)   # {'a': 0, 'b': 0}

{s: s**2 for s in range(4)}        # comprehension -> {0:0,1:1,2:4,3:9}

d1.update(d2)                      # merge d2 into d1 in place (returns None!)
merged = {**defaults, **overrides} # new dict; later keys win
merged = d1 | d2                   # 3.9+  merge operator
d1 |= d2                           # 3.9+  in-place
```

#### Access with defaults

```python
d["a"]                # KeyError if missing
d.get("a")            # None if missing
d.get("a", 0)         # fallback value
"a" in d              # membership test (checks keys)

v = d.pop("a", None)  # remove & return, with fallback
del d["a"]            # remove (KeyError if missing)

# fetch several keys at once
from operator import itemgetter
itemgetter("a", "b")(d)
```

#### Iteration

```python
for k in d: ...            # keys
for v in d.values(): ...
for k, v in d.items(): ...
```

#### defaultdict — auto-initializing values

Stop writing `if key not in d: d[key] = []`:

```python
from collections import defaultdict

groups = defaultdict(list)
groups["fruit"].append("apple")     # key auto-created with []

counts = defaultdict(int)
counts["x"] += 1                    # starts at 0

nested = defaultdict(lambda: {"n": 0})   # any factory
```

#### Counter — counting made trivial

```python
from collections import Counter

c = Counter(["red", "blue", "red", "green", "blue", "blue"])
# Counter({'blue': 3, 'red': 2, 'green': 1})
c.most_common(2)          # [('blue', 3), ('red', 2)]
c.most_common()[-1]       # least common
sum(c.values())           # grand total
c["red"] += 1             # missing keys read as 0
c + Counter(other)        # combine by adding counts
```

#### Common transformations

```python
# invert (swap keys/values)
{v: k for k, v in d.items()}

# sort a dict by value into a new dict
{k: v for k, v in sorted(d.items(), key=lambda kv: kv[1])}

# build a lookup table from a list
{name: i for i, name in enumerate(classes)}

# merge a list of dicts, summing shared keys
super_d = defaultdict(int)
for sub in dicts:
    for k, v in sub.items():
        super_d[k] += v

# merge a list of dicts, collecting values into lists
super_d = defaultdict(list)
for sub in dicts:
    for k, v in sub.items():
        super_d[k].append(v)
```

#### Attribute-style access

```python
from types import SimpleNamespace
ns = SimpleNamespace(**{"a": 1, "b": 2})
ns.a                 # 1   (but ns["a"] does NOT work)
```

For a richer "dict that's also an object", or comparing nested dicts:

```python
import deepdiff        # pip install deepdiff
deepdiff.DeepDiff(d1, d2)   # structured, recursive difference
```

#### dataclasses — structured records

For anything with named fields, prefer a dataclass over a bare dict — you get types, defaults, `__init__`, `__repr__`, and `__eq__` for free:

```python
from dataclasses import dataclass, field, asdict

@dataclass
class Config:
    lr: float = 1e-3
    layers: int = 12
    tags: list = field(default_factory=list)   # mutable defaults MUST use this
    name: str = "run"

cfg = Config(lr=3e-4)
asdict(cfg)              # -> plain dict, recursively
Config(frozen=True)      # make it immutable & hashable via @dataclass(frozen=True)
```

> Gotcha: never use a mutable default directly (`tags: list = []`) — it would be shared across all instances. Use `field(default_factory=list)`.

---

### Comprehensions, Iterators and itertools

Comprehensions are the Pythonic way to build collections — they're faster than equivalent loops and often clearer.

#### List / dict / set / generator forms

```python
[x*x for x in range(5)]                 # list
{x: x*x for x in range(5)}              # dict
{x % 3 for x in range(10)}              # set
(x*x for x in range(5))                 # generator (lazy, memory-cheap)

[x for x in data if x > 0]              # with filter
[x if x > 0 else 0 for x in data]      # with conditional expression
```

#### Nested comprehensions

The loop order matches a normal nested `for` read left to right; the expression goes first:

```python
# flatten one level: for row in matrix: for x in row
[x for row in matrix for x in row]

# build a list of lists (keep structure)
[[int(x) for x in row.split(",")] for row in text.splitlines()]
```

#### The essential itertools

```python
import itertools as it

it.chain(a, b)                 # concatenate iterables lazily
it.chain.from_iterable(lists)  # flatten one level, lazily
it.product(a, b)               # Cartesian product (nested loops)
it.product(a, repeat=2)        # all pairs incl. self-pairs
it.permutations(a, 2)          # ordered arrangements
it.combinations(a, 2)          # unordered selections
it.groupby(sorted_data, key)   # group consecutive items (SORT first!)
it.accumulate(nums)            # running totals
it.islice(iterable, 10)        # slice any iterable (even infinite)
it.count(0, 2), it.cycle(a), it.repeat(x, 3)   # infinite generators
```

#### Flattening, zipping, unzipping

```python
# flatten arbitrarily nested iterables (mixed depth, skip str/bytes)
from collections.abc import Iterable
def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

# zip pairs up; zip(*...) unzips
list(zip([1, 2, 3], "abc"))     # [(1,'a'),(2,'b'),(3,'c')]
xs, ys = zip(*pairs)            # unzip back into two tuples

# sort two parallel lists together by the first
ys, xs = zip(*sorted(zip(ys, xs)))
```

> `zip` stops at the shortest input. Use `itertools.zip_longest` to pad, or `zip(a, b, strict=True)` (3.10+) to *require* equal lengths.

#### Generators and `yield`

Generators produce values lazily, which keeps memory flat for large or infinite streams:

```python
def read_big(path):
    with open(path) as f:
        for line in f:            # one line in memory at a time
            yield line.rstrip()

def integers():
    n = 0
    while True:
        yield n
        n += 1

# the walrus operator (3.8+) streams nicely too
while (chunk := f.read(8192)):
    process(chunk)
```

---

### Functions

#### Arguments: positional, keyword, defaults, *args/**kwargs

```python
def f(a, b=2, *args, key=None, **kwargs):
    ...

def g(a, b, /, c, *, d):     # a,b positional-only; d keyword-only (3.8+)
    ...
```

> Gotcha: default arguments are evaluated **once**, at definition time. Never use a mutable default:
> ```python
> def bad(x, acc=[]):      # acc is shared across calls!
>     acc.append(x); return acc
> def good(x, acc=None):
>     acc = [] if acc is None else acc
> ```

#### Pass-by-object-reference

Python passes references by assignment. Mutating a mutable argument in place is visible to the caller; rebinding the name is not:

```python
def mutate(a):  a[0] = 99      # caller sees the change
def rebind(a):  a = [99]       # caller does NOT see it
```

Immutable objects (int, str, tuple) can't be changed in place at all, so functions can only communicate back via return values.

#### Closures

Inner functions capture their enclosing scope. To *reassign* a captured variable use `nonlocal`:

```python
def make_counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
```

> The late-binding trap: closures capture variables, not values. In a loop, bind the current value with a default argument:
> ```python
> funcs = [lambda x, v=v: v + x for v in range(4)]   # correct
> ```

#### functools: partial, caching, reduce

```python
from functools import partial, lru_cache, cache, reduce
from operator import mul

add10 = partial(lambda a, b: a + b, 10)   # preset an argument
reduce(mul, [1, 2, 3, 4])                 # 24

@cache                       # 3.9+ unbounded memoization
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)

@lru_cache(maxsize=1000)     # bounded memoization
def slow(x): ...
```

#### Decorators

A decorator wraps a function to add behavior. Use `functools.wraps` to preserve the wrapped function's metadata:

```python
from functools import wraps

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        import time
        t = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__} took {time.perf_counter() - t:.3f}s")
    return wrapper

@timed
def work(): ...
```

A robust pattern for optional dependencies — provide a no-op fallback so code keeps working if a decorator isn't available:

```python
try:
    from torch.distributed.elastic.multiprocessing.errors import record
except ImportError:
    def record(fn):   # no-op
        return fn
```

#### Introspecting the call stack

```python
import inspect, sys
inspect.currentframe().f_code.co_name            # this function's name
inspect.currentframe().f_back.f_code.co_name     # the caller's name
sys._getframe().f_code.co_name                   # same, faster/uglier

# does a function accept a given parameter?
"device_id" in inspect.signature(some_fn).parameters
```

---

### Classes and Objects

#### Dunder (special) methods

They hook classes into language syntax:

```python
class Vector:
    def __init__(self, x, y):      # constructor
        self.x, self.y = x, y
    def __repr__(self):            # unambiguous, for developers/REPL
        return f"Vector({self.x}, {self.y})"
    def __str__(self):             # readable, for users (falls back to repr)
        return f"({self.x}, {self.y})"
    def __eq__(self, o):           # ==
        return (self.x, self.y) == (o.x, o.y)
    def __add__(self, o):          # +
        return Vector(self.x + o.x, self.y + o.y)
    def __len__(self):             # len()
        return 2
    def __call__(self, k):         # make instances callable: v(3)
        return Vector(self.x * k, self.y * k)
```

Operator hooks include `__sub__`, `__mul__`, `__truediv__`, `__pow__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__ne__`, `__neg__`, `__abs__`, `__getitem__`, `__setitem__`, `__contains__`, `__iter__`, and more.

A quick vertical dump for debugging:

```python
import json
def __repr__(self):
    return json.dumps(self.__dict__, sort_keys=True, indent=4, default=str)
```

#### Inheritance

```python
class Base:
    def __init__(self):
        print(f"{__class__.__name__}.__init__")   # the DEFINING class' name

class Child(Base):
    def __init__(self):
        super().__init__()        # cooperative init up the MRO

import inspect
inspect.getmro(Child)             # method resolution order (all superclasses)
Child.__subclasses__()            # direct subclasses
```

#### Dynamic attributes and delegation

```python
getattr(obj, "attr")            # AttributeError if missing
getattr(obj, "attr", default)   # safe
setattr(obj, "attr", value)
hasattr(obj, "attr")
delattr(obj, "attr")

# call methods by name
for name in ["start", "stop"]:
    getattr(obj, name)()
```

Delegate unknown attributes to a member (composition over inheritance) via `__getattr__`, which is only called when normal lookup fails:

```python
class Wrapper:
    def __init__(self, inner):
        self._inner = inner
    def __getattr__(self, name):
        return getattr(self._inner, name)   # forward to the wrapped object
```

#### Importing a class from strings

```python
import importlib
def load(fqcn):                  # "package.module.ClassName"
    module_name, class_name = fqcn.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)
```

#### Null-object / dummy classes

Useful as safe stand-ins in tests or optional code paths:

```python
class Dummy:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return self
    def __getattr__(self, _):    return self   # any attr/method -> itself
```

#### Context managers

Guarantee setup/teardown with `with`. The easiest way is `@contextmanager`:

```python
from contextlib import contextmanager

@contextmanager
def opened(path):
    f = open(path)
    try:
        yield f              # value bound by `as`
    finally:
        f.close()           # always runs, even on exceptions

with opened("x.txt") as f:
    ...
```

`contextlib.nullcontext()` is a do-nothing manager, perfect for conditional `with` blocks:

```python
from contextlib import nullcontext
ctx = autocast() if use_amp else nullcontext()
with ctx:
    ...
```

---

### Dates and Times

The stdlib splits time handling across `datetime`, `time`, and `timeit`. Prefer `datetime` for calendar work, `time.perf_counter()` for measuring durations.

#### Parsing and formatting

```python
from datetime import datetime, timedelta

datetime.now().strftime("%Y-%m-%d %H:%M:%S")     # format -> string
datetime.strptime("2013-02-01 05:00", "%Y-%m-%d %H:%M")   # parse <- string

import dateutil.parser        # pip install python-dateutil - guesses the format
dateutil.parser.parse("Feb 1 2013 5am")
```

Common `strftime` codes: `%Y` year, `%m` month, `%d` day, `%H`/`%I` hour 24/12, `%M` minute, `%S` second, `%p` AM/PM, `%a`/`%A` weekday, `%b`/`%B` month name, `%j` day-of-year, `%w` weekday number, `%Z` timezone, `%%` literal `%`.

#### Time zones (be explicit!)

```python
from datetime import datetime, timezone
datetime.now(timezone.utc)              # aware UTC "now" (preferred)
datetime.now()                          # naive local time - avoid for storage

from zoneinfo import ZoneInfo           # 3.9+
datetime.now(ZoneInfo("America/New_York"))
```

> Store and transmit timestamps in UTC; convert to local only for display. "Naive" datetimes (no tzinfo) are a frequent source of off-by-hours bugs.

#### Arithmetic and durations

```python
diff = dt2 - dt1                        # a timedelta
diff.days, diff.seconds, diff.total_seconds()
dt + timedelta(hours=3, minutes=30)

str(timedelta(seconds=666))             # '0:11:06'
str(diff).split(".")[0]                 # drop microseconds for display
```

#### Measuring elapsed time

```python
import time
t0 = time.perf_counter()                # monotonic, high resolution
work()
print(f"{time.perf_counter() - t0:.3f}s")

time.time()                             # wall-clock epoch seconds (can jump!)
time.sleep(2)
```

A reusable timing context manager:

```python
from contextlib import contextmanager
from timeit import default_timer as timer

@contextmanager
def elapsed():
    t0 = timer()
    yield lambda: timer() - t0
    # (final value frozen when the block exits)

with elapsed() as t:
    work()
    print(t())
```

For micro-benchmarks use `timeit`, which repeats and averages:

```python
import timeit
timeit.timeit("sorted(data)", globals=globals(), number=1000)
```

---

## Part II: Runtime and Environment

### Modules and Imports

#### sys.path — where imports come from

```python
import sys
print("\n".join(sys.path))       # the import search path, in order
```

Add a directory so sibling modules can be imported, computing paths relative to the current file (Perl `FindBin` style) rather than the CWD:

```python
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = Path(__file__).resolve().parents[2]      # N levels up
for p in (str(root),):
    if p not in sys.path:                        # avoid duplicates
        sys.path.insert(0, p)                    # 0 = highest precedence
```

Set it externally via the `PYTHONPATH` env var:

```bash
PYTHONPATH="$PWD/src:$PYTHONPATH" python app.py
```

#### Inspecting and reloading modules

```python
import sys
sys.modules["numpy"]              # module object; where it was loaded from
"numpy" in sys.modules           # already imported? (aliases like np don't count)

from importlib import reload
import mymod
mymod = reload(mymod)            # pick up code changes in a REPL
```

> After `reload`, objects created before the reload still reference the *old* classes. Recreate them to use the new definitions.

#### Dynamic import

```python
import importlib
mod = importlib.import_module("package.module")
cls = getattr(mod, "ClassName")
```

---

### Files, Paths and I/O

Prefer `pathlib.Path` for path manipulation — it's object-oriented, cross -platform, and replaces most of `os.path`.

#### pathlib basics

```python
from pathlib import Path

p = Path("/tmp/foo/bar.txt")
p.name          # 'bar.txt'
p.stem          # 'bar'
p.suffix        # '.txt'
p.parent        # Path('/tmp/foo')
p.parents[1]    # Path('/tmp')
p.with_suffix(".md")     # swap extension
p.with_name("baz.txt")   # swap filename

Path.cwd()               # current directory
Path.home()              # home directory
(Path.cwd() / "sub" / "file.txt")   # join with /
```

#### Existence, type, metadata

```python
p.exists()
p.is_file()
p.is_dir()
p.stat().st_size          # size in bytes
p.stat().st_mtime         # modified time (epoch seconds)

# is src newer than dst?
if src.stat().st_mtime > dst.stat().st_mtime: ...
```

#### Create, move, delete

```python
Path("a/b/c").mkdir(parents=True, exist_ok=True)   # mkdir -p
p.touch()                                          # create empty / update mtime
p.rename("new.txt")                                # move/rename
p.unlink(missing_ok=True)                          # delete file (3.8+)

import shutil
shutil.copy2(src, dst)          # copy incl. metadata; dst may be a dir
shutil.move(src, dst)
shutil.rmtree(path, ignore_errors=True)   # delete a dir tree
shutil.which("git")             # locate an executable on PATH (or None)
```

#### Listing and globbing

```python
list(p.iterdir())               # immediate children
list(p.glob("*.py"))            # non-recursive glob
list(p.rglob("*.py"))           # recursive glob
list(p.glob("**/"))             # subdirectories only
```

#### Reading and writing

The one-line forms cover most cases:

```python
text = Path("f.txt").read_text(encoding="utf-8")
Path("f.txt").write_text(data, encoding="utf-8")
raw  = Path("f.bin").read_bytes()

# streaming with a context manager (always use `with`)
with open("f.txt", "w") as f:
    f.write("hi")
with open("f.txt", "a") as f:   # append
    f.write("\n more")

# read as a list of lines without trailing newlines
lines = Path("f.txt").read_text().splitlines()

# process a line at a time (memory-friendly)
with open("f.txt") as f:
    for line in f:
        handle(line.rstrip("\n"))

# in-place find/replace
p = Path("f.txt")
p.write_text(p.read_text().replace("old", "new"))
```

Detect binary files by sniffing for a NUL byte:

```python
with open(path, "rb") as f:
    if b"\x00" in f.read(1024):
        ...     # looks binary; skip
```

For very large files, memory-map instead of loading into RAM:

```python
import mmap
with open(path, "r") as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    for line in iter(mm.readline, b""):
        ...
```

#### Temporary files and directories

Let `tempfile` pick safe, unique names and clean up for you:

```python
import tempfile

with tempfile.TemporaryDirectory() as d:      # auto-removed on exit
    path = Path(d) / "scratch.txt"
    ...

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=True) as f:
    f.write("{}")
    f.flush()
    use(f.name)
```

---

### Environment Variables and Program Arguments

#### Environment variables

```python
import os

os.environ["MYVAR"] = "foo"              # values are always strings
os.environ.get("MYVAR")                  # None if unset
os.environ.get("MYVAR", "default")       # fallback
"HOME" in os.environ                     # existence check
os.environ.pop("MYVAR", None)            # delete (safe)

# unset everything matching a pattern
for key in list(os.environ):             # copy keys - we mutate while iterating
    if key.startswith("SLURM_"):
        os.environ.pop(key)
```

Pass a modified environment to a subprocess without disturbing your own:

```python
import subprocess
env = {**os.environ, "RSYNC_PASSWORD": "secret"}   # copy + override
subprocess.Popen(cmd, env=env)
```

#### argparse — the built-in CLI parser

```python
import argparse

parser = argparse.ArgumentParser(description="Process a CSV.")
parser.add_argument("input", help="input file")                # positional
parser.add_argument("output", nargs="?", help="optional out")  # optional pos.
parser.add_argument("-n", "--name", default="grid", help="name")
parser.add_argument("-v", "--verbose", action="store_true")    # boolean flag
parser.add_argument("--ids", type=int, nargs="+")              # list of ints
parser.add_argument("--mode", choices=["a", "b", "all"], default="all")
args = parser.parse_args()
# use args.input, args.name, args.verbose, ...

from pprint import pprint
pprint(vars(args))               # dump all parsed values
```

For richer CLIs consider [`click`](https://click.palletsprojects.com/), [`typer`](https://typer.tiangolo.com/) (type-hint based), or `fire`.

#### Replaying the exact command line

Handy for logging exactly how a script was invoked:

```python
import sys, shlex
print(sys.executable, " ".join(map(shlex.quote, sys.argv)))
```

---

### Subprocess and Shell Integration

`subprocess.run` is the modern, high-level entry point. Pass a *list* of arguments (not a shell string) to avoid quoting bugs and shell injection.

```python
import subprocess

r = subprocess.run(["ls", "-l"], capture_output=True, text=True)
r.returncode        # 0 on success
r.stdout            # captured stdout as str (text=True)
r.stderr

subprocess.run(["make"], check=True)      # raise CalledProcessError on failure

# capture output as a list of lines
out = subprocess.run(["ls"], capture_output=True, text=True).stdout.splitlines()
```

Long-running or streaming processes use `Popen`:

```python
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
for line in p.stdout:
    print(line, end="")
p.wait()

# fully detached child that outlives the parent
subprocess.Popen(cmd, start_new_session=True,
                 stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
```

Propagate termination signals to child processes so nothing is orphaned:

```python
import signal, sys

processes = []
def terminate(signum, frame):
    for p in processes:
        p.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, terminate)
signal.signal(signal.SIGTERM, terminate)
```

> Only use `shell=True` if you truly need shell features, and never with untrusted input. Otherwise pass an argument list.

---

### Serialization: JSON, CSV, Pickle, XML, gzip

#### JSON

```python
import json

json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)   # -> str
json.loads('{"a": 1}')                                          # str -> obj

with open("f.json", "w", encoding="utf-8") as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)
with open("f.json", encoding="utf-8") as f:
    obj = json.load(f)
```

JSON Lines (one JSON object per line) is the standard for large/streamed data:

```python
# write
with open("data.jsonl", "w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# read
with open("data.jsonl", encoding="utf-8") as f:
    records = [json.loads(line) for line in f]
```

Serializing custom types — teach the encoder about dataclasses:

```python
import dataclasses, json

class DataclassEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

json.dumps(cfg, cls=DataclassEncoder)
```

Tolerating slightly malformed JSON (trailing commas etc.) — parse it as YAML, or use `json-repair`:

```python
import yaml
yaml.safe_load('{"a": 1, "b": 2,}')     # trailing comma OK in YAML
```

#### CSV

Always use the `csv` module (it handles quoting/escaping), not manual `split`:

```python
import csv

with open("data.csv", newline="") as f:
    for row in csv.reader(f):            # each row is a list of strings
        ...
    # or, with a header row:
    for row in csv.DictReader(f):        # each row is a dict
        row["name"], row["age"]

with open("out.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "age"])
    w.writerows([["Ada", 36], ["Bob", 40]])
```

#### Pickle

Python-native object serialization. **Never unpickle untrusted data** — it can execute arbitrary code.

```python
import pickle
with open("obj.pkl", "wb") as f:
    pickle.dump(obj, f)
with open("obj.pkl", "rb") as f:
    obj = pickle.load(f)
```

#### gzip

```python
import gzip
with gzip.open("f.gz", "wt", encoding="utf-8") as f:   # text mode
    f.write("hello")
with gzip.open("f.gz", "rt", encoding="utf-8") as f:
    data = f.read()
```

#### XML (streaming, memory-safe)

For big XML, iterate and clear as you go instead of building a full tree:

```python
from lxml import etree

def iter_tag(source, tag):
    context = etree.iterparse(source, events=("end",))
    for _, elem in context:
        if elem.tag == tag:
            yield elem
            elem.clear()             # free the element's memory
```

#### Archives

```python
import tarfile, zipfile

with tarfile.open("a.tar.gz", "r:gz") as t:
    t.extractall("out/")
with zipfile.ZipFile("a.zip") as z:
    z.extractall("out/")
```

---

### Concurrency: Processes, Threads and the GIL

CPython has a **Global Interpreter Lock (GIL)**: only one thread executes Python bytecode at a time. The practical rule of thumb:

- **CPU-bound** work → `multiprocessing` (or `ProcessPoolExecutor`): real parallelism across cores.
- **I/O-bound** work (network, disk) → threads or `asyncio`: the GIL is released during blocking I/O, so threads help here.

#### Process pool

```python
import multiprocessing as mp

def work(item):
    return item * item

with mp.Pool(processes=4) as pool:
    results = pool.map(work, range(10))
```

#### concurrent.futures — one API for both

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=8) as ex:      # I/O-bound
    results = list(ex.map(fetch, urls))

with ProcessPoolExecutor() as ex:                  # CPU-bound
    results = list(ex.map(crunch, chunks))
```

#### A background monitoring thread

Daemon threads die with the main program — useful for lightweight monitors:

```python
import threading, time

stop = False
def monitor():
    while not stop:
        sample_something()
        time.sleep(0.1)

t = threading.Thread(target=monitor, daemon=True)
t.start()
```

---

### Networking

#### Sockets and ports

```python
import socket

socket.gethostname()     # short hostname
socket.getfqdn()         # fully-qualified

def port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

# grab a free port from the OS
with socket.socket() as s:
    s.bind(("", 0))
    free_port = s.getsockname()[1]
```

#### HTTP with requests

```python
import requests

r = requests.get(url, timeout=10,
                 headers={"User-Agent": "Mozilla/5.0"})
r.status_code            # 200
r.headers["content-type"]
r.text                   # body as str
r.json()                 # parsed JSON (if applicable)
r.url                    # final URL after redirects
for h in r.history:      # redirect chain
    print(h.status_code, h.url)

# reuse a connection / share cookies across calls
sess = requests.Session()
sess.get("https://example.com/login")
sess.get("https://example.com/data")
```

> Always set a `timeout`. Without it a hung server hangs your program forever.

---

## Part III: Debugging, Profiling and Testing

### Printing, Logging and Output Control

#### print, stderr, and separators

```python
print("a", "b", sep=", ", end="\n")
print("error", file=sys.stderr)
print("no newline", end="")
print(*mylist, sep="\n")            # unpack an iterable onto separate lines
```

Overwriting the current line (progress bars) with carriage return and a VT100 "erase line" escape:

```python
print("working...", end="")
print("\33[2K\rdone", end="")       # \33[2K clears the whole line
```

#### Unbuffered output

Output can appear out of order (or vanish on crash) when buffered. Force flushing:

```python
print("live", flush=True)           # per-call
# or globally:
#   python -u script.py
#   PYTHONUNBUFFERED=1 python script.py
sys.stdout.reconfigure(line_buffering=True)   # 3.7+
```

#### Tee: print to console and file at once

```python
import re, sys

class Tee:
    """Duplicate stdout to a file. Usage: sys.stdout = Tee('log.txt')."""
    def __init__(self, filename):
        self.stdout = sys.stdout
        self.file = open(filename, "a")
        sys.stdout = self
    def write(self, msg):
        self.stdout.write(msg)
        self.file.write(re.sub(r"^.*\r", "", msg, flags=re.M))  # strip \r noise
    def flush(self):
        self.stdout.flush(); self.file.flush()
    def close(self):
        sys.stdout = self.stdout; self.file.close()
```

Restore the originals when done:

```python
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
```

#### logging — prefer it over print for real programs

`logging` gives you levels, timestamps, module names, and per-module control.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)
log.debug("verbose"); log.info("normal"); log.warning("hmm")
log.error("bad"); log.critical("fatal")
log.exception("boom")     # ERROR + traceback; call inside an except block
```

Turn down noisy third-party loggers:

```python
logging.getLogger("urllib3").setLevel(logging.WARNING)

import re
def set_global_logging_level(level=logging.ERROR, prefixes=("",)):
    pat = re.compile(rf"^(?:{'|'.join(prefixes)})")
    for name in logging.root.manager.loggerDict:
        if pat.match(name):
            logging.getLogger(name).setLevel(level)

set_global_logging_level(logging.ERROR, ["transformers", "torch"])
```

#### warnings

```python
import warnings

warnings.warn("deprecated, use bar()", DeprecationWarning)

warnings.simplefilter("ignore", category=FutureWarning)   # silence a category
with warnings.catch_warnings():                           # scoped
    warnings.simplefilter("ignore")
    noisy_call()

warnings.filterwarnings("error")     # turn warnings into exceptions (find them!)
```

Externally: `python -W error script.py` or `PYTHONWARNINGS=error`. Filter actions: `default`, `error`, `always`, `module`, `once`, `ignore`.

---

### Debugging

#### The interactive debugger

Drop a breakpoint anywhere; execution stops and you get a prompt:

```python
breakpoint()                     # 3.7+  honors the PYTHONBREAKPOINT env var
import pdb; pdb.set_trace()      # classic
import ipdb; ipdb.set_trace()    # nicer, needs `pip install ipdb`
```

Run a whole script under the debugger, or post-mortem after a crash:

```bash
python -m pdb script.py          # start under pdb
python -m pdb -c continue app.py # run; drop into pdb on an uncaught exception
```

Key pdb commands: `n` (next), `s` (step in), `c` (continue), `r` (return), `l`/`ll` (list source), `p`/`pp expr` (print), `w` (where/stack), `u`/`d` (up/down the stack), `b file:line` (breakpoint), `q` (quit), `interact` (a full Python REPL in the current frame).

#### Debugging forked / multiprocess code

The standard `pdb` breaks when stdin isn't the terminal (subprocesses). Fix it:

```python
import sys, pdb

class ForkedPdb(pdb.Pdb):
    """pdb that works inside forked processes."""
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open("/dev/stdin")
            super().interaction(*args, **kwargs)
        finally:
            sys.stdin = _stdin

ForkedPdb().set_trace()
```

For remote processes there's `remote-pdb` (debug over a TCP socket) and `pudb` (a full-screen console debugger: `python -m pudb.run script.py`).

#### Getting a traceback out of a stuck or crashed process

`faulthandler` can dump every thread's stack on a signal or timer — the fastest way to see *where* a hung program is stuck:

```python
import faulthandler, signal
faulthandler.register(signal.SIGUSR1)          # then: kill -USR1 <pid>
faulthandler.dump_traceback_later(20, repeat=True)   # dump every 20s

# enable native-crash tracebacks (segfaults):
#   python -X faulthandler script.py
```

Attach to an *already running* process without any code changes using [`py-spy`](https://github.com/benfred/py-spy):

```bash
pip install py-spy
py-spy dump --pid 12345      # one-shot stack dump of every thread
py-spy top  --pid 12345      # live, top-like view of where time goes
py-spy top -- python app.py  # launch under py-spy (no sudo needed)
```

For segfaults in C extensions, run under `gdb`:

```bash
gdb -ex r --args python -m pytest -sv tests/test_crash.py
# on crash:  bt   (backtrace),  c  (continue)
gdb --pid 12345              # attach to a hung process
(gdb) thread apply all bt    # all threads' native stacks
```

#### Programmatic stack traces

```python
import traceback
traceback.print_stack(limit=6)                 # current stack, no exception
for line in traceback.format_stack():          # as strings
    print(line.strip())
```

#### Tracing execution

```python
python -m trace --trace script.py     # print every line as it runs
```

A filtered call tracer (only your package, indented by depth):

```python
import re, sys, os.path
only = re.compile(r"mypackage")

def tracer(frame, event, arg, depth=[0]):
    if only.search(frame.f_code.co_filename):
        if event == "call":
            depth[0] += 2
            print(" " * depth[0] + "> " + frame.f_code.co_name)
        elif event == "return":
            depth[0] -= 2
    return tracer

sys.settrace(tracer)
```

---

### Introspection and Object Inspection

#### What is this thing?

```python
type(obj)                 # its class
isinstance(obj, (int, float))
obj.__class__.__name__    # class name as a string
dir(obj)                  # attribute & method names
vars(obj)                 # __dict__ (instance attributes)
id(obj); hex(id(obj))     # identity / address
callable(obj)             # is it callable?
```

Fully-qualified class name:

```python
def full_class_name(obj):
    cl = obj.__class__
    return f"{cl.__module__}.{cl.__qualname__}"
```

#### Dump an object's attributes

```python
def dump(obj):
    for name in dir(obj):
        if not name.startswith("__"):
            print(f"{name} = {getattr(obj, name)!r}")

# attributes only (no methods)
attrs = [k for k in vars(obj)]
# methods only
import inspect
methods = [k for k in dir(obj)
           if not k.startswith("__") and inspect.isroutine(getattr(obj, k))]
```

#### Prettier dumps

```python
from pprint import pprint
pprint(vars(obj))
pprint(globals()); pprint(locals())

from rich import inspect          # pip install rich  - great in a terminal
inspect(obj, methods=True)
```

Reach the caller's locals from inside a helper (for debug tooling):

```python
import inspect
def show_caller_locals():
    frame = inspect.currentframe().f_back
    try:
        print(frame.f_locals)
    finally:
        del frame                 # break the reference cycle
```

---

### Profiling CPU and Memory

Measure before you optimize. Start coarse (which function is slow?), then go fine (which line?).

#### Timing quick experiments

```python
import timeit
timeit.timeit("sorted(data)", globals=globals(), number=1000)

from timeit import default_timer as timer
t0 = timer(); work(); print(f"{timer() - t0:.3f}s")
```

#### cProfile — function-level CPU profiling

```bash
python -m cProfile -s tottime script.py     # sort by time in the function itself
python -m cProfile -s cumtime -m mymodule   # sort by cumulative time
python -m cProfile -o out.pstats script.py  # save for later analysis
```

In code, and reading a saved profile:

```python
import cProfile
from pstats import Stats, SortKey

with cProfile.Profile() as pr:
    run()
Stats(pr).sort_stats(SortKey.CUMULATIVE).print_stats(20)   # top 20
```

Columns: `ncalls` (calls; `12/2` means recursion — total/primitive), `tottime` (time in the function excluding sub-calls), `cumtime` (including sub-calls).

Visualize the call graph:

```bash
pip install gprof2dot
python -m cProfile -o p.pstats script.py
gprof2dot -f pstats p.pstats | dot -Tsvg -o callgraph.svg
```

#### line_profiler — line-level CPU profiling

```bash
pip install line_profiler
# decorate the hot function with @profile (no import needed), then:
kernprof -l script.py
python -m line_profiler script.py.lprof
```

#### tracemalloc — where Python memory goes

```python
import tracemalloc
tracemalloc.start()
run()
current, peak = tracemalloc.get_traced_memory()
print(f"current={current/2**20:.1f}MiB peak={peak/2**20:.1f}MiB")
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:10]:
    print(stat)
tracemalloc.stop()
```

#### Process memory with psutil

```python
import psutil
p = psutil.Process()
p.memory_info().rss     # Resident Set Size - what most tools report
p.memory_full_info().uss# Unique Set Size - freed if the process died now
p.memory_info().vms     # Virtual Memory Size
```

Whole-program peak memory, no code changes:

```bash
/usr/bin/time -v python script.py     # see "Maximum resident set size"
```

Size of individual objects:

```python
import sys
sys.getsizeof(obj)             # shallow, built-in types only

import objsize                 # pip install objsize - recursive/deep
objsize.get_deep_size(obj)
```

#### Finding leaks

Normal objects free immediately (refcounting); cycles wait for the garbage collector. To hunt leaks:

```python
import gc
gc.collect()
print(gc.garbage)              # uncollectable objects

import objgraph                # pip install objgraph
objgraph.show_most_common_types()
objgraph.show_growth()         # what grew since last call?
```

Other tools worth knowing: [`memray`](https://github.com/bloomberg/memray) (tracks C/C++ allocations too), `memory_profiler` (line-by-line RAM), [`pyinstrument`](https://github.com/joerick/pyinstrument) (statistical profiler with a readable call tree).

---

### Exceptions and Error Handling

#### Raising and catching

Pick the most specific built-in exception (see the [exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)):

```python
raise ValueError("bad argument: expected a positive int")

try:
    risky()
except FileNotFoundError:
    handle_missing()
except (KeyError, IndexError) as e:   # catch several
    log.warning("lookup failed: %s", e)
except Exception as e:                # broad catch — usually re-raise
    raise
else:
    ran_without_error()               # runs only if no exception
finally:
    cleanup()                         # always runs
```

#### Re-raising and chaining

```python
try:
    func()
except Exception as e:
    if "out of memory" in str(e):
        handle()
    else:
        raise                # re-raise the SAME exception, preserving traceback

# wrap a low-level error in a domain error, keeping the cause
try:
    parse()
except ValueError as e:
    raise ConfigError("invalid config") from e     # sets __cause__

# suppress the chained context ("During handling ..."):
raise ConfigError("invalid config") from None
```

#### Custom exceptions

```python
class ConfigError(Exception):
    """Raised when configuration is invalid."""

class RetryableError(ConfigError):
    """A ConfigError that callers may retry."""
```

#### Good habits

- Catch the narrowest exception that makes sense; a bare `except:` also swallows `KeyboardInterrupt` and `SystemExit`.
- Never `except: pass` silently — at minimum log it.
- Use `try/finally` or context managers to guarantee cleanup.
- Add context to the message; the traceback already tells you *where*.

---

### Testing with pytest and unittest

`pytest` is the de-facto standard: plain `assert`, powerful fixtures, and a huge plugin ecosystem. `unittest` ships with Python and shows up in many codebases.

#### pytest basics

```python
# test_math.py  -- files test_*.py, functions test_*
import pytest

def test_add():
    assert 1 + 1 == 2

def test_raises():
    with pytest.raises(ValueError, match="positive"):
        int("not a number")

@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (2, 3, 5)])
def test_add_many(a, b, expected):
    assert a + b == expected
```

```bash
pytest                      # discover & run everything
pytest tests/test_x.py::test_add   # one test
pytest -k "add and not slow"       # select by name expression
pytest -x --ff                     # stop on first failure, failed-first
pytest -q                          # quiet
```

Useful output flags: `-s` (show prints), `-rA` (show captured output for all outcomes), `-rs` (why tests were skipped), `--disable-warnings`, `--color=no`.

#### Fixtures

Fixtures provide setup/teardown and reusable resources; request them by name:

```python
import pytest

@pytest.fixture
def tmp_config(tmp_path):          # tmp_path is a built-in fixture (a Path)
    p = tmp_path / "cfg.json"
    p.write_text("{}")
    yield p                        # code after yield is teardown
    # (nothing to clean up here; tmp_path is auto-removed)

def test_reads_config(tmp_config):
    assert tmp_config.exists()
```

Built-in fixtures worth knowing: `tmp_path`, `tmp_path_factory`, `capsys`/ `capfd` (capture output), `monkeypatch` (patch env/attrs safely), `caplog`.

#### Capturing output

```python
def test_prints(capsys):
    print("hello")
    assert capsys.readouterr().out == "hello\n"

def test_env(monkeypatch):
    monkeypatch.setenv("MODE", "test")
    monkeypatch.setattr("mymod.CONST", 42)
```

#### Parallel and slow tests

```bash
pip install pytest-xdist
pytest -n auto                 # run across all CPU cores
pytest --dist=loadscope        # keep a class's tests on one worker

pip install pytest-timeout
pytest --timeout=180           # fail tests that hang
```

Give parallel workers distinct resources (e.g. network ports) using the worker id:

```python
import os
def unique_port(base=11000):
    return base + int(os.environ.get("PYTEST_XDIST_WORKER", "gw0")[2:])
```

#### unittest

```python
import unittest

class TestThings(unittest.TestCase):
    def setUp(self):    self.data = [1, 2, 3]
    def tearDown(self): ...

    def test_sum(self):
        self.assertEqual(sum(self.data), 6)

    def test_raises(self):
        with self.assertRaises(ValueError):
            int("x")

    def test_skip(self):
        self.skipTest("not ready")

if __name__ == "__main__":
    unittest.main()
```

Capturing stdout under `unittest` (where `capsys` isn't available) via `mock.patch`:

```python
import io, unittest.mock

@unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
def test_output(mock_stdout):
    print("hi")
    assert "hi" in mock_stdout.getvalue()
```

> pytest can run `unittest.TestCase` classes directly, so you can adopt pytest's runner without rewriting existing tests.

---

## Part IV: Packaging and Tooling

### Versions and Dependencies

#### Checking your Python version

```python
import sys
sys.version_info                 # e.g. sys.version_info(major=3, minor=11, ...)

MIN = (3, 8)
if sys.version_info < MIN:
    sys.exit(f"Python {MIN[0]}.{MIN[1]}+ required")
```

#### Querying installed package versions

`pkg_resources` is deprecated; use `importlib.metadata` (stdlib, 3.8+):

```python
from importlib.metadata import version, PackageNotFoundError

try:
    print(version("requests"))
except PackageNotFoundError:
    print("requests is not installed")
```

#### Comparing versions correctly

Don't compare version strings lexically (`"2.10" < "2.9"` is `True`!). Use `packaging`, which understands pre/post/dev releases:

```python
from packaging import version
version.parse("2.3.1.dev0")  < version.parse("2.3.1")   # True
version.parse("2.3.1.post1") > version.parse("2.3.1")   # True

# enforce a minimum
got = version("tqdm")
if version.parse(got) < version.parse("4.60"):
    raise ImportError(f"tqdm>=4.60 required, found {got}")
```

#### Virtual environments

Isolate each project's dependencies:

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
deactivate
```

Faster modern alternatives: [`uv`](https://github.com/astral-sh/uv) and [`pip-tools`](https://github.com/jazzband/pip-tools) for locked, reproducible installs.

---

### Packaging and Requirements

#### Generating a requirements file from imports

```bash
pip install pipreqs
pipreqs /path/to/project      # scans imports -> requirements.txt
```

`pip freeze > requirements.txt` captures the *entire* environment (including transitive deps); `pipreqs` captures only what your code imports.

#### Modern packaging with pyproject.toml

New projects should use `pyproject.toml` (PEP 621) rather than `setup.py`:

```toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = ["requests>=2.28", "packaging"]

[project.scripts]
mytool = "mypackage.cli:main"      # console entry point
```

Build distributions:

```bash
pip install build
python -m build                    # produces sdist (.tar.gz) + wheel (.whl)
```

Legacy `setup.py` equivalents you'll still encounter:

```bash
python setup.py sdist              # source distribution
python setup.py bdist_wheel        # wheel
```

---

### Code Quality and Formatting

[`ruff`](https://github.com/astral-sh/ruff) is a fast, all-in-one linter and formatter that replaces flake8, isort, autoflake, and more:

```bash
pip install ruff
ruff check .                       # lint
ruff check --fix .                 # lint & autofix
ruff check --select F401 --fix .   # remove unused imports
ruff format .                      # format (Black-compatible)
```

Other staples: `black` (formatter), `isort` (import sorting), `mypy` / `pyright` (static type checking), `pre-commit` (run all of these on `git commit`). Fix indentation of legacy code with `reindent`:

```bash
pip install reindent
reindent -r .                      # normalize to 4-space indentation
```

Adopt type hints incrementally — they document intent and unlock static checking:

```python
def greet(name: str, times: int = 1) -> str:
    return " ".join([f"hi {name}"] * times)
```

---

### Big Data and Scaling Pointers

When data outgrows a single machine's memory or a single core, these libraries extend familiar APIs:

- **[Dask](https://docs.dask.org/)** — parallel/larger-than-memory NumPy, pandas, and task graphs.
- **[Modin](https://github.com/modin-project/modin)** — drop-in pandas replacement (`import modin.pandas as pd`) that parallelizes across cores.
- **[Vaex](https://github.com/vaexio/vaex)** — out-of-core DataFrames for billion-row tables.
- **[Ray](https://www.ray.io/)** — general distributed execution for Python.
- **[Polars](https://pola.rs/)** — fast, multi-threaded DataFrames (Arrow-based); excellent single-node performance.
- **[PyArrow](https://arrow.apache.org/docs/python/)** — the columnar memory format underpinning much of the above.

Rule of thumb: exhaust single-machine options (better algorithms, `polars`, chunked processing, `numpy` vectorization) before reaching for a distributed framework — distribution adds real operational complexity.

---

### Appendix: One-liners and Resources

#### Handy shell one-liners

```bash
# dump the environment, sorted
python3 -c 'import os;[print(f"{k}={v}") for k,v in sorted(os.environ.items())]'

# how many CPU cores can this process use?
python3 -c 'import os; print(len(os.sched_getaffinity(0)))'

# a random free TCP port
python3 -c 'import socket;s=socket.socket();s.bind(("",0));print(s.getsockname()[1])'

# pretty-print / validate a JSON file
python3 -m json.tool file.json

# start a static HTTP server in the current directory
python3 -m http.server 8000

# validate a .jsonl file line by line
python3 -c "import sys,json;[json.loads(l) for l in open(sys.argv[1])]" data.jsonl

# time and peak-memory of any command
/usr/bin/time -v python script.py
```

#### Recursion limits

For deep recursion, raise both the interpreter limit and the OS stack size:

```python
import sys, resource
sys.setrecursionlimit(100_000)
resource.setrlimit(resource.RLIMIT_STACK,
                   (0x4000000, resource.RLIM_INFINITY))
```

#### Tables for humans

```python
from tabulate import tabulate         # pip install tabulate
print(tabulate(rows, headers, tablefmt="github"))

import pandas as pd
print(pd.DataFrame(records).to_markdown(index=False))
```

#### Where to go next

- [The Python Tutorial](https://docs.python.org/3/tutorial/) and [Standard Library reference](https://docs.python.org/3/library/) — the canonical sources.
- [pyformat.info](https://pyformat.info/) — string formatting by example.
- [regex101.com](https://regex101.com/) — build and debug regexes interactively.
- [Real Python](https://realpython.com/) — high-quality tutorials.
- `python -m this` — the Zen of Python; a good compass when choosing between approaches.

---

*This book favors clarity and the standard library. When a third-party package is suggested, it's called out with `pip install`.*
