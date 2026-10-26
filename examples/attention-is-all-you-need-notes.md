# 精读笔记：Attention Is All You Need（Vaswani et al., NeurIPS 2017）

> 读它的目的：（诊断时记录）为课程报告找"注意力机制"的原始出处；弄清 position encoding 为什么用正弦函数。

## 问题

2017 年时序列转换（翻译）的主流是 RNN/LSTM 编码器-解码器，配合 Bahdanau 式注意力。两个结构性缺陷：一是**顺序计算**——第 t 步必须等第 t−1 步算完，训练无法在时间维度并行；二是**长距离依赖**——信息要在隐状态里"传递"很多步，路径越长越容易丢。

## 核心贡献

1. **Transformer**：完全去掉循环和卷积，仅靠 self-attention 建模序列内依赖，位置信息由 position encoding 显式注入。
2. **多头注意力**：把 attention 拆成 8 个并行的"子空间视角"，每个头 64 维，各自关注不同关系模式后拼接。
3. **效果与成本同时改善**：WMT14 英德 28.4 BLEU（超当时最佳集成 2 BLEU 以上），英法 41.8 BLEU 单模型 SOTA，且训练成本不足此前 SOTA 的四分之一（论文结论原文口径）。

论文声称的贡献和实际贡献基本一致——第 3 条是硬结果，第 1、2 条支撑了此后几乎所有大模型架构。

## 方法拆解

1. **编码器-解码器各 6 层**：每层 = 注意力子层 + 逐位置前馈子层，各配残差连接 + LayerNorm。
2. **Self-attention**：序列自己对自己做注意力——每个词拿全句做"加权查询"，一步就把任意两词连起来（对比 RNN 的 O(距离) 步）。编码器内是双向的；解码器的自注意力带因果掩码（只看左侧），另有跨编码器的 cross-attention。
3. **多头**：d_model=512 拆成 h=8 个头，每头 d_k=d_v=64。直觉：一个头只能表达一种"关系分布"，多头允许同时attend语法头、指代头、语义头。
4. **Position encoding**：无循环则无顺序概念，把位置编码成同维向量与词向量相加。
5. **训练细节**：Adam + warmup 线性升再按步数平方根衰减（warmup=4000 步）；label smoothing 0.1——作者自己注明会伤 perplexity 但提 BLEU。

## 关键公式与直觉

缩放点积注意力：

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

逐符号：

- **Q（query）、K（key）、V（value）**：同一句子的线性投影。直觉用检索系统：query 是搜索词，key 是候选网页的摘要，value 是网页内容——匹配度（点积）决定取多少内容。
- **$QK^\top$**：所有 query-key 两两点积一次算完，这就是并行性的来源（对比 RNN 逐步递推）。
- **除以 $\sqrt{d_k}$（凭什么）**：$d_k$ 维独立同分布分量做点积，方差随 $d_k$ 增长；不除的话点积幅值大，softmax 落入饱和区、梯度趋近 0。缩放让 softmax 保持"软"。
- **softmax 后乘 V**：注意力权重是"取多少"，V 才是被取的内容。

## 实验与证据强度

- WMT14 英德 28.4 BLEU（big model），超过此前最佳（含集成）2.0 BLEU；英法 41.8 BLEU。训练成本表（Table 2）显示其成本不足此前 SOTA 的四分之一。
- 附加实验：句长分桶分析（长句不劣化）、constituency parsing 泛化（少量调参即有竞争力）。
- **证据强度：撑得住**——主结果用同任务同评测，对比对象是当时最强系统；但要打折处见下（单种子、成本口径）。

## 局限与质疑

- **O(n²) 复杂度（重要）**：自注意力对序列长度平方增长，长文档/高分辨率场景直接受限。作者在第 4 节 Table 1 的讨论里自己承认（把 self-attention 限制在大小 r 的邻域内是未来方向："We plan to investigate this approach further in future work"）——后来的 sparse/linear attention、FlashAttention 整条线都是对它的回应。
- **单种子 BLEU（疑问）**：主表数字未见多 seed 方差；BLEU 对翻译质量的覆盖本身有限（后续工作普遍报告多 checkpoint 平均）。
- **位置编码的选择（疑问）**：正弦 vs 可学习编码在该论文设定下效果相当（Table 3 (E)），正弦的"可外推到更长序列"优势当时并未验证——这恰是本笔记读它的目的之一，课程报告中应如实说明。
- **label smoothing 的代价（作者已承认）**：提 BLEU 但伤 perplexity，说明指标间存在权衡。

## 与我读它的目的的关系

两个目的都达成：① 课程报告的"原始出处"链条已闭合——Bahdanau(2014) 给注意力，本篇把注意力推到唯一机制并证明够用；② 正弦编码的疑问点已定位（等价性实验在 Table 3(E)，外推性当时未测），报告里可作为批判点写。报告结构建议：动机（顺序计算瓶颈）→ 机制（self-attention 公式逐符号）→ 影响（后续架构谱系）。

## 延伸阅读

- **Bahdanau et al. 2014**（Neural Machine Translation by Jointly Learning to Align and Translate）：注意力的前身，读它能补"为什么要 attention"的动机链。
- **Vaswani et al. 的后续对比**：BERT（只留编码器，双向）/ GPT（只留解码器，因果）——读它们能补"Transformer 各部件分别贡献了什么"。
- **FlashAttention (Dao et al. 2022)**：读它能补 O(n²) 限制在工程上如何被绕开（IO 感知精确注意力）。
