# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Composite pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s composite -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_leaf_and_composite_share_the_component_interface` | A `File` and a `Directory` are both just `Entry` — the uniformity the pattern is named for. |
| `test_client_code_needs_no_isinstance_checks` | One function handles a lone file and a whole tree identically — the `isinstance` ladder from the naive design is gone. |
| `test_leaf_reports_its_own_size` | The leaf is the recursion's base case: it answers directly, no delegation. |
| `test_directory_size_aggregates_the_whole_subtree` | The composite implements the operation in terms of its children's same operation — recursive delegation is the engine of the pattern. |
| `test_empty_directory_has_size_zero` | The aggregation is total: the edge case of a childless composite is well-defined, not an error. |
| `test_add_returns_self_so_trees_build_fluently` | Child management supports declarative tree construction (`Directory("d").add(...)`). |
| `test_safe_design_leaves_have_no_child_management` | The *safe* variant's promise: `File.add` does not exist, so misuse is visible statically instead of exploding at runtime. |
| `test_cycles_are_rejected_so_the_tree_stays_a_tree` | The composite defends its shape invariant — no directory can end up inside its own subtree. |

## A note for learners

When you do the exercises (e.g. adding a `Symlink` leaf), write the tests *first* by copying this file and adjusting the expectations. The two tests that must keep passing untouched are `test_client_code_needs_no_isinstance_checks` and `test_directory_size_aggregates_the_whole_subtree` — if your new node type forces changes there, it has broken the uniform interface.
