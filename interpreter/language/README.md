# `language/` — the abstract side of the pattern

This package **is the mini-language**. It plays the role a language designer plays in real life: it fixes the grammar, provides the parser, and defines what an executing program may ask its surroundings to do — without knowing anything about robots, turtles, or any other concrete receiver.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`context.py`](context.py) | **Context** | The token stream: a cursor plus `expect()` / `read_number()` helpers. |
| [`nodes.py`](nodes.py) | **AbstractExpression / Terminal- & NonterminalExpression** | One class per grammar rule; each parses itself and executes itself. |
| [`receiver.py`](receiver.py) | *(receiver interface)* | The three primitives a program can request: `go`, `turn_right`, `turn_left`. |
| [`errors.py`](errors.py) | *(error type)* | `ParseError` — raised on grammar violations, before anything runs. |

## The grammar is the table of contents

```text
<program>           ::= "program" <command list>            -> ProgramNode
<command list>      ::= <command>* "end"                    -> CommandListNode
<command>           ::= <repeat command> | <primitive command> -> CommandNode
<repeat command>    ::= "repeat" <number> <command list>    -> RepeatNode
<primitive command> ::= "go" | "right" | "left"             -> PrimitiveNode
```

Five rules, five classes — the mapping is the pattern. To change the language you change the BNF, and the BNF tells you which class to edit. Each class's `parse` classmethod is a near-literal transcription of its rule:

```python
@classmethod
def parse(cls, context: Context) -> "RepeatNode":
    context.expect("repeat")                            # "repeat"
    count = context.read_number()                       # <number>
    return cls(count, CommandListNode.parse(context))   # <command list>
```

Because `<repeat command>` contains `<command list>`, which contains `<command>`, which may again be a `<repeat command>`, the classes call each other recursively — a **recursive-descent parser** that falls out of the grammar for free, and with it, arbitrarily nested repeats.

## Parse first, run second

Every grammar violation raises `ParseError` while the tree is being built — a missing `end`, an unknown word, a `repeat` without a number. Execution starts only when a complete, valid tree exists. That ordering is a safety property: *a malformed program moves the robot zero steps*, rather than failing halfway through. The tests pin this down.

## The one rule of this package

> `language/` must **never** import from `robot/` (or any other concrete package).

The language talks to the world only through the small abstract [`CommandReceiver`](receiver.py) interface it defines itself. That is why the same parsed tree can drive the grid `Robot`, the test-suite's recording double, or your `AsciiCanvas` from the exercises — the dependency arrow points concrete → abstract, exactly as in the other patterns in this repository.
