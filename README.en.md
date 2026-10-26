# Paper Deep Reading

> **Summaries tell you what a paper says. Three passes teach you how to read it.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
![Platforms](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20ZCode%20%7C%20Codex%20%7C%20GPTs%20%7C%20Generic-lightgrey)

[中文文档](./README.md) · [Demo](./demo/attention-is-all-you-need-demo.md) · [Worked notes example](./examples/attention-is-all-you-need-notes.md) · [Design principles](./docs/design-principles.md)

---

## A reading coach, not a summarizer

"Summarize this paper" is a solved prompt. But a summary is forgotten by tomorrow, and you still can't read the next paper alone. This skill turns **triage → diagnostic close reading → critical review** into one Agent Skill: the agent first decides *whether the paper is worth reading and what you're missing*, then decides what to explain:

```text
"Help me read this paper"
        │
        ▼
  Pass 1 · Triage (5–10 min) ──► Overview card: problem / method / evidence / verdict
        │                          STOP: worth a close read?  ❌ stop ✅ continue
        ▼
  Pass 2 · Close reading ──► Diagnose first (goal / missing prerequisites)
        │                         ▼ minimal primer ──► section-by-section notes
        ▼
  Pass 3 · Hard mode (on demand)                    Reading notes (8 fixed fields)
  symbol-by-symbol derivations /                    progress saved to memory,
  critical checklist on experiments                 resume across sessions
```

Three differentiating behaviors: **triage before effort** (the overview card is a gate), **diagnose before teaching** (patch only what's missing, never re-lecture everything), **honest boundaries** (if the full text is unavailable, say so — never fabricate).

## What it does

> The interactions below are written behavior examples shipped in this repo to show the expected interaction shape; they are not controlled experiments, live model transcripts, or evidence of real learning outcomes.

**Triage first — is it worth reading?**

```
【一句话】This paper solves RNN's sequential bottleneck and vanishing
          long-range dependencies with a pure self-attention architecture
【问题】seq2seq decodes word by word — slow to train, drops distant context
【方法】6-layer encoder-decoder; all dependencies via self-attention;
        order injected through position encoding
【证据】28.4 BLEU on WMT14 En-De (2+ BLEU over best prior, incl. ensembles)
        at less than a quarter of the training cost of the previous state of the art
【判断】✅ Worth a close read — reading attention for a course report?
        This is the primary source

Enter pass 2, or jump to specific sections?
```

**"Continue" actually continues:** mid-paper progress, sticking points, and what explanations worked all live in memory — resume from the breakpoint, never re-teach confirmed sections.

**Every derivation step answers "says who":** each equality carries its justification; derivations the paper omits are explicitly labeled as completions, never passed off as the original text.

## Quick start

1. Clone the repo:

   ```bash
   git clone https://github.com/F1EE7/Paper-Deep-Reading.git
   ```

2. Copy `skills/paper-deep-reading/` into your agent's skills directory:

   | Agent | Directory |
   |---|---|
   | ZCode | `~/.zcode/skills/` |
   | Claude Code | `~/.claude/skills/` |

3. Trigger: hand it a paper (PDF path / arXiv link / pasted text) and say "help me read this paper".

The memory-format sample ships inside the skill's `memory/` directory.

## Repository layout

| Path | Contents |
|---|---|
| `skills/paper-deep-reading/SKILL.md` | Skill entry: mode routing, three-pass overview, memory rules |
| `skills/paper-deep-reading/references/` | Three-pass method / diagnosis & primers / critical checklist / note template |
| `skills/paper-deep-reading/memory/` | Memory-format sample (half-filled) |
| `demo/` | Full interaction transcript (Attention Is All You Need) |
| `examples/` | Finished reading-note example |
| `evals/` | Behavioral cases E1–E8 + scoring rubric + failure log |
| `docs/` | Design principles, testing guide, design docs |
| `scripts/check_skill.py` | Structure validator (CI gate) |

## Evals

8 behavioral cases (`evals/cases/E1–E8`) cover: triage-first, verdict+reason, diagnose-first, symbol-by-symbol derivation, memory resume, note export, non-paper routing, honest degradation. Each case is a must-behavior / forbidden-behavior checklist pair; any forbidden behavior is an instant fail. See [docs/testing-guide.md](./docs/testing-guide.md) for execution and [evals/scoring_rubric.md](./evals/scoring_rubric.md) for scoring boundaries.

## Sister project

[Scientific-learning-skills](https://github.com/F1EE7/Scientific-learning-skills): a "diagnose first, then explain" learning suite (9 sub-skills + spaced-repetition engine). That repo handles **learning knowledge** (concepts, problem solving, mistakes, vocabulary, memorization); this one handles **reading literature**.

## License

[MIT](./LICENSE)
