# Python Tutorial Hub

> Your one-stop personal reference: **basic → advanced Python**, packed with
> practical, copy-paste-ready snippets and short explanations. Build on it
> as you learn — every page assumes the previous ones.

---

## How to use this site

- **Read in order** — the Basics module builds from zero, so follow the sections top to bottom at least once.
- **Search** — use the search box (top right) to jump straight to the topic or snippet you need.
- **Cheatsheet** — once you know the basics, bookmark the [Quick Reference](001-cheatsheet.md) for fast lookup.
- **Copy code** — every code block has a copy button; grab snippets and paste them into your own scratch scripts to experiment.
- **Expand later** — this site is designed to keep growing. New pages or deeper sections can be added anytime.

## A practical learning loop

The numbered core lessons build concepts in sequence. The package lessons are
task-oriented: choose the category that matches your problem, read the
prerequisites, and treat external-service examples as templates rather than
drop-in production code. A code fence may be a complete script or a fragment;
when it depends on an earlier definition, the surrounding explanation names
that dependency.

Create a virtual environment before installing optional packages:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For a package not included in the base requirements, install it with
`python -m pip` inside the active environment. Pin versions for an application,
and check the package's current documentation when an API is version-sensitive.

Use this loop for each example: **understand** the inputs, outputs, state, and
failure mode; **run** the smallest local version; **modify** one thing and
predict the result; **harden** it with validation, timeouts, cleanup, and a
test; then **integrate** with external services or deployment systems.

---

## The Roadmap

The site is organized into three modules that build on each other:

=== "🐣 Basics"
!!! info ""
    **You are here if:** you're new to Python or want to firm up fundamentals.
!!!

**01** — [Getting Started](basics/002-getting-started.md) — install, run scripts, REPL, hello world.
**02** — [Variables & Types](basics/003-variables-types.md) — names, dynamic typing, core built-in types.
**03** — [Numbers & Strings](basics/004-numbers-strings.md) — arithmetic, f-strings, slicing, common methods.
**04** — [Collections](basics/005-collections.md) — lists, tuples, sets, dicts: when to use which.
**05** — [Control Flow](basics/006-control-flow.md) — if/elif/else, loops, break/continue/else.
**06** — [Functions](basics/007-functions.md) — def, parameters, scopes, returning values.
**07** — [Modules & Packages](basics/008-modules-packages.md) — import, standard library, structuring code.
**08** — [File Handling](basics/009-file-handling.md) — reading/writing files safely with context managers.
**09** — [Errors & Exceptions](basics/010-errors-exceptions.md) — try/except, raising, custom exceptions.
**10** — [Comprehensions](basics/011-comprehensions.md) — list/dict/set comprehensions, zip/enumerate.
===

=== "🚀 Intermediate"
!!! info ""
    **You are here if:** you can write small scripts and want to level up with more powerful idioms.
!!!

**11** — [OOP](intermediate/012-oop.md) — classes, inheritance, dunder methods.
**12** — [Decorators](intermediate/013-decorators.md) — functions wrapping functions, timers, caching.
**13** — [Generators](intermediate/014-generators.md) — lazy sequences, yield, memory-saving iteration.
**14** — [Context Managers](intermediate/015-context-managers.md) — with statements, writing your own.
**15** — [Lambda & Functional](intermediate/016-lambda-functional.md) — map/filter/reduce, itertools, operator module.
**16** — [JSON & CSV](intermediate/017-json-csv.md) — serialization, config files, data exchange.
**17** — [Regular Expressions](intermediate/018-regex.md) — pattern matching for text extraction/validation.
**18** — [VEnv & Packaging](intermediate/019-venv-packaging.md) — isolated environments, dependencies, distributing code.
===

=== "🧠 Advanced"
!!! info ""
    **You are here if:** you're working on real projects and need performance, reliability, concurrency.
!!!

**19** — [Asyncio](advanced/020-asyncio.md) — async/await, concurrent I/O with a single thread.
**20** — [Concurrency](advanced/021-concurrency.md) — threads vs processes, ThreadPoolExecutor, locks.
**21** — [Performance & Profiling](advanced/022-performance.md) — profiling, timing, smart optimizations.
**22** — [Testing](advanced/023-testing.md) — pytest, fixtures, mocking, TDD-style workflow.
**23** — [Type Hints](advanced/024-type-hints.md) — gradual typing, mypy-level confidence.
**24** — [Design Patterns](advanced/025-design-patterns.md) — battle-tested solutions to recurring problems.
**25** — [Best Practices](advanced/026-best-practices.md) — code style, Zen of Python, project hygiene.
===

---

## Suggested next stop

[Start at 01 — Getting Started →](basics/002-getting-started.md)

---

*New snippets and topics get added continuously. This is a living document.*
