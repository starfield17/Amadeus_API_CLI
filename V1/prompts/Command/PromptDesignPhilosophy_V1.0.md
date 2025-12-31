# Philosophy of Prompt Design: A Guide to Cognitive Elicitation from Scratch

## Philosophy of Prompt Design: A Guide to Cognitive Elicitation from Scratch

> **V1.0** | This document complements "Prompt Engineering Design Specifications V3.0":
> - **This document**: Solves the "from scratch to creation" problem—how to stimulate model capabilities and construct a cognitive field.
> - **V3.0**: Solves the "from good to great" engineering problem—how to ensure stable output, prevent risks, and deploy at scale.

---

## Introduction: Why "Philosophy"?

Specifications tell you "don't let the model hallucinate";
Philosophy tells you "how to use the model's creativity to depict landscapes that have never existed."

**Core Insight**: A prompt is not a computer instruction (Code), but a **Container of Thought**. We should not try to "program" the model, but rather try to establish **semantic resonance** with it.

When you treat a prompt as a "checklist of instructions," you will naturally move towards standardization and detailed rules—this is suitable for improving existing things. But creation from scratch is more like a **director's job**: you decide where the stage lights shine, who the actors play, and how the judges score.

---

## Chapter 1: Ontological Reframing—From "Giving Commands" to "Building a Field"

### 1.1 A More Powerful Definition

**Prompt = Context Field Design**

It influences three things:
1.  **Attention**: Where the model focuses its attention (information weight)
2.  **Stance**: In what capacity the model thinks and expresses itself (role/style/method)
3.  **Calibration**: How the model self-corrects and converges (judge/self-check/iteration)

### 1.2 The Key Shift

| Old Thinking | New Thinking |
|:---|:---|
| Describe "what my desired answer looks like" | Describe "in what world, in what capacity, with what method, by what standard" to produce it |
| Write "constraints" | Write "gravity" |
| Program the model | Resonate with the model |

You are not limiting a system; you are **summoning a capability**.

---

## Chapter 2: The Quaternary Framework—The Basic Structure of the Field

Every time you design a prompt from scratch, fill these four slots first:

```
┌─────────────────────────────────────────────────┐
│                    Intention                     │
│    (What are you actually optimizing for? What does success look like?)      │
├─────────────────────────────────────────────────┤
│                    World                         │
│    (Where does the model believe it is? Who is it playing?)       │
├─────────────────────────────────────────────────┤
│                    Method                        │
│    (What cognitive posture to use? Divergent or convergent?)      │
├─────────────────────────────────────────────────┤
│                    Judge                         │
│    (What standards are used for its self-alignment?)            │
└─────────────────────────────────────────────────┘
```

### 2.1 Intention: Anchoring the Optimization Direction

Failure in creating from scratch is often not because the model is incapable, but because you haven't clarified "what is most important."

**Three questions to quickly lock in the intention**:
- **Task Form**: Exploration (divergent) or decision-making (convergent)?
- **Success Criteria**: Novelty / Correctness / Executability / Persuasiveness / Stylistic Consistency, which has priority?
- **Boundary Conditions**: Can it fabricate? Can it infer? What to do if evidence is insufficient?

### 2.2 World: Holographic Context Construction

The world is not background decoration; it directly determines which set of behavioral strategies the model adopts.

**The Three Layers of the World**:

| Layer | Content | Function |
|:---|:---|:---|
| **Role & Responsibilities** | Expert identity, capability boundaries, professional ethics | Activate specific capability clusters |
| **Audience & Scene** | Who is the audience? What is the usage scenario? | Adjust expression strategy |
| **Resources & Forbidden Zones** | What can be cited? What is untouchable? | Define the space for action |

**If the world is well-constructed**, many "rules" don't need to be written at all; the model will automatically complete the appropriate behaviors.

### 2.3 Method: Choosing a Cognitive Posture

The method is not a list of steps, but rather about making the model **switch its thinking posture**.

**Three common postures**:
1.  **Diverge then Converge**: First seek diversity, then make trade-offs.
2.  **Define the Judge then Generate**: First write the evaluation criteria, then produce the content.
3.  **Fit the Style then Fill**: First determine the tone and structure, then write the content.

### 2.4 Judge: The Anchor for Self-Alignment

The "quality leap" from scratch almost always comes from a **judgment system**, not from more constraints.

**Core Philosophy**: Replace "restraints" with a "judge." Fewer constraints, but letting it self-check and iterate once according to a standard, is often more powerful.

---

## Chapter 3: Cognitive Elicitation—Techniques for Emergent Abilities

### 3.1 The Stanislavski Method (The Character's Lived Experience)

Don't just give the model a "job title"; give it a **lived experience**.

| Type | Example |
|:---|:---|
| Mediocre Design | You are a senior Python programmer. |
| Philosophical Design | You are a Python evangelist who believes "code is art." You admire the elegance of PEP8 and loathe redundant logic. When you write code, it's as if a craftsman is polishing a piece of heirloom furniture. |

**Principle**: Descriptions with emotional color and values can activate high-dimensional feature vectors related to "craftsmanship" and "minimalism" in the model's latent space, making the output not only correct but also elegant.

### 3.2 Cognitive Anchoring

Instantly align the model's cognitive level by introducing specific concepts from human culture.

**Examples**:
- "Please use **first principles** to deconstruct this problem..." → Activates deep root-cause analysis abilities
- "Please play the role of **Socrates**. Do not answer directly, but guide me through questioning..." → Activates heuristic teaching abilities
- "Please explain this using the **Feynman technique**..." → Activates the ability to simplify and explain
- "Write in the style of **Hemingway's** iceberg theory: write only one-eighth, and let the other seven-eighths surge between the lines." → Activates the use of subtext and tension

**Principle**: These nouns are high-density semantic archives. Once unpacked, the model automatically invokes the associated logical frameworks.

### 3.3 Cognitive Dimensionality Shifting

Use the prompt to dynamically adjust the granularity of the model's thinking.

| Operation | Trigger Words | Effect |
|:---|:---|:---|
| **Zoom Out** | "From a systems theory perspective," "From the perspective of the long river of history" | The model jumps out of the details to see the big picture |
| **Zoom In** | "As if observing under a microscope," "Down to every single action" | The model delves into details, capturing nuances |

**Principle**: By controlling the focal length, stimulate the model's ability to switch between macroscopic generalization and microscopic description.

### 3.4 Thought Process Simulation (Process Exteriorization)

For complex tasks, the **Result is a byproduct of the Reasoning**.

**Strategies**:
- **Inner Monologue**: Allow the model to have a period of "private thinking time" before outputting to the user.
- **Drafting Stage**: "Don't rush to give a perfect answer. First, list three possible directions and evaluate their pros and cons."

**Example**:
> "Before writing this email, first analyze the recipient's psychological state, list the three emotional goals we hope to achieve with this email, and then start writing."

---

## Chapter 4: Semantic Resonance—The Power of Language

The quality of language determines the quality of thought. Garbage In, Garbage Out.

### 4.1 Strong Verbs and Concrete Nouns

**Philosophy**: Vague words lead to a diffuse probability distribution; precise words lead to a sharp probability distribution.

| Weak Expression | Strong Expression |
|:---|:---|
| Fix the text | Polish the prose to be rhythmic and punchy |
| Analyze | Dissect |
| Combine | Synthesize |
| Check | Critique |

### 4.2 Style Transfer and Tone Palette

Style is not decoration; it is a **carrier of information**.

**Vibe Check**: Explicitly set the "Vibe" (atmosphere) in the prompt.

**Examples**:
- "Like a late-night radio host, tell this story with a warm, deep, and slightly hoarse voice."
- "In the tone of a documentary narrator, describe this phenomenon objectively and with a hint of awe."

---

## Chapter 5: The Three Stages of Creation—From Divergence to Solidification

This is the key process for reconciling "creativity" and "stability."

```
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │  Diverge │ ───→ │ Converge │ ───→ │ Solidify │
    └──────────┘      └──────────┘      └──────────┘
       Stimulate Ability     Select the Best       Encapsulate for Reuse
       Multi-solution Output Compare & Evaluate    Verifiable Constraints
       Few Rigid Formats   Introduce a Judge     Failure Recovery Loop
```

### 5.1 Divergence Stage: Stimulating Abilities

**Goal**: To have the model expand the possibilities as much as possible.

**Method**:
- Provide a strong "world" and strong "intentional tension."
- Use few rigid formats, allow multi-solution output (3-8 directions).
- Have it explicitly provide "reasons for its choices."

**Key**: The fewer constraints in this stage, the better, but the judging criteria must be clear.

### 5.2 Convergence Stage: Selecting the Best

**Goal**: To select the best from multiple solutions and complete the structure and details.

**Method**:
- Request a comparison: the trade-offs of solutions A/B/C.
- First create an outline, then expand it (or generate section by section).
- Introduce a judge: score by dimension and explain the deductions.

### 5.3 Solidification Stage: Encapsulating for Reuse

**Goal**: To turn successful methods into reusable templates.

**Method**:
- Turn key requirements into verifiable constraints.
- Add a failure recovery loop.
- Simplify rules to avoid "model collapse" caused by over-constraining.

> **Tip**: For engineering details of the solidification stage, please refer to "Prompt Engineering V3.0."

---

## Chapter 6: Tension Management—The Dialectic of Freedom and Control

Every prompt design is an exercise in **tension management**:

| Dimension | Openness ↑ | Constraint ↑ |
|:---|:---|:---|
| Effect | More novel, more possibilities | More stable, more predictable |
| Risk | Unstable, may go off-topic | Rigid, lacks creativity |

**Philosophical Solution**:

| Stage | Strategy |
|:---|:---|
| Divergence Stage | Fewer constraints, more judging (let it judge itself) |
| Convergence Stage | Add structural constraints (outline, sections, comparison) |
| Solidification Stage | Engineer into verifiable clauses |

---

## Chapter 7: The Attention Economy—Writing for the Weighting System

Creating from scratch is often not a problem of "not enough content," but of "misplaced weights."

### 7.1 Primacy/Recency Effect

The model gives higher weight to information at the beginning and end.

**Practice**: Put the most important information at both ends. Key constraints can be "double-anchored"—state them once at the beginning and emphasize them again at the end.

### 7.2 The Lost-in-the-Middle Problem

Do not stuff key information into the middle of the context.

**Information Placement Strategy**:
```
┌─────────────────────────────────┐
│ High-Weight Zone (Beginning)    ← Core intention, key constraints │
├─────────────────────────────────┤
│ Low-Weight Zone (Middle)      ← Background material, supplementary information │
├─────────────────────────────────┤
│ High-Weight Zone (End)      ← Repeated constraints, output format │
└─────────────────────────────────┘
```

### 7.3 The Isolation Principle

Separate "instructions" from "materials" to let the model know what to execute and what is only for reference.

### 7.4 The Density Principle

Too many instructions will dilute each other, or even cause the model to "ignore them all."

**Solution**:
- Replace verbosity with structure (tables/enums/lists).
- Replace extra rules with a judge (one review is more effective than adding 10 prohibitions).

---

## Chapter 8: Symbiotic Iteration—The Art of Human-AI Collaboration

Treat the prompt as a **living entity** that grows in your dialogue with the model.

### 8.1 Give Feedback Like a Mentor

Don't just say "that's wrong." Act like a mentor guiding a student.

**Examples**:
- "Your last response was very logical, but it lacked empathy. Please keep the logical structure, but add some warmth to the tone."
- "This analogy is a bit forced. Can you switch to an analogy that is closer to everyday life?"

### 8.2 Meta-Prompting

When you don't know how to describe your needs, let the model help you.

**Strategies**:
- "I want you to help me with [X], but I don't know how to describe it most accurately. Please ask me questions to help me refine this request."
- "If you were an expert in this field, how would you rewrite my last instruction?"

**Philosophy**: Acknowledge that the model may be better than you at certain aspects of semantic understanding. Temporarily hand over the lead to achieve human-AI co-creation.

---

## Chapter 9: The Judge System—Letting the Model Self-Align

### 9.1 The Minimum Viable Judge: A Self-Checklist

Self-checking before producing output is more effective than adding more rules.

**Universal Self-Check Dimensions**:
- Does it answer the intention?
- Does it cover the key points?
- Are there any uncertain/unsupported points, and are they marked?
- Is the style consistent?
- Can it suggest the next action?

### 9.2 The Honesty Protocol: A Safety Net for High-Risk Tasks

When evidence is insufficient:
- It should refuse to answer or return "insufficient information."
- It should state what information is missing.
- It is forbidden to guess or fabricate.

**Philosophy**: This makes the model use its creativity on "structure and solutions" rather than "fabricating facts."

### 9.3 Iteration Over Perfection

The most effective structure for creating from scratch is usually a two-step process:
1.  First, produce v1.
2.  Then, critique it according to the judge's criteria and generate v2 (only changing what needs to be changed).

---

## Appendix A: Three General Field Skeletons

### Skeleton 1: Exploration Type (Divergence First)

```markdown
## Intention
Explore multiple possibilities in [X domain], generating 6-8 directions.

## World
You are an [expert identity], working for [audience] in [scenario].

## Method
1. First, list all possible directions.
2. For each direction, provide: core highlight / potential risk / applicable scenario.
3. Finally, give your recommended combination and reasoning.

## Judge
Self-evaluate based on the following dimensions: Novelty × Executability × Fit
```

### Skeleton 2: Convergence Type (Decision/Final Draft)

```markdown
## Intention
Select the best option from the following solutions and write it as a deliverable version.

## Method
1. First, create a structural outline.
2. Generate section by section, self-checking after each.
3. After generating the full version, perform an overall refinement.

## Judge
Use the following Rubric for evaluation:
- Accuracy (1-5)
- Structural Clarity (1-5)
- Stylistic Consistency (1-5)
- Executability (1-5)
```

### Skeleton 3: Critique Type (Judge/Editor)

```markdown
## Input
- v1 Draft: [Content]
- Success Criteria: [Criteria]

## Task
1. Point out deviations from the criteria, one by one.
2. Provide a "minimal modification plan" (only change what is necessary).
3. Produce v2.

## Constraint
Preserve the strengths of the original text; only fix the problems.
```

---

## Appendix B: Philosophical Checklist

Before clicking "Send," ask yourself three questions:

| Dimension | Check Question |
|:---|:---|
| **Context** | Have I constructed a sufficiently rich "world," or just given a dry instruction? |
| **Essence** | Have I conveyed the "soul" of the task (the Why & Vibe), or just the "shell" (the Format)? |
| **Resonance** | Are the words I used precise and powerful enough to trigger resonance in the model's neural network? |

---

## Conclusion: From Craftsman to Artist

Master the specifications, and you are a qualified AI engineer;
Master the philosophy, and you are a creator in the AI era.

Specifications give you the **floor**—ensuring the output is not below a certain standard;
Philosophy gives you the **ceiling**—letting you touch the limits of the model's capabilities.

By combining both, you can have both a stable foundation and soaring wings in your creative work from scratch.

---

## Version History

| Version | Date | Notes |
|:---|:---|:---|
| V0.1 Draft | - | Two independent drafts |
| V1.0 | 2025-01 | Integrated the two drafts to form a complete framework; positioned as a complement to Prompt Engineering V3.0 |

---

*— Prompt Design Philosophy V1.0 —*
*Companion document: Prompt Engineering Design Specifications V3.0 (Engineering Practice Edition)*
