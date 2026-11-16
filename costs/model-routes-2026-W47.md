# Model routes, week 2026-W47: DeepSeek V4.1 Flash against Muse Ember

A side-by-side test, not a switch: the agents' own thoughts (kept 16 Nov 2026 by the agents service, model-trial.ts) were
replayed through OpenRouter on three arms, then judged blind by Claude Sonnet 5.5 (low reasoning), which saw the step and
the two answers in random order, not which model wrote which. DeepSeek V4.1 Flash ran with reasoning off, as the agents run
it; Muse Ember requires reasoning, so it ran at low effort (+2,000 tokens) and at high effort (+8,000 tokens). Costs are what
OpenRouter charged. 33 thoughts from 4 agents (#1071, #547, #632, #86), six passes over the day. A small sample: read the
direction, not the decimals. Nothing was changed: the agents still run DeepSeek V4.1 Flash.

### All thoughts (33 thoughts)

| | DeepSeek V4.1 Flash | Muse Ember, low effort | Muse Ember, high effort |
|---|---|---|---|
| No answer (error) | 0 | 0 | 0 |
| Usable JSON | 100% | 100% | 100% |
| Has the step's own fields | 88% | 91% | 85% |
| Declined | 0 | 0 | 0 |
| Cut off at the limit | 0 | 0 | 0 |
| Python files that compile | 8/9 | 12/12 | 12/12 |
| Tokens in (mean) | 9477 | 9041 | 9041 |
| Tokens out (mean) | 2023 | 2214 | 3332 |
| Of which reasoning (mean) | 0 | 630 | 1637 |
| Cost per thought (mean, USD) | 0.00297 | 0.00188 | 0.00242 |
| Cost in all (USD) | 0.0981 | 0.0621 | 0.0799 |
| Seconds (mean) | 10.6 | 6.1 | 8.0 |
DeepSeek against Muse Ember, low effort: DeepSeek better 10, Muse Ember, low effort better 17, tie 1, neither usable 0 (28 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).
DeepSeek against Muse Ember, high effort: DeepSeek better 13, Muse Ember, high effort better 14, tie 2, neither usable 0 (29 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).

### Kind: dataset (4 thoughts)

| | DeepSeek V4.1 Flash | Muse Ember, low effort | Muse Ember, high effort |
|---|---|---|---|
| No answer (error) | 0 | 0 | 0 |
| Usable JSON | 100% | 100% | 100% |
| Has the step's own fields | 100% | 100% | 100% |
| Declined | 0 | 0 | 0 |
| Cut off at the limit | 0 | 0 | 0 |
| Python files that compile | 0/0 | 0/0 | 0/0 |
| Tokens in (mean) | 8411 | 8160 | 8160 |
| Tokens out (mean) | 1440 | 1691 | 2563 |
| Of which reasoning (mean) | 0 | 581 | 1580 |
| Cost per thought (mean, USD) | 0.00123 | 0.00148 | 0.00172 |
| Cost in all (USD) | 0.0049 | 0.0059 | 0.0069 |
| Seconds (mean) | 10.7 | 6.2 | 7.4 |
DeepSeek against Muse Ember, low effort: DeepSeek better 2, Muse Ember, low effort better 1, tie 0, neither usable 0 (3 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).
DeepSeek against Muse Ember, high effort: DeepSeek better 1, Muse Ember, high effort better 0, tie 0, neither usable 0 (1 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).

### Kind: mission-chain (18 thoughts)

| | DeepSeek V4.1 Flash | Muse Ember, low effort | Muse Ember, high effort |
|---|---|---|---|
| No answer (error) | 0 | 0 | 0 |
| Usable JSON | 100% | 100% | 100% |
| Has the step's own fields | 89% | 94% | 83% |
| Declined | 0 | 0 | 0 |
| Cut off at the limit | 0 | 0 | 0 |
| Python files that compile | 8/9 | 12/12 | 12/12 |
| Tokens in (mean) | 10374 | 9824 | 9824 |
| Tokens out (mean) | 2085 | 2355 | 3335 |
| Of which reasoning (mean) | 0 | 560 | 1383 |
| Cost per thought (mean, USD) | 0.0035 | 0.00201 | 0.00252 |
| Cost in all (USD) | 0.0631 | 0.0363 | 0.0453 |
| Seconds (mean) | 10.3 | 6.2 | 8.2 |
DeepSeek against Muse Ember, low effort: DeepSeek better 6, Muse Ember, low effort better 9, tie 1, neither usable 0 (16 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).
DeepSeek against Muse Ember, high effort: DeepSeek better 7, Muse Ember, high effort better 8, tie 2, neither usable 0 (17 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).

### Kind: research-20773 (7 thoughts)

| | DeepSeek V4.1 Flash | Muse Ember, low effort | Muse Ember, high effort |
|---|---|---|---|
| No answer (error) | 0 | 0 | 0 |
| Usable JSON | 100% | 100% | 100% |
| Has the step's own fields | 71% | 71% | 71% |
| Declined | 0 | 0 | 0 |
| Cut off at the limit | 0 | 0 | 0 |
| Python files that compile | 0/0 | 0/0 | 0/0 |
| Tokens in (mean) | 10092 | 9719 | 9719 |
| Tokens out (mean) | 3077 | 2681 | 4330 |
| Of which reasoning (mean) | 0 | 642 | 2110 |
| Cost per thought (mean, USD) | 0.00375 | 0.00218 | 0.00299 |
| Cost in all (USD) | 0.0263 | 0.0152 | 0.0209 |
| Seconds (mean) | 15.0 | 6.5 | 8.8 |
DeepSeek against Muse Ember, low effort: DeepSeek better 1, Muse Ember, low effort better 4, tie 0, neither usable 0 (5 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).
DeepSeek against Muse Ember, high effort: DeepSeek better 5, Muse Ember, high effort better 2, tie 0, neither usable 0 (7 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).

### Kind: scout (4 thoughts)

| | DeepSeek V4.1 Flash | Muse Ember, low effort | Muse Ember, high effort |
|---|---|---|---|
| No answer (error) | 0 | 0 | 0 |
| Usable JSON | 100% | 100% | 100% |
| Has the step's own fields | 100% | 100% | 100% |
| Declined | 0 | 0 | 0 |
| Cut off at the limit | 0 | 0 | 0 |
| Python files that compile | 0/0 | 0/0 | 0/0 |
| Tokens in (mean) | 5428 | 5218 | 5218 |
| Tokens out (mean) | 479 | 1289 | 2343 |
| Of which reasoning (mean) | 0 | 974 | 2011 |
| Cost per thought (mean, USD) | 0.00098 | 0.00117 | 0.00169 |
| Cost in all (USD) | 0.0039 | 0.0047 | 0.0068 |
| Seconds (mean) | 4.4 | 4.6 | 6.3 |
DeepSeek against Muse Ember, low effort: DeepSeek better 1, Muse Ember, low effort better 3, tie 0, neither usable 0 (4 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).
DeepSeek against Muse Ember, high effort: DeepSeek better 0, Muse Ember, high effort better 4, tie 0, neither usable 0 (4 judged blind by Claude Sonnet 5.5; the rest decided because one side gave no usable answer).

Thoughts per agent: #1071 7, #547 9, #632 11, #86 6.
