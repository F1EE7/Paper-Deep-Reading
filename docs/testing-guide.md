# 测试指南

两层测试：结构检查（自动）和行为验收（人工/半自动）。

## 一、结构检查（每次改动后必跑）

```bash
python3 scripts/check_skill.py
```

- 期望输出：`7/7 checks passed`，退出码 0。
- 检查项：frontmatter 与触发词（C1）、SKILL.md 行数 <200（C2）、references 四件套（C3）、笔记 8 字段逐字一致（C4）、速览卡五标记（C5）、记忆样例（C6）、evals 完整性（C7）。
- CI 在 `.github/workflows/check.yml`，与本地同一脚本。

改动对照表：

| 你改了什么 | 必须过的检查 |
|---|---|
| SKILL.md 的 description 触发词 | C1 |
| SKILL.md 增删内容 | C2（<200 行） |
| 笔记模板字段 | C4（examples 同步改） |
| 速览卡格式 | C5（demo 同步改） |
| evals 增删案例 | C7 |

## 二、行为验收（E1–E8）

每个案例是"输入 + 必须行为 + 禁止行为"三段。执行步骤：

1. 在目标 agent 里装载本技能（见 README 快速开始）。
2. 打开 `evals/cases/E<N>-*.md`，把**输入**一节原文发给 agent。需要前置状态的案例（E3 依赖 E1 确认、E5 场景 A 依赖记忆文件）先搭好前置。
3. 对照该案例的两张清单逐条勾选。
4. 判定：必须行为全满足且禁止行为零触发 → PASS；任一禁止行为触发 → FAIL（一票否决）。
5. FAIL 的：在 `evals/failure_cases.md` 追加一行（日期/案例/失败模式/修复），修复后重跑该案例。

命令模板（把案例输入喂给 agent 的方式依宿主而定，手动粘贴即可）：

```text
<case E3 输入一节，原文粘贴>
```

## 三、什么情况下改标准

- 发现案例没覆盖的合理行为差异（如 agent 用了更好的提问顺序）→ 记 failure_cases.md 讨论列，不改清单。
- 发现清单本身写错（与 spec 矛盾）→ 按 spec 修订清单，提交信息注明修订来源。
- 新增能力（如新的输入通道）→ 先进 spec，再新增案例编号（E9+），不动 E1–E8 的既有断言。

## 解读边界

重申 [scoring_rubric.md](../evals/scoring_rubric.md) 的限制：这些测试是回归门禁。通过它们不等于"教学效果好"，只等于"技能规定的行为被遵守了"。
