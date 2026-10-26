# 贡献指南

欢迎贡献。开工前先读 [docs/design-principles.md](./docs/design-principles.md)——本技能的每个结构决定都有理由，新内容要么服从这些原则，要么作为对原则的显式修订先改 [spec](./docs/specs/)。

## 环境与门禁

- 只需要 Python 3（标准库，无第三方依赖）。
- 每次改动后运行：

  ```bash
  python3 scripts/check_skill.py   # 期望 7/7 checks passed
  ```

- CI（`.github/workflows/check.yml`）跑同一个脚本，本地过了 CI 就过。

## 常见贡献类型

### 1. 加 eval 案例

1. 读 [docs/testing-guide.md](./docs/testing-guide.md) 的判定规则与解读边界。
2. 新案例编号顺延（E9、E10……），**不改 E1–E8 的既有断言**——发现它们写错了请开 issue 讨论。
3. 案例格式：输入（原文可粘贴）+ 必须行为 + 禁止行为；禁止行为要能一票否决。
4. 同步在 [evals/scoring_rubric.md](./evals/scoring_rubric.md) 的逐案例表加一行。
5. 跑 `scripts/check_skill.py`（C7 会校验案例数量与文件）。

### 2. 改笔记模板 / 速览卡格式

字段是跨文件契约：`note-template.md`、`examples/`、（速览卡）`demo/`、`scripts/check_skill.py` 的 `NOTE_FIELDS`/`OVERVIEW_MARKERS` 必须同步改，C4/C5 会拦住漏改。改字段名属于破坏性变更，请先开 issue。

### 3. 改技能行为（SKILL.md / references）

- SKILL.md 保持 <200 行（C2 拦截）；细则下沉 references。
- 新增触发场景时同步扩 description 的触发词（C1 校验既有 6 词仍在）。
- 新行为要有对应 eval 案例再合入。

### 4. 修文档 / demo

双语内容（README.md / README.en.md）信息等价——改一边请改另一边。

## 提交约定

约定式前缀：`feat:` / `docs:` / `chore:` / `fix:`。一个提交一个主题。

## 行为准则

批评行为，不批评人；引用论文内容时给出处；评测结论遵守 [scoring_rubric.md](./evals/scoring_rubric.md) 的解读限制，不得把 eval 通过表述为教学效果。
