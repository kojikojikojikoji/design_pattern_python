# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Interpreter pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s interpreter -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_parser_builds_one_node_per_grammar_rule` | The tree's structure mirrors the grammar — visible directly in its `repr`. |
| `test_missing_end_is_a_parse_error` | Grammar violations fail at **parse time**, before anything executes. |
| `test_unknown_command_is_a_parse_error` | Only the grammar's terminals are accepted; there is no "undefined behaviour" for typos. |
| `test_program_keyword_is_required` | Every sentence must derive from the start symbol `<program>`. |
| `test_repeat_executes_its_body_the_given_number_of_times` | A nonterminal node interprets itself by looping over its child expression. |
| `test_nested_repeats_multiply` | Recursion in the grammar becomes recursion in the tree — nesting costs zero extra code. |
| `test_language_is_decoupled_from_the_concrete_receiver` | A parsed tree drives *any* `CommandReceiver` — proven with a plain recording double. |
| `test_the_square_program_returns_the_robot_home` | End-to-end: text → tree → execution moves the real receiver exactly as the language promises. |

## A note for learners

The `RecordingReceiver` test double at the top of the test file is half the lesson: it implements `CommandReceiver` in nine lines and simply appends `"go"` / `"right"` / `"left"` to a list. That the *entire language* can be specified against it — no robot, no grid — is the decoupling the receiver interface buys. When you do the exercises (e.g. adding a `back` primitive), extend `RecordingReceiver` first and write the failing test before touching `nodes.py`.
