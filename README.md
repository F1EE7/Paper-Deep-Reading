# Paper Deep Reading

> **总结告诉你论文说了什么；三遍法教会你怎么读。**
>
> Summaries tell you what a paper says. Three passes teach you how to read it.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
![Platforms](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20ZCode%20%7C%20Codex%20%7C%20GPTs%20%7C%20Generic-lightgrey)

[English](./README.en.md) · [Demo](./demo/attention-is-all-you-need-demo.md) · [成品笔记示例](./examples/attention-is-all-you-need-notes.md) · [设计原则](./docs/design-principles.md)

---

## 一个精读教练，不是一个总结器

"帮我总结这篇论文"谁都会。但总结读完就忘，而且你依然不会读下一篇。本技能把**速览分流 → 诊断式精读 → 批判性审读**做成一个 Agent Skill，让模型先判断"值不值得读、你缺什么"，再决定讲什么：

```text
"帮我读这篇论文"
        │
        ▼
  第一遍·速览（5–10 分钟）──► 速览卡：问题/方法/证据/判断
        │                      停下：值得精读吗？❌ 到此为止 ✅ 继续
        ▼
  第二遍·精读 ──► 先诊断（为什么读/缺什么前置）──► 最小前置包 ──► 逐节讲义
        │                                                        │
        ▼                                                        ▼
  第三遍·硬核（按需）                              精读笔记（8 字段）
  逐符号推公式 / 批判清单审实验                     进度入记忆，跨会话续读
```

三个差异化行为：**先判断再投入**（速览是门禁）、**先诊断再讲解**（缺什么补什么，不整段重讲）、**诚实边界**（全文拿不到就明示，禁止编造）。

## 它能做什么

> 下列内容是仓库中编写的行为示例，用于展示 Skill 期望的交互形式；不是受控对照实验、实时模型生成记录或真实用户学习证据。

**先速览，判断值不值得读：**

```
【一句话】这篇论文用纯自注意力架构（Transformer）解决了
          RNN 无法并行、长距离依赖难传递的问题
【问题】seq2seq 翻译逐词递推，训练慢；依赖隔得远就丢
【方法】编码器-解码器各 6 层，全部依赖用 self-attention 表达，
        顺序信息用 position encoding 补上
【证据】WMT14 英德 28.4 BLEU，超此前最佳 2 BLEU 以上，
        训练成本不足此前 SOTA 的四分之一
【判断】✅ 值得精读——你做注意力机制的课程报告，这是必读的原始出处

要进入第二遍精读吗？还是只看某几节？
```

**"继续"能接上：** 长论文读到一半，进度、卡点、有效讲法都在记忆里，下次从断点继续，不重讲。

**公式讲透有"凭什么"纪律：** 每个等号一步都要说清凭什么成立——论文没写明的推导要声明"这是补全"，不冒充原文。

## 快速开始

1. 克隆本仓库：

   ```bash
   git clone https://github.com/F1EE7/Paper-Deep-Reading.git
   ```

2. 把 `skills/paper-deep-reading/` 复制到你的 agent 技能目录：

   | Agent | 目录 |
   |---|---|
   | ZCode | `~/.zcode/skills/`（Windows: `%USERPROFILE%\.zcode\skills`） |
   | Claude Code | `~/.claude/skills/` |

3. 触发：给一篇论文（PDF 路径 / arXiv 链接 / 粘贴文本），说"帮我读论文"。

需要一起加载的记忆样例说明见技能内 `memory/` 目录。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `skills/paper-deep-reading/SKILL.md` | 技能入口：模式路由、三遍概览、记忆规则 |
| `skills/paper-deep-reading/references/` | 三遍法细则 / 诊断与前置包 / 批判清单 / 笔记模板 |
| `skills/paper-deep-reading/memory/` | 记忆格式样例（半填状态） |
| `demo/` | 完整交互示例（精读 Attention Is All You Need） |
| `examples/` | 成品精读笔记示例 |
| `evals/` | E1–E8 行为案例 + 评分标准 + 失败记录 |
| `docs/` | 设计原则、测试指南、设计文档 |
| `scripts/check_skill.py` | 结构验证器（CI 门禁） |

## Evals

8 个行为案例（`evals/cases/E1–E8`）覆盖：速览先行、判断+理由、诊断先行、逐符号推导、记忆恢复、笔记导出、非论文路由、诚实降级。每个案例是"必须行为 + 禁止行为"双清单，禁止行为一票否决。执行方法见 [docs/testing-guide.md](./docs/testing-guide.md)，评分边界见 [evals/scoring_rubric.md](./evals/scoring_rubric.md)。

## 姊妹项目

[Scientific-learning-skills](https://github.com/F1EE7/Scientific-learning-skills)：一套"先诊断，再讲解"的学习技能（9 个子技能 + 间隔复习引擎）。那边管**学会知识**（概念、解题、错题、单词、背诵），这边管**读文献**。

## 许可

[MIT](./LICENSE)
