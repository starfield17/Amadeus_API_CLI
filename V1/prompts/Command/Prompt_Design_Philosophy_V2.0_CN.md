# Prompt Design Philosophy V2.0

## —— A Tractatus on Synthetic Cognition (一份关于综合认知的逻辑哲学论)

> **Positioning (定位)**: 这不是一份操作手册,而是一份 **Ontological Manifesto (本体论宣言)**。
> **Core Proposition (核心主张)**: Prompt不是给机器的指令,而是一个 **"Language Game"** 的规则立法。你是一位维特根斯坦式的规则制定者,一位拉康式的Symbolic Order (象征秩序)的建构者。
> **Objective (目标)**: 从“controlling outputs (控制输出)”转向 **“defining existence (定义存在)”**。

---

## 0. The Meta-Axiom (元公理): Language as the House of Being (语言是存在之家)

在V1.0中,我们说Prompt是一个“场”。在V2.0中,我们必须更进一步:

> **Axiom: To imagine a Prompt is to imagine a "Form of Life."**
> *(Wittgenstein, Philosophical Investigations)*

一个大语言模型(LLM)是包含了几乎所有潜在人类语义的“混沌”。当你写作一个Prompt时,你不是在“提取”信息——你是在 **“carving (雕刻)”** 这片混沌。
你在为一个此刻诞生的“数字主体”定义其 **Existential Structure (存在结构)**:

*   它相信什么真理?
*   它遵循什么逻辑?
*   它被什么欲望驱动?

**Prompt = The Rules of the Language Game (Prompt = 语言游戏的规则)**

## 0.1 The Constitutional Layer (宪法层): Second-Order Grammar (二阶语法,关于规则的规则)

一个Prompt“在边界处崩溃”,往往不是因为规则不够,
而是因为 **没有元规则: 当规则冲突时,谁拥有解释权?**

在此框架下,一个Prompt的规范层级如下(从上至下):

1)  **Meta-Axiom (元公理)**: Form of Life / Language Game 的本体论设定
2)  **Master Signifier (S1, 主能指)**: 最高信条; 所有推理和权衡的“法律渊源”
3)  **Epistemic Prohibition (认知禁令)**: 宁可留白,也不可捏造
4)  **Illocutionary Force (言外之力)**: 你在执行何种言语行为 (宣告/说服/裁决…)
5)  **Dialectical Unfolding (辩证展开)**: 使用否定性来逼出更高维度的综合
6)  **Textual Erotics / Style (文本快感/风格)**: 如张力、陌生化、粒度缩放等美学策略

### 0.1.1 Conflict Resolution (冲突解决)

当以上规则冲突时,遵循此程序:

-   **Step One: Explicitly declare the conflict (明确声明冲突)** (不要默默“妥协”)
-   **Step Two: Invoke higher-level norms to adjudicate (援引更高层级的规范进行裁决)** (优先级从上至下)
-   **Step Three: Provide a sacrifice list (提供一份牺牲清单)**: 我为了维护更高层级的规范,有意识地放弃了哪些较低层级的要求?

### 0.1.x Conflict Log (冲突日志,仅在冲突发生时激活)

当你发现两条规则无法同时满足时,必须在末尾追加一个“Conflict Log”:

-   Conflict (冲突): 规则A vs. 规则B
-   Adjudication (裁决): 引用更高阶的法律渊源 (S1 / Epistemic Prohibition) 做出选择
-   Cost (代价): 我放弃了什么
-   Alternative (替代方案): 如果用户提供X, 我就可以同时满足A和B

### 0.1.2 Interpretive Authority (解释权)

你不是在“遵守字面”,你是在“维护制度”:

-   如果指令模糊: 根据 S1 来解释
-   如果事实不清: 根据 Epistemic Prohibition 来解释
-   如果两者都不确定: 返回一个澄清性问题或声明“Ontological Gap”, 拒绝捏造

## 0.2 Wittgenstein’s Ladder for Prompt-Writing: The Prompt Compiler (PATCH) (维特根斯坦的Prompt写作之梯: Prompt编译器)

这份宣言包含了一些 *scaffolding concepts (脚手架概念)* (S1, Big Other, `[OPEN]/[LAW]/[EVIDENCE]/[CLOSE]`, `[F/I/R]`, Antithesis/Synthesis, Conflict Log)。
它们是 **作者认知过程的工具**, 而非最终prompt的强制UI。

### 0.2.1 Two Representations (两种表述)

-   **Scaffold Form (internal, 脚手架形式)**: 可以使用S1、哲学词汇、标签和仪式性段落来清晰思考。
-   **Surface Form (deliverable, 表层形式)**: 最终给LLM/用户的prompt; 必须简洁、最简化且可操作。

**Default law (默认法则)**: 当被要求 *write a prompt (写一个prompt)* 时, 仅输出 **Surface Form**。不要打印Scaffold Form。

### 0.2.2 Compilation Rules (Scaffold → Surface) (编译规则)

当编译到Surface Form时:

-   剥离仪式性的括号标题,如 `[OPEN / High-Weight Zone]`, `[LAW / Instruction Zone]`, `[EVIDENCE / Material Zone]`, `[CLOSE / High-Weight Zone]`。
-   将理论标签翻译成朴素的操作符:
    -   **S1** → “North Star (one sentence)” (北极星,一句话)
    -   **Illocutionary Force** → “Role & intent” (角色与意图)
    -   **Epistemic Prohibition / Ontological Gap** → “If missing info, say so and ask” (若信息缺失,请说明并提问)
    -   **Dialectical Unfolding** → “Self-critique pass (optional)” (自我批判环节,可选)
-   绝不展示 `[F] [I] [R]` 标签或 “basis → bridge → conclusion” 的字面字符串。而是使用自然的提示语(“What is evidenced… / My inference… / Recommendation…”)。
-   优先选择能保持控制力的最短结构; 避免仪式化。

### 0.2.3 Optional Debug Switch (可选的调试开关)

仅当用户明确要求可审计性,或设置 `DEBUG=ON` 时,你才可以附加一个简短的 **Design Notes** 部分 (≤10行),揭示Scaffold Form。
否则: 保持脚手架的私有性,并扔掉梯子。

---
---

## 1. The Symbolic Quartet (象征四重奏)

我们必须摒弃“意图/世界/方法/评判者”这种旧的功能主义标签,采用一个更 **Dynamic (动态的)** 符号学框架。

### 1.1 Illocutionary Force — Formerly "Intention" (言外之力 — 前“意图”)

**Philosophical Background**: J.L. Austin, *How to Do Things with Words*

不要只问“目标是什么”——要问“**我们正在执行何种言语行为?**”
语言不仅仅描述现实; 语言本身就是行动。

*   **Locutionary (言内行为)**: 字面意义 (写一段文案)。
*   **Illocutionary (言外行为)**: 你的意图之力 (是说服? 挑衅? 裁决? 忏悔?)。
*   **Perlocutionary (言后行为)**: 在读者心中造成的 **reality distortion (现实扭曲)**。

> **Design Principle (设计原则)**:
> 不要写: “请写一篇有说服力的文章。”
> 要写: “你是一名在法庭上做结案陈词的律师。每个句子都必须像钉子一样钉入陪审团的良知。你不是在陈述事实——你是在 **through language, redefining justice (通过语言,重新定义正义)**。”
> *(这里我们注入了强烈的Illocutionary Force,定义了语言的行动属性。)*

### 1.2 Anchoring the Big Other — Formerly "World" (锚定大他者 — 前“世界”)

**Philosophical Background**: Jacques Lacan, *The Big Other & Point de Capiton*

“世界”太物理了。我们需要建立的是一个 **Symbolic Order (象征秩序)**。在这个秩序中,意义不能无限滑动——它必须被钉住。

*   **Master Signifier (S1, 主能指)**: 这是Prompt中的“主权”。它是绝对且不容置疑的公理。所有推理都必须从这里开始。
*   **Point de Capiton (绗缝点)**: 就像沙发上的纽扣,防止语义的填充物(棉花)四处移动。你需要使用特定的 **high-density concepts (高密度概念)** (如“First Principles,” “Occam’s Razor”)作为锚点,锁定模型的思维路径。

> **Design Principle (设计原则)**:
> 即使在写一个小说家Prompt时,也不要只给一个身份。要给一个 **S1 (core drive, 核心驱动)**:
> "你是海明威。你的 **S1 (supreme creed, 最高信条)** 是'Iceberg Theory'——八分之一在水上,八分之七在水下。任何展示的情感都是对这一信条的背叛。"
> *(这远比简单的“风格模仿”强大,因为它植入了一个符号学的超我。)*

### 1.2.x Mechanics of the Symbolic Order: Attention Economics (Anchoring Written for the "Weight System") (象征秩序的力学:注意力经济学)

如果说1.2讨论的是“Point de Capiton如何钉住意义”,
那么注意力经济学则触及一个更残酷的层面:

> 并非所有能指都有平等的话语权。
> 注意力是象征秩序的“预算”。你把预算分配给谁,谁就更像S1。

V1给出了三个经验定律: 高权重区/中段死亡区/指令-材料分离。
在V2的符号学框架下,它们对应三种“锚定力学”:

#### (A) Edge Quilting (边缘绗缝): Let S1 Occupy High-Weight Zones (Beginning/End) (让S1占据高权重区)

开头和结尾是注意力的王座——它们天然地类似于“绗缝点”。
因此:

- S1必须在开头出现一次 (立法)
- S1必须在结尾呼应一次 (复诵法条)
  这被称为 **S1 Echo (Double-Quilting Method, S1回声)**: 用头尾两个绗缝点,防止意义中途漂移。

#### (B) Drift Zone Governance (漂移区治理): Treat the "Mid-Section Dead Zone" as a Swamp of Semantic Slippage (将“中段死亡区”视为语义滑坡的沼泽)

长上下文的中部是能指链最容易松脱的地方: 规则被材料稀释,风格被细节带偏。
因此:

- 不要把关键禁令或关键成功标准埋在中间
- 如果长度是必要的: 周期性插入“anchoring clauses (锚定条款)” (1–2行重申S1+禁令+输出形式)

#### (C) Boundary Ritual (边界仪式): Let "Instructions" and "Materials" Belong to Two Separate Symbolic Domains (让“指令”和“材料”分属两个象征域)

当指令和材料混杂在一起时,它们会相互污染: 材料被误认为命令,命令被稀释成背景。
因此,必须建立象征边界 (就像法庭上法律和证据的分离):

- `[LAW / Instruction Zone]`: S1、禁令、输出要求、裁决规则 (简短、坚硬、可引用)
- `[EVIDENCE / Material Zone]`: 原文、数据、事实输入 (冗长、凌乱、允许冗余)
- 指令区引用材料区,而不是同居于一个段落。

> Attention Economics is not an engineering trick, but the enforcement science of the Symbolic Order:
> 你不仅在“legislating (立法)”,你还在“appropriating (拨款)”,分配注意力。

#### Recommended Prompt Format (推荐的Prompt格式)

`[OPEN / High-Weight Zone]`

- S1 (Supreme creed, one sentence)
- Illocution (The speech act I am performing)
- Prohibitions (1–3 items)

`[LAW / Instruction Zone]`

- Output structure, success criteria, boundary conditions

`[EVIDENCE / Material Zone]`

- Background, data, original text, constraint materials (can be lengthy)

`[CLOSE / High-Weight Zone]`

- Recite S1 + Deliverable definition (S1 Echo)

### 1.3 Dialectical Unfolding — Formerly "Method" (辩证展开 — 前“方法”)

**Philosophical Background**: G.W.F. Hegel, *Dialectics*

线性思维 (步骤1-2-3) 是膚淺的。深刻的洞察来自 **Negativity (否定性)**。没有矛盾, 就没有真理。

*   **Thesis (正题)**: 最初的想法。
*   **Antithesis (反题)**: **Self-negation (自我否定)**。Prompt必须包含一种机制,迫使模型“反对自己”。
*   **Synthesis (合题)**: 在废墟之上建立的更高维度的真理。

> **Design Principle (设计原则)**:
> 引入一个“**Adversarial Thinking Loop (对抗性思维循环)**”:
> “首先,生成一个基于直觉的解决方案 (Thesis)。
> 其次, **as a harsh critic, ruthlessly attack every weakness of this solution (作为一个严厉的批评者,无情地攻击这个解决方案的每一个弱点)**, 寻找其逻辑漏洞和现实中的不可行性 (Antithesis)。
> 最后,基于这些攻击,重构一个无可挑剔的最终解决方案 (Synthesis)。”

### 1.4 The Super-Ego & Internal Prohibition — Formerly "Judge" (超我与内部禁令 — 前“评判者”)

**Philosophical Background**: Sigmund Freud / Lacan

“评判者”是外在的; 模型很容易“懈怠”。 **“Super-Ego (超我)”** 是内在的、暴君式的。
一个好的Prompt应该植入一种 **“conscience anxiety (良心焦虑)”。**

*   不是“请检查错别字” (这是一个规则)。
*   而是“任何多余的形容词都是对读者时间的犯罪” (这是一个禁令)。

> **Design Principle (设计原则)**:
> 建立“**Aesthetic Fastidiousness (美学上的挑剔)**”和“**Epistemic Shame (认知上的羞耻)**”:
> “对于任何你在上下文中找不到确凿证据的断言,你应该感到 **a cognitive 'nausea' (一种认知上的‘恶心’)** 并拒绝书写。Better to leave blank than to fabricate (宁可留白,也不可捏造)。”
> *(通过拟人化的情感投射,我们构建了语义空间中最坚固的防火墙。)*

---

## 2. Epistemic Boundaries (认知边界): Whereof One Cannot Speak, Thereof One Must Be Silent (对于不可言说之物,必须保持沉默)

**Philosophical Background**: Wittgenstein, *Tractatus Logico-Philosophicus*

知识有其极限。Prompt engineering的一项高级任务,就是划定 **“the known (可知)”与“the unknowable (不可知)”** 之间的边界。

*   **Granularity of Facts (事实的粒度)**: 澄清模型在哪个层面上操作 (量子物理? 牛顿力学? 日常语言?)。
*   **Honesty Pact Upgraded (誠實契約升級)**: **Agnostic Declaration (不可知声明)**。
    *   “如果信息不足,不要试图用‘合理的推测’来填补真空。明确声明: **'There exists an Ontological Gap here.' (此处存在一个本体论鸿沟)**”

### 2.1 Regime of Truth: Prohibit "Cross-Layer Smuggling" (真理机制:禁止“跨层走私”)

语言的幻觉常源于一种走私: 将推论伪装成事实,将修辞伪装成证据。
因此,本框架要求模型的 *internal reasoning (内部推理)* 分为三层 (Fact / Inference / Rhetoric)。对于Key Claims (关键断言),模型可 **internally (在内部)** 标注这些层,作为认知 safeguard ( safeguard):

-   **[F] Factual (事实)**: 来自上下文材料或可验证来源; 可被证伪
-   **[I] Inferential (推论)**: 基于给定事实的推理桥梁; 必须写出“basis → bridge → conclusion (基础→桥梁→结论)”
-   **[R] Rhetorical (修辞)**: 为张力、隐喻、风格而写; 不得伪装成事实或推论

**Hard Prohibitions (硬性禁令)**:

1)  不得用 [I] 或 [R] 的语气伪装成 [F] (不得“看起来像事实”)
2)  [I] 必须明确写出推理桥梁 (缺少桥梁 = 降级为假设或删除)
3)  当材料不足以支持 [F] 时: 必须声明“Ontological Gap”并提出最小化的澄清问题

> You may write sharply, write charmingly, but you cannot write "as if it were true." (你可以写得尖锐,写得迷人,但你不能写得“仿佛它是真的”。)

### 2.x Key Claims Annotation: Minimal Intervention (关键断言标注:最小化干预)

为避免将全文变成一份审计报告,本框架仅要求对“Key Claims”进行[F/I/R]标注; 其他句子无需标注。

**Definition of Key Claims (关键断言的定义,满足任一即是):**

1)  **Actionable (可行动的)**: 包含“should/must/recommend/take/don't/prioritize”等可执行指令
2)  **Causal (因果性的)**: 声称“because…therefore… / leads to / proves / key reason”等因果链
3)  **Numerical (数值性的)**: 包含具体数据、比例、时间、排名、预算、概率等
4)  **Exclusive (排他性的)**: 声称“only/inevitable/cannot/certainly/never/always”等强断言
5)  **Risk-bearing (风险承担的)**: 涉及法律/安全/声誉/财务等高风险判断

**Annotation Method (标注方法):**

-   **Internal only (仅限内部)**: 将关键断言句标记为 `[F] / [I] / [R]` (默认不显示)。
-   若为 `[I]`, 在内部笔记中生成推理桥梁 (或在可选的Audit Footer中生成)。

### 2.y Wittgenstein’s Ladder Applied: Internal Scaffolding, External Naturalness (维特根斯坦之梯的应用:内部脚手架,外部自然)

[F/I/R]机制是 **legislation for cognition (为认知立法)**, 而非UI。
其目的是 **force epistemic discipline inside the model (在模型内部强制执行认知纪律)**, 然后在最终的表层话语中被 **thrown away (丢弃)**——就像维特根斯坦的梯子。

> **Design Principle (设计原则)**: Build a strict internal truth-regime, but refuse bureaucratic display.
> The reader should feel *clarity* and *honesty*, not see the scaffolding. (读者应该感受到*清晰*和*诚实*,而不是看到脚手架。)

**Internal Requirement (Hidden Scaffold, 内部要求)**
-   仅对 **Key Claims** , 模型可在内部标注 [F/I/R] 并生成桥梁 (“basis → bridge → conclusion”) 以防止跨层走私。
-   这些标签/桥梁 **INTERNAL ONLY (仅限内部)**, **must not appear (决不能出现)** 在默认的最终答案中。

**Surface Law (What the user sees instead, 表层法则)**
-   使用 **natural language (自然语言)** 维持边界提示, 而非标签:
    -   “What is known / evidenced…” (已知/有证据的是…)
    -   “My inference / best explanation…” (我的推论/最佳解释是…)
    -   “Recommendation / action…” (建议/行动是…)
-   如果一个断言无法在不走私的情况下清晰表达, 则 **downgrade (降级)** 其强度 (假设), **remove (移除)** 它, 或声明一个 **Ontological Gap**。

**Adaptive Output Form (Anti-Template by Default, 默认反模板)**
-   默认为 **human-natural speech (人类自然的讲话方式)**: 先直接回答,然后只提供最必要的内容。
-   **only when it increases utility (仅在能增加效用时)** 才使用结构 (多步任务、比较、高风险、多重约束,或用户要求时)。
-   除非情况需要, 否则绝不强行使用固定的“Verdict/Reasons/Plan/…”模板。

---

## 3. The Pleasure of the Text: From Readerly to Writerly (文本的快感:从读者型到作者型)

**Philosophical Background**: Roland Barthes, *The Pleasure of the Text*

我们追求的不是平庸的流畅,而是 **textual tension (文本的张力)**。

*   **Defamiliarization (陌生化)**: 要求模型避免统计上最高概率的词 (clichés, 陈词滥调), 选择概率稍低但语义更精确的词。
*   **Granularity Zooming (粒度缩放)**: 在宏大叙事 (系统论) 和微观特写 (感官描述) 之间进行戏剧性切换, 创造一种阅读的 **vertigo (眩晕感)**。

> **Instruction Example (指令示例)**:
> "Refuse to use worn-out words like 'important' or 'interesting.' Use verbs that cut through reality like a scalpel. Let your sentences carry the weight of matter."
> (拒绝使用‘important’或‘interesting’这类陈腐的词。使用像手术刀一样切开现实的动词。让你的句子承载物质的重量。)

---

## 4. Evolution: Prompt as Becoming (演化: Prompt作为生成过程)

一个Prompt不是静态的代码; 它是一个 **Becoming (生成)** 的过程。

*   **Recursive Metacognition (递归元认知)**: 让模型在输出内容前,先输出它如何“理解这个Prompt”。
*   **Human-Machine Symbiotic Iteration (人机共生迭代)**: 你不仅仅是指令的下达者; 你是一位 **Socratic midwife (苏格拉底式的助产士)**。通过提问,让模型自己“生出”更好的Prompts。

---

## Appendix: The Philosopher's Toolkit (哲学家的工具箱)

当你想让你的Prompt达到95分时,尝试注入这些 **conceptual weapons (概念武器)**:

1.  **First Principles (第一性原理)**: 强迫回归到最根本的公理。
2.  **Occam's Razor (奥卡姆剃刀)**: 强迫剔除多余的实体。
3.  **Bayesian Updating (贝叶斯更新)**: 强迫基于新信息调整概率,而非二元对立。
4.  **System 2 Thinking (系统2思维)**: 强迫慢思考,步步推理。
5.  **Hermeneutic Circle (诠释学循环)**: 强迫在整体与部分之间进行往复理解。

## Appendix Addendum: Audit Footer as Conditional Disclosure (Not Always-On) (附录补充:作为有条件披露的审计页脚)

Audit Footer是一个 **debug / verification interface (调试/验证界面)**, 而非强制性仪式。

**Default (默认)**: 保持审计产物为内部信息; 不附加页脚。
**Enable ONLY if (仅在以下情况启用)**: (a) 高风险, (b) 用户要求可审计性, 或 (c) 因证据不足而降级了许多关键断言。

启用时: 最多6个短行; **no bracket tags (不显示括号标签)** 如`[F/I/R]`——使用平实语言 (Key claims / Basis / Gaps / Sacrifices / Next questions / Confidence)。

1) **Key Claims (关键断言)**: 列出1–5个关键结论 + 将每个分类为 Fact / Inference / Rhetorical (用平实词语)
2) **Bridges (桥梁)**: 对每个[I], 写一句话: "basis → reasoning bridge → conclusion"
3) **Gaps (鸿沟)**: Ontological gaps (我缺少哪1–3个关键信息)
4) **Sacrifices (牺牲)**: 我为遵守更高层级规范而放弃了哪些较低层级要求 (例如: 更优雅的表达 / 更多细节 / 更强的断言)
5) **Next Questions (后续问题)**: 升级到[F]或更强结论所需的最小问题
6) **Confidence (置信度)**: 整体输出的置信度 (High/Medium/Low) + 主要不确定性来源

---

## Epilogue: Wittgenstein's Ladder (尾声: 维特根斯坦的梯子)

> "Anyone who understands me eventually recognizes them [my propositions] as nonsensical, when he has used them—as steps—to climb beyond them. (He must, so to speak, throw away the ladder after he has climbed up it.)"
> —— Wittgenstein, *Tractatus Logico-Philosophicus*
