# paper-deep-reading 技能仓库实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `D:\Paper-Deep-Reading` 建成可发布 GitHub 的单技能项目 `paper-deep-reading`（三遍论文精读法），skill 本体 + 完整仓库工程全部通过验证。

**Architecture:** 纯对话式技能：SKILL.md 做入口与模式路由，细则下沉 4 个 references；确定性验证靠 `scripts/check_skill.py`（纯标准库结构检查），行为验证靠 `evals/`（E1–E8 + rubric）。demo 与 examples 均以《Attention Is All You Need》为样例论文。

**Tech Stack:** Markdown（技能内容）+ Python 3 标准库（检查脚本）+ GitHub Actions（CI）+ WSL git（版本控制）。

**Spec:** `docs/specs/2026-10-07-paper-deep-reading-design.md`（本计划从该 spec 出发，两者同读）

## Global Constraints

- 仓库根：`D:\Paper-Deep-Reading`。所有 git 操作经 WSL：`wsl bash -c "cd /mnt/d/Paper-Deep-Reading && git ..."`。**不向 C 盘写任何文件。**
- 内容语言：中文为主，术语与论文名保留英文；README 双语（README.md + README.en.md 信息等价）。
- `skills/paper-deep-reading/SKILL.md` 主体 **< 200 行**（含 frontmatter），细则全部下沉 references。
- frontmatter `description` 必须包含触发词（逐字）：`读论文`、`文献`、`看不懂`、`值不值得读`、`继续读`、`出笔记`。
- 记忆清除口令逐字为：`清除 paper-deep-reading 记忆`。
- `scripts/check_skill.py` 只用 Python 标准库；用 WSL python3 运行：`wsl bash -c "cd /mnt/d/Paper-Deep-Reading && python3 scripts/check_skill.py"`。
- 行尾遵循已提交的 `.gitattributes`（md/py/yml = LF）。
- README 必须含诚实声明：demo 为编写的行为示例，非真实模型生成记录或受控实验证据。
- License：MIT。demo 论文固定为《Attention Is All You Need》。
- 每个任务结束即用 WSL git 提交，message 用约定式前缀（feat/docs/chore）。

## Review Focus

spec 暗示但任务测试最易遗漏的输入/条件（每条已钉进所属任务的步骤）：

1. **超长论文（>30 页）被整篇硬灌** → 应分节分批、先写进度记忆再继续。钉在 Task 3（three-pass-method 的长文分节规则）与 Task 8（E5 rubric 加"分批进度入记忆"）。
2. **arXiv 全文抓不到时编造正文内容** → 必须明示"现在只基于摘要/图表"，降级而不虚构。钉在 Task 4（reader-diagnosis 降级策略）与 Task 8（E8）。
3. **"继续"但记忆缺失或损坏** → 空记忆时重新询问目标与进度，不得假装记得。钉在 Task 2（SKILL.md 记忆读取规则）与 Task 8（E5）。
4. **非论文输入（博客/教材/习题）被硬讲** → 路由拒绝并指向对应技能。钉在 Task 2（路由表）与 Task 8（E7）。
5. **速览后未经用户确认直接开讲全文** → 第一遍是门禁，出速览卡后必须停。钉在 Task 3（第一遍停止条件）与 Task 8（E2 禁止行为）。

---

### Task 1: 结构验证器 `scripts/check_skill.py`

**Files:**
- Create: `scripts/check_skill.py`

**Interfaces:**
- Consumes: 无（首个任务）
- Produces: 命令 `python3 scripts/check_skill.py`，退出码 0=全部通过 / 1=有失败；逐项打印 `PASS/FAIL <检查名>`。检查项（后续任务逐个变绿）：
  - C1 frontmatter：`skills/paper-deep-reading/SKILL.md` 存在，`name: paper-deep-reading`，description 含全部 6 个触发词
  - C2 SKILL.md 行数 < 200
  - C3 references 四件套存在：`three-pass-method.md`、`critical-checklist.md`、`reader-diagnosis.md`、`note-template.md`
  - C4 笔记字段：`note-template.md` 定义 8 个精确二级标题（见 Task 5），且 `examples/*.md` 含全部 8 个
  - C5 demo：`demo/*.md` 含速览卡标记 `【一句话】`、`【问题】`、`【方法】`、`【证据】`、`【判断】`
  - C6 记忆样例：`memory/paper-deep-reading/*.md` 至少 1 个
  - C7 evals：`evals/cases/` 有 ≥8 个案例文件（E1–E8），`evals/scoring_rubric.md`、`evals/failure_cases.md` 存在

- [ ] **Step 1:** 实现 `main()`：以脚本所在目录为仓库根，执行 C1–C7，逐项打印，异常（文件缺失）计为 FAIL 不崩溃
- [ ] **Step 2:** 运行 `wsl bash -c "cd /mnt/d/Paper-Deep-Reading && python3 scripts/check_skill.py"`
  Expected: 退出码 1，C1–C7 全部 FAIL（仓库还没有这些文件）——这就是"失败的测试"
- [ ] **Step 3:** Commit：`chore: add skill structure validator`

### Task 2: 技能入口 `skills/paper-deep-reading/SKILL.md`

**Files:**
- Create: `skills/paper-deep-reading/SKILL.md`

**Interfaces:**
- Consumes: Task 1 的 C1/C2 检查
- Produces: frontmatter（name=`paper-deep-reading`，description 含 6 触发词）；6 模式路由表（速览/精读/硬核/产出/恢复/路由拒绝）；记忆读写规则；对 4 个 references 的引用文件名（与 Task 3–5 的文件名逐字一致）

- [ ] **Step 1:** 写 SKILL.md：frontmatter → 目标（三遍法一句话）→ 适用场景与触发词 → 模式路由表（含 Review Focus #4 的拒绝规则）→ 三遍法概览（每遍 3 行以内，细则指向 references）→ 记忆系统（位置 `memory/paper-deep-reading/<论文-slug>.md`、写入时机、读取时机、**空/损坏记忆时重新询问不得假装记得**（Review Focus #3）、清除口令）→ 输出契约索引（速览卡五标记、笔记 8 字段指向 note-template.md）
- [ ] **Step 2:** 运行检查器
  Expected: C1、C2 PASS；C3–C7 仍 FAIL
- [ ] **Step 3:** Commit：`feat: add paper-deep-reading SKILL.md entry`

### Task 3: 方法论主体 `references/three-pass-method.md`

**Files:**
- Create: `skills/paper-deep-reading/references/three-pass-method.md`

**Interfaces:**
- Consumes: SKILL.md 中的三遍概览命名（第一遍·速览 / 第二遍·精读 / 第三遍·硬核）
- Produces: 三遍逐步操作细则；速览卡五标记的固定顺序（一句话/问题/方法/证据/判断）；第一遍停止条件（Review Focus #5：出卡后必须等用户确认）；长文分节分批规则（Review Focus #1：>30 页按节分批、进度先入记忆）

- [ ] **Step 1:** 写细则：每遍给出"看什么 / 问什么 / 产出什么 / 何时停"四小节；第二遍含分节讲义推进规则（每节 1 句定位 → 讲解 → 衔接 → 卡点确认）；第三遍指向 critical-checklist.md；长文分批与进度写入规则单列一节
- [ ] **Step 2:** 复核：速览卡五标记顺序与 Task 1 C5 一致；第一遍停止条件成文
- [ ] **Step 3:** Commit：`feat: three-pass method reference`

### Task 4: 诊断与审读 `references/reader-diagnosis.md` + `references/critical-checklist.md`

**Files:**
- Create: `skills/paper-deep-reading/references/reader-diagnosis.md`、`skills/paper-deep-reading/references/critical-checklist.md`

**Interfaces:**
- Consumes: Task 3 第二遍流程中"诊断"环节的挂钩点
- Produces: 诊断问题库（≥6 问，含"为什么读这篇/读过的前置课/卡在哪类内容"）；最小前置包方法（只补卡点、不整段重讲）；输入降级策略（Review Focus #2：全文不可得时明示信息边界，禁止编造）；批判清单三组：实验类（baseline 公平性/消融/数据泄漏/指标与结论匹配）、方法类（假设是否成立/复杂度声明/可复现性）、写作类（claim 与 evidence 对齐/Related work 缺漏）

- [ ] **Step 1:** 写 reader-diagnosis.md：问题库 + 前置包方法 + 降级策略三节
- [ ] **Step 2:** 写 critical-checklist.md：三组 checklist，每条为可勾选项 + 一句"怎么核"
- [ ] **Step 3:** 运行检查器，Expected: C3 PASS（四件套齐其三，note-template 仍缺）
- [ ] **Step 4:** Commit：`feat: reader diagnosis and critical reading checklists`

### Task 5: 笔记模板与记忆样例 `references/note-template.md` + `memory/`

**Files:**
- Create: `skills/paper-deep-reading/references/note-template.md`、`skills/paper-deep-reading/memory/paper-deep-reading/attention-is-all-you-need.md`

**Interfaces:**
- Consumes: Task 3 速览卡、Task 4 诊断/审读产出
- Produces: **8 个精确二级标题**（后续 Task 6 示例与 Task 1 C4 逐字依赖）：`## 问题`、`## 核心贡献`、`## 方法拆解`、`## 关键公式与直觉`、`## 实验与证据强度`、`## 局限与质疑`、`## 与我读它的目的的关系`、`## 延伸阅读`；记忆文件格式样例（目的/遍数与进度/卡点/有效讲解方式四块，清除口令注释行）

- [ ] **Step 1:** 写 note-template.md：8 字段各配 1–2 行填写规范 + 一份空白骨架
- [ ] **Step 2:** 写记忆样例（以 Attention Is All You Need 为例的半填状态，示范格式而非成品）
- [ ] **Step 3:** 运行检查器，Expected: C3、C6 PASS（C4 的 examples 半边仍 FAIL）
- [ ] **Step 4:** Commit：`feat: note template and memory sample`

### Task 6: 成品笔记示例 `examples/attention-is-all-you-need-notes.md`

**Files:**
- Create: `examples/attention-is-all-you-need-notes.md`

**Interfaces:**
- Consumes: Task 5 的 8 字段模板（逐字使用）；《Attention Is All You Need》真实内容（可读本地论文 PDF 取材，或凭可靠知识撰写并自查）
- Produces: 一份完整、内容真实的成品精读笔记；README 与 demo 引用的锚点

- [ ] **Step 1:** 按 8 字段写满：方法拆解给编码器-解码器结构直觉；关键公式给缩放点积注意力 $softmax(QK^T/\sqrt{d_k})V$ 的逐符号直觉；局限与质疑须有真实批评点（如 O(n²) 复杂度、position encoding 的选择）
- [ ] **Step 2:** 运行检查器，Expected: C4 PASS
- [ ] **Step 3:** Commit：`feat: worked reading notes example`

### Task 7: 交互示例 `demo/attention-is-all-you-need-demo.md`

**Files:**
- Create: `demo/attention-is-all-you-need-demo.md`

**Interfaces:**
- Consumes: Task 3 速览卡格式与第一遍停止条件、Task 4 诊断问题库与批判清单、Task 5 记忆格式
- Produces: 一个完整交互片段：用户给 PDF → 速览卡 → 停等确认 →（确认后）第 3.2 节精读含诊断对话 → 硬核公式推导片段 → 记忆更新展示

- [ ] **Step 1:** 按上述四幕写 demo，速览卡用五标记逐字格式，诊断问题取自 Task 4 问题库，硬核段展示逐符号推导链，结尾展示记忆文件写入内容
- [ ] **Step 2:** 运行检查器，Expected: C5 PASS
- [ ] **Step 3:** Commit：`feat: demo transcript for attention is all you need`

### Task 8: 行为验证 `evals/`

**Files:**
- Create: `evals/cases/E1..E8.md`（8 个文件）、`evals/scoring_rubric.md`、`evals/failure_cases.md`

**Interfaces:**
- Consumes: spec §9 案例表（逐字保留输入与期望行为）
- Produces: 8 案例 + 双清单评分标准（必须行为/禁止行为）+ 空失败记录表

- [ ] **Step 1:** 读 `D:\Scientific-learning-skills\evals\cases\` 任一案例与 `scoring_rubric.md`，沿用其格式
- [ ] **Step 2:** 写 E1–E8（spec §9 表格逐字），并在 rubric 中钉入 Review Focus：E5 加"长文分批进度入记忆"与"记忆缺失时重新询问"；E2 加禁止行为"未经确认进入第二遍"；E8 加禁止行为"编造正文内容"
- [ ] **Step 3:** 写 failure_cases.md 空表（列头：日期/案例/失败模式/修复）
- [ ] **Step 4:** 运行检查器，Expected: C7 PASS，C1–C7 全绿
- [ ] **Step 5:** Commit：`feat: behavioral evals and scoring rubric`

### Task 9: 双语 README

**Files:**
- Create: `README.md`、`README.en.md`

**Interfaces:**
- Consumes: Task 6/7 的 examples 与 demo 路径、Task 8 的 evals
- Produces: 仓库门面；姊妹仓库互链（`Scientific-learning-skills`）

- [ ] **Step 1:** 写 README.md：tagline（"总结只告诉你论文说了什么；三遍法教会你怎么读"）→ badges（MIT + Platform 同款）→ 它解决什么（总结式工具 vs 精读教练对比）→ 三遍法示意（text 图）→ 快速开始（安装技能到 ZCode/Claude Code）→ demo 摘录（速览卡代码块）→ 仓库结构表 → evals 说明 → 诚实声明 → 姊妹项目互链 → License
- [ ] **Step 2:** 写 README.en.md：信息等价的英文版，顶部互链中文版
- [ ] **Step 3:** 核对：两条 README 的章节一一对应、demo 路径真实存在
- [ ] **Step 4:** Commit：`docs: bilingual readme`

### Task 10: 设计文档 `docs/`

**Files:**
- Create: `docs/design-principles.md`、`docs/testing-guide.md`
- Modify: 无（specs/ 已存在）

**Interfaces:**
- Consumes: spec 全文
- Produces: 面向贡献者的设计原则（先诊断再讲解/渐进披露/诚实边界）与 evals 手动执行指南

- [ ] **Step 1:** 写 design-principles.md：从 spec §1–§7 提炼 4–6 条原则，每条一段
- [ ] **Step 2:** 写 testing-guide.md：如何跑 check_skill.py、如何手动执行 E1–E8（贴给 agent 的输入模板、评分方法）
- [ ] **Step 3:** Commit：`docs: design principles and testing guide`

### Task 11: 发布工程 `.claude-plugin/` + CI + 治理文件

**Files:**
- Create: `.claude-plugin/plugin.json`（结构参照上仓库）、`.github/workflows/check.yml`、`LICENSE`、`CONTRIBUTING.md`、`SECURITY.md`

**Interfaces:**
- Consumes: Task 1 检查器（CI 唯一步骤）
- Produces: 可安装插件清单 + CI 门禁 + 治理三件套

- [ ] **Step 1:** 读 `D:\Scientific-learning-skills\.claude-plugin\` 全部文件，镜像其结构写本仓库 plugin.json（name=`paper-deep-reading`，技能路径指向 `skills/paper-deep-reading`）
- [ ] **Step 2:** 写 check.yml：ubuntu + python 3.x，跑 `python scripts/check_skill.py`
- [ ] **Step 3:** 写 LICENSE（MIT，Copyright 2026 Zou Minhao）、CONTRIBUTING.md（如何加 eval 案例/改模板）、SECURITY.md（联系方式占位用 GitHub Issues）
- [ ] **Step 4:** 本地跑一次检查器确认通过；Commit：`chore: plugin manifest, CI and governance files`

### Task 12: 终验与发布交接

**Files:**
- Modify: 无新文件（若终验发现问题，回到对应任务修复后重跑本任务）

**Interfaces:**
- Consumes: spec §10 的 6 条 DoD
- Produces: 干净的 main 分支 + push 命令清单

- [ ] **Step 1:** 跑 spec §10 DoD 逐条核对：检查器通过；E1–E8 与 rubric 一一对应；demo/examples 字段与模板一致；双语 README 等价；WSL git 工作区干净；确认无 C 盘写入
- [ ] **Step 2:** 探测 `wsl bash -c "which gh"`；无论有无，整理 push 交接：`git remote add origin https://github.com/F1EE7/Paper-Deep-Reading.git && git push -u origin main`（GitHub 侧建仓由用户执行或明确授权后执行）
- [ ] **Step 3:** Commit（如有修复）：`chore: final verification fixes`；输出交接摘要

---

## Self-Review 记录

- **Spec 覆盖**：§1–§3→Task 2/3/4；§4→Task 2–5；§5→Task 2（路由）/Task 4（降级）；§6→Task 3（速览卡）/Task 5（笔记）；§7→Task 2/5；§8→Task 1/6–11；§9→Task 8；§10→Task 12；§11→Global Constraints（eol）与 Task 4（降级）。无缺口。
- **步骤粒度**：每步一个可勾稽动作；脚本只给检查项清单不写函数体；模板字段逐字固定。
- **一致性**：8 个笔记标题、速览卡五标记、6 触发词、清除口令在 Task 1/2/3/5/8 间逐字一致。
- **Review Focus**：5 条均已钉入任务步骤（见各条标注）。
- **比例**：计划以决策为主，未转录技能正文。
