---
name: python-cookbook
description: >-
  Practical, example-driven recipes for the Python standard library and everyday
  idioms - string/text wrangling, formatting, regex, numbers, the core data
  structures (list/tuple/set/dict) and comprehensions/itertools, functions,
  classes, dates/times, modules/imports, files/paths/IO, env vars and argparse,
  subprocess, serialization (JSON/CSV/pickle/XML/gzip), concurrency, networking,
  logging, debugging, introspection, CPU/memory profiling, exceptions, testing
  with pytest/unittest, virtualenvs, packaging, and code quality. Use when the
  user asks "how do I do X in Python?", needs a stdlib snippet or idiom, is
  formatting strings/numbers, writing a regex, transforming a dict/list, handling
  paths/files, parsing CLI args, running a subprocess, reading/writing
  JSON/CSV, adding logging, profiling slow code, tracking memory, writing tests,
  pinning dependencies, or packaging a project. Distilled from "Stas' Python
  Cookbook" open book, the latest version of which can be found at
  https://github.com/stas00/python-cookbook

  The latest SKILL.md version can be found at https://github.com/stas00/python-cookbook/blob/main/SKILL.md
---

# Stas' Python Cookbook

> Distilled from **Stas' Python Cookbook** open book by Stas Bekman - source: https://github.com/stas00/python-cookbook (CC BY-SA 4.0). This skill is a condensed index; each section links back to the full chapter for depth, runnable snippets, and gotchas.

A practical, standard-library-first reference for the Python idioms that come up again and again in real work. It leads with the *why*, shows the *how* with copy-paste snippets, and calls out the gotchas that bite in practice. Targets **Python 3.8+**; version-specific features are flagged inline. For deep single-process/tool debugging (gdb, strace, py-spy, core files, CUDA) pair this with [The Art of Debugging](https://github.com/stas00/the-art-of-debugging/blob/master/SKILL.md).

## Core principles

- **Reach for the standard library first.** A third-party package is only suggested when the stdlib genuinely falls short - and it's flagged with `pip install`.
- **Prefer the modern idiom.** f-strings over `%`/`.format()`, `pathlib` over `os.path`, `subprocess.run` over `os.system`, dataclasses over ad-hoc tuples, `logging` over `print` in real programs.
- **Know the gotcha before it bites.** Mutable default arguments, shallow vs deep copy, pass-by-object-reference, naive vs aware datetimes, the GIL - each chapter flags the trap.
- **Read the linked section before applying a recipe** - each has worked examples, caveats, and edge cases the one-liner here omits.

## Part I - Language core

Full chapters: [Strings](https://github.com/stas00/python-cookbook/blob/main/content/README.md#strings-and-text) · [Formatting](https://github.com/stas00/python-cookbook/blob/main/content/README.md#string-formatting) · [Numbers](https://github.com/stas00/python-cookbook/blob/main/content/README.md#numbers-and-math) · [Regex](https://github.com/stas00/python-cookbook/blob/main/content/README.md#regular-expressions).

- **Text wrangling:** case/containment/split/join/strip/replace, encoding-decoding, and a [worked text-normalization example](https://github.com/stas00/python-cookbook/blob/main/content/README.md#regular-expressions). Compare strings with a [readable diff](https://github.com/stas00/python-cookbook/blob/main/content/README.md#strings-and-text). See [Strings and Text](https://github.com/stas00/python-cookbook/blob/main/content/README.md#strings-and-text).
- **Formatting:** the [format spec mini-language](https://github.com/stas00/python-cookbook/blob/main/content/README.md#string-formatting) (alignment, padding, precision, `,`/`_` grouping), [f-string tricks](https://github.com/stas00/python-cookbook/blob/main/content/README.md#string-formatting) (`=` debug, nested specs), and number/byte humanization. See [String Formatting](https://github.com/stas00/python-cookbook/blob/main/content/README.md#string-formatting).
- **Numbers/math:** rounding traps, `decimal`/`fractions`, [statistics without NumPy](https://github.com/stas00/python-cookbook/blob/main/content/README.md#numbers-and-math), and special values (`nan`/`inf`). See [Numbers and Math](https://github.com/stas00/python-cookbook/blob/main/content/README.md#numbers-and-math).
- **Regex:** the [core functions](https://github.com/stas00/python-cookbook/blob/main/content/README.md#regular-expressions), flags, groups/assertions, substitution with backreferences/callables, splitting, and escaping literals. See [Regular Expressions](https://github.com/stas00/python-cookbook/blob/main/content/README.md#regular-expressions).

## Part I - Data structures

Full chapters: [Lists](https://github.com/stas00/python-cookbook/blob/main/content/README.md#lists) · [Tuples](https://github.com/stas00/python-cookbook/blob/main/content/README.md#tuples) · [Sets](https://github.com/stas00/python-cookbook/blob/main/content/README.md#sets) · [Dictionaries](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries) · [Comprehensions/itertools](https://github.com/stas00/python-cookbook/blob/main/content/README.md#comprehensions-iterators-and-itertools).

- **Lists:** add/remove, [shallow vs deep copy](https://github.com/stas00/python-cookbook/blob/main/content/README.md#lists) (a classic bug source), slicing/splicing, searching/aggregating, chunking, and ranges. See [Lists](https://github.com/stas00/python-cookbook/blob/main/content/README.md#lists).
- **Tuples & sets:** immutability and namedtuples ([Tuples](https://github.com/stas00/python-cookbook/blob/main/content/README.md#tuples)); set algebra and mutation ([Sets](https://github.com/stas00/python-cookbook/blob/main/content/README.md#sets)).
- **Dictionaries:** construction/merging (`|`), [access with defaults](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries), [`defaultdict`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries), [`Counter`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries), transformations, and [dataclasses for structured records](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries). See [Dictionaries](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries).
- **Comprehensions & iterators:** list/dict/set/generator forms, [the essential itertools](https://github.com/stas00/python-cookbook/blob/main/content/README.md#comprehensions-iterators-and-itertools), flatten/zip/unzip, and [generators with `yield`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#comprehensions-iterators-and-itertools) for streaming. See [Comprehensions, Iterators and itertools](https://github.com/stas00/python-cookbook/blob/main/content/README.md#comprehensions-iterators-and-itertools).

## Part I - Functions, classes, time

Full chapters: [Functions](https://github.com/stas00/python-cookbook/blob/main/content/README.md#functions) · [Classes](https://github.com/stas00/python-cookbook/blob/main/content/README.md#classes-and-objects) · [Dates](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dates-and-times).

- **Functions:** `*args`/`**kwargs`, the [mutable-default-argument trap](https://github.com/stas00/python-cookbook/blob/main/content/README.md#functions), [pass-by-object-reference](https://github.com/stas00/python-cookbook/blob/main/content/README.md#functions), closures, `functools` (partial/`lru_cache`/reduce), and [decorators](https://github.com/stas00/python-cookbook/blob/main/content/README.md#functions). See [Functions](https://github.com/stas00/python-cookbook/blob/main/content/README.md#functions).
- **Classes:** dunder methods, inheritance, dynamic attributes/delegation, [importing a class from a string](https://github.com/stas00/python-cookbook/blob/main/content/README.md#classes-and-objects), and [context managers](https://github.com/stas00/python-cookbook/blob/main/content/README.md#classes-and-objects). See [Classes and Objects](https://github.com/stas00/python-cookbook/blob/main/content/README.md#classes-and-objects).
- **Dates/times:** parsing/formatting, [always use timezone-aware datetimes](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dates-and-times), durations, and measuring elapsed time. See [Dates and Times](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dates-and-times).

## Part II - Runtime & environment

Full chapters: [Modules](https://github.com/stas00/python-cookbook/blob/main/content/README.md#modules-and-imports) · [Files/IO](https://github.com/stas00/python-cookbook/blob/main/content/README.md#files-paths-and-io) · [Env & args](https://github.com/stas00/python-cookbook/blob/main/content/README.md#environment-variables-and-program-arguments) · [Subprocess](https://github.com/stas00/python-cookbook/blob/main/content/README.md#subprocess-and-shell-integration).

- **Modules/imports:** how [`sys.path`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#modules-and-imports) resolves imports, inspecting/reloading modules, and dynamic import. See [Modules and Imports](https://github.com/stas00/python-cookbook/blob/main/content/README.md#modules-and-imports).
- **Files/paths/IO:** [`pathlib` basics](https://github.com/stas00/python-cookbook/blob/main/content/README.md#files-paths-and-io), metadata, create/move/delete, globbing, [reading/writing](https://github.com/stas00/python-cookbook/blob/main/content/README.md#files-paths-and-io), and [temp files/dirs](https://github.com/stas00/python-cookbook/blob/main/content/README.md#files-paths-and-io). See [Files, Paths and I/O](https://github.com/stas00/python-cookbook/blob/main/content/README.md#files-paths-and-io).
- **Env vars & CLI:** reading [environment variables](https://github.com/stas00/python-cookbook/blob/main/content/README.md#environment-variables-and-program-arguments) safely, [`argparse`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#environment-variables-and-program-arguments), and replaying the exact command line. See [Environment Variables and Program Arguments](https://github.com/stas00/python-cookbook/blob/main/content/README.md#environment-variables-and-program-arguments).
- **Subprocess:** run external commands with `subprocess.run` (capture output, check errors, avoid `shell=True` pitfalls) instead of `os.system`. See [Subprocess and Shell Integration](https://github.com/stas00/python-cookbook/blob/main/content/README.md#subprocess-and-shell-integration).

## Part II - Data, concurrency, network

Full chapters: [Serialization](https://github.com/stas00/python-cookbook/blob/main/content/README.md#serialization-json-csv-pickle-xml-gzip) · [Concurrency](https://github.com/stas00/python-cookbook/blob/main/content/README.md#concurrency-processes-threads-and-the-gil) · [Networking](https://github.com/stas00/python-cookbook/blob/main/content/README.md#networking).

- **Serialization:** [JSON](https://github.com/stas00/python-cookbook/blob/main/content/README.md#serialization-json-csv-pickle-xml-gzip) (custom encoders, streaming), CSV, pickle (and its security caveat), gzip, [memory-safe streaming XML](https://github.com/stas00/python-cookbook/blob/main/content/README.md#serialization-json-csv-pickle-xml-gzip), and archives. See [Serialization](https://github.com/stas00/python-cookbook/blob/main/content/README.md#serialization-json-csv-pickle-xml-gzip).
- **Concurrency:** the [GIL](https://github.com/stas00/python-cookbook/blob/main/content/README.md#concurrency-processes-threads-and-the-gil) and when to use processes vs threads, process pools, the unified [`concurrent.futures`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#concurrency-processes-threads-and-the-gil) API, and background monitoring threads. See [Concurrency](https://github.com/stas00/python-cookbook/blob/main/content/README.md#concurrency-processes-threads-and-the-gil).
- **Networking:** sockets/ports and [HTTP with `requests`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#networking). See [Networking](https://github.com/stas00/python-cookbook/blob/main/content/README.md#networking).

## Part III - Debugging, profiling & testing

Full chapters: [Logging](https://github.com/stas00/python-cookbook/blob/main/content/README.md#printing-logging-and-output-control) · [Debugging](https://github.com/stas00/python-cookbook/blob/main/content/README.md#debugging) · [Introspection](https://github.com/stas00/python-cookbook/blob/main/content/README.md#introspection-and-object-inspection) · [Profiling](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory) · [Exceptions](https://github.com/stas00/python-cookbook/blob/main/content/README.md#exceptions-and-error-handling) · [Testing](https://github.com/stas00/python-cookbook/blob/main/content/README.md#testing-with-pytest-and-unittest).

- **Output control:** print to stderr, [unbuffered output](https://github.com/stas00/python-cookbook/blob/main/content/README.md#printing-logging-and-output-control), tee to console+file, [`logging` over `print`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#printing-logging-and-output-control) for real programs, and `warnings`. See [Printing, Logging and Output Control](https://github.com/stas00/python-cookbook/blob/main/content/README.md#printing-logging-and-output-control).
- **Debugging:** the [interactive debugger](https://github.com/stas00/python-cookbook/blob/main/content/README.md#debugging) (`breakpoint()`/pdb), debugging forked/multiprocess code, [getting a traceback out of a stuck or crashed process](https://github.com/stas00/python-cookbook/blob/main/content/README.md#debugging), programmatic stack traces, and [tracing execution](https://github.com/stas00/python-cookbook/blob/main/content/README.md#debugging). See [Debugging](https://github.com/stas00/python-cookbook/blob/main/content/README.md#debugging).
- **Introspection:** [what is this thing?](https://github.com/stas00/python-cookbook/blob/main/content/README.md#introspection-and-object-inspection) (`type`/`dir`/`inspect`), dumping an object's attributes, and prettier dumps. See [Introspection and Object Inspection](https://github.com/stas00/python-cookbook/blob/main/content/README.md#introspection-and-object-inspection).
- **Profiling:** [`timeit`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory) for micro-benchmarks, [`cProfile`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory) for function-level CPU, `line_profiler` for per-line, [`tracemalloc`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory) for memory, `psutil` for process RSS, and leak-finding. See [Profiling CPU and Memory](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory).
- **Exceptions:** raising/catching precisely, [re-raising and chaining (`from`)](https://github.com/stas00/python-cookbook/blob/main/content/README.md#exceptions-and-error-handling), custom exceptions, and good habits (never bare-`except`). See [Exceptions and Error Handling](https://github.com/stas00/python-cookbook/blob/main/content/README.md#exceptions-and-error-handling).
- **Testing:** [pytest basics](https://github.com/stas00/python-cookbook/blob/main/content/README.md#testing-with-pytest-and-unittest), fixtures, capturing output, [parallel/slow-test control](https://github.com/stas00/python-cookbook/blob/main/content/README.md#testing-with-pytest-and-unittest), and `unittest`. See [Testing with pytest and unittest](https://github.com/stas00/python-cookbook/blob/main/content/README.md#testing-with-pytest-and-unittest).

## Part IV - Packaging & tooling

Full chapters: [Versions/Deps](https://github.com/stas00/python-cookbook/blob/main/content/README.md#versions-and-dependencies) · [Packaging](https://github.com/stas00/python-cookbook/blob/main/content/README.md#packaging-and-requirements) · [Code quality](https://github.com/stas00/python-cookbook/blob/main/content/README.md#code-quality-and-formatting) · [Big data](https://github.com/stas00/python-cookbook/blob/main/content/README.md#big-data-and-scaling-pointers) · [Appendix](https://github.com/stas00/python-cookbook/blob/main/content/README.md#appendix-one-liners-and-resources).

- **Versions/deps:** check the running Python version, query installed package versions, [compare versions correctly](https://github.com/stas00/python-cookbook/blob/main/content/README.md#versions-and-dependencies) (not string compare), and [virtual environments](https://github.com/stas00/python-cookbook/blob/main/content/README.md#versions-and-dependencies). See [Versions and Dependencies](https://github.com/stas00/python-cookbook/blob/main/content/README.md#versions-and-dependencies).
- **Packaging:** generate a requirements file from imports and [modern packaging with `pyproject.toml`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#packaging-and-requirements). See [Packaging and Requirements](https://github.com/stas00/python-cookbook/blob/main/content/README.md#packaging-and-requirements).
- **Code quality:** formatters/linters (black/ruff) and type checking. See [Code Quality and Formatting](https://github.com/stas00/python-cookbook/blob/main/content/README.md#code-quality-and-formatting).
- **Scaling pointers & one-liners:** when to reach past the stdlib ([Big Data](https://github.com/stas00/python-cookbook/blob/main/content/README.md#big-data-and-scaling-pointers)) plus handy shell one-liners, recursion limits, and human-readable tables ([Appendix](https://github.com/stas00/python-cookbook/blob/main/content/README.md#appendix-one-liners-and-resources)).

## Pick the recipe by need

| Need | Reach for |
|---|---|
| Format a number/string cleanly | [format spec mini-language](https://github.com/stas00/python-cookbook/blob/main/content/README.md#string-formatting), [f-string tricks](https://github.com/stas00/python-cookbook/blob/main/content/README.md#string-formatting) |
| Match/extract/replace text | [Regular Expressions](https://github.com/stas00/python-cookbook/blob/main/content/README.md#regular-expressions) |
| Count / group / default values | [`Counter`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries), [`defaultdict`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries) |
| Structured record type | [dataclasses](https://github.com/stas00/python-cookbook/blob/main/content/README.md#dictionaries) |
| Stream/lazily process data | [generators & itertools](https://github.com/stas00/python-cookbook/blob/main/content/README.md#comprehensions-iterators-and-itertools) |
| Work with files/paths | [`pathlib`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#files-paths-and-io) |
| Parse CLI arguments | [`argparse`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#environment-variables-and-program-arguments) |
| Run an external command | [`subprocess.run`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#subprocess-and-shell-integration) |
| Read/write JSON/CSV/gzip | [Serialization](https://github.com/stas00/python-cookbook/blob/main/content/README.md#serialization-json-csv-pickle-xml-gzip) |
| Parallelize work | [`concurrent.futures`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#concurrency-processes-threads-and-the-gil) (mind the [GIL](https://github.com/stas00/python-cookbook/blob/main/content/README.md#concurrency-processes-threads-and-the-gil)) |
| Real logging (not print) | [`logging`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#printing-logging-and-output-control) |
| Code is too slow | [`cProfile`/`timeit`/`line_profiler`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory) |
| Memory keeps growing | [`tracemalloc`/`psutil`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#profiling-cpu-and-memory) |
| A stuck/crashed process | [get a traceback out of it](https://github.com/stas00/python-cookbook/blob/main/content/README.md#debugging) |
| Write/run tests | [pytest & unittest](https://github.com/stas00/python-cookbook/blob/main/content/README.md#testing-with-pytest-and-unittest) |
| Compare version strings | [compare versions correctly](https://github.com/stas00/python-cookbook/blob/main/content/README.md#versions-and-dependencies) |
| Package/pin a project | [`pyproject.toml`](https://github.com/stas00/python-cookbook/blob/main/content/README.md#packaging-and-requirements), [requirements](https://github.com/stas00/python-cookbook/blob/main/content/README.md#packaging-and-requirements) |

## Notes for AI agents

- **Prefer the stdlib and the modern idiom** (f-strings, `pathlib`, `subprocess.run`, dataclasses, `logging`) unless the user's environment dictates otherwise; only add a dependency when the stdlib truly can't do it.
- **Watch the flagged gotchas** - mutable default args, shallow vs deep copy, pass-by-object-reference, naive datetimes, `shell=True`, bare `except`, string version comparison - before shipping a snippet.
- **Measure before optimizing:** profile with `cProfile`/`timeit`/`tracemalloc` rather than guessing which line is slow or leaky.
- **Read the linked chapter section** before applying an unfamiliar recipe - each has worked examples, caveats, and copy-paste code the index line omits.
- **Note the target version** (3.8+ baseline); guard newer-only features (`|` dict merge, `str.removeprefix`, `zoneinfo`, structural pattern matching) when portability matters.
- For deep runtime debugging of a crash/hang/segfault/OOM (gdb, strace, py-spy, core files, CUDA), use the companion skill: [The Art of Debugging](https://github.com/stas00/the-art-of-debugging/blob/master/SKILL.md).
