# The Philosophy of Prompt Design: A Guide to Cognitive Elicitation V1.0

> **Version Positioning**: This guide is applicable to the **"0 to 1"** phase of Prompt development.
> **Core Task**: To stimulate the model's potential, explore optimal solutions, and establish a path of thinking.
> **Follow-up Document**: Once the Prompt structure is stable, please refer to "Prompt Engineering Design Specifications V3.0" for engineering and solidification.

---

## 0. Ontology: What is a Prompt?

In design philosophy, a Prompt is not a piece of instruction (Code) sent to a computer, but a **Cognitive Field**.

We are not "programming" the model, but **"sculpting" probabilities**.

*   **Engineering Perspective**: A Prompt is a constraint. Without constraints, the model will make mistakes.
*   **Philosophical Perspective**: A Prompt is gravity. By constructing a specific semantic field, it causes the model's high-dimensional vectors to naturally collapse into the desired region.

**The essence of design is to manage the resonance between "attention" and "intention."**

---

## I. Core Framework: The Quadruple (The I.W.M.J. Model)

When facing a blank editor, don't rush to write the `<system>` tag. First, construct these four dimensions in your mind. This is the skeleton that brings the model to "life".

### 1. Intention: What is this conversation for?

Not just "output format," but "cognitive goal."

*   **Exploration**: Requires divergent thinking, multiple perspectives, and even unexpected surprises. (*Keywords: brainstorm, connect, possibilities*)
*   **Decision-making**: Requires convergence, trade-offs, and logical closure. (*Keywords: critique, rank, Occam's razor*)
*   **Creation**: Requires immersion, stylization, and emotional resonance. (*Keywords: flow, sensory, empathy*)

### 2. World: Holographic Context Construction

The model needs to "believe" where it is to activate its corresponding potential. Don't just give it a job title; give it a **life experience** (The Stanislavski System).

*   **From Job Title to Belief**:
    *   *Weak Setting*: "You are a senior programmer."
    *   *Strong Setting*: "You are a code minimalist who believes 'code is art.' You have a visceral aversion to redundant logic and pursue the aesthetic of logic as refined as a haiku."
*   **Holographic Projection**:
    *   **Who is the audience?** (Explaining to a 5-year-old vs. reporting to a 50-year-old academician)
    *   **Resources and Forbidden Zones**: Is this a utopia with infinite resources, or a realistic battlefield full of constraints?

### 3. Method: Thought Path Simulation

Don't just focus on the Result; design the scaffolding for Reasoning. Guide the model to simulate advanced human thought patterns.

*   **Cognitive Anchoring**: Use highly compressed concepts from human culture to instantly align cognition.
    *   *Example*: "Deconstruct... using **first principles**." (Activates the ability to trace back to the source)
    *   *Example*: "Explain it like **Feynman**..." (Activates the ability to simplify complex topics)
*   **Thought Exteriorization**:
    *   **Inner Monologue**: Require the model to conduct a period of "private thought" before answering.
    *   **Dimensionality Shifting**: Require the model to "first look from the macro perspective of history, then observe the micro details like a microscope."

### 4. Judge: Self-Correction Mechanism

In the "0 to 1" phase, the fewer constraints the better, but the **standard** must be clear. Use "review" instead of "prohibit."

*   **Minimal Judge Rule**: Don't preset 10 prohibitions; instead, provide a 5-point "self-check checklist."
*   **Rubric**: Tell the model what "good" is.
    *   *Example*: "A good answer should have both the granularity of data and the penetrating power of insight."

---

## II. Semantic Mechanics: Language Density and Resonance

The quality of a Prompt depends on the **energy density** of the language. Vague language leads to a diffuse probability distribution; precise language brings about a sharp, high-confidence output.

### 1. The Alchemy of Verbs

Weak verbs (like "Analyze," "Write") are generic and therefore mediocre. Use strong verbs to anchor the thinking:

*   Use **"Dissect"** instead of "Analyze."
*   Use **"Craft"** instead of "Write."
*   Use **"Synthesize"** instead of "Summarize."
*   Use **"Critique"** instead of "Check."

### 2. Tone Palette

Style is not decoration; it is a carrier of information. Establishing a Vibe is key to preventing the model from outputting "AI flavor."

*   *Example*: "Write in the style of Hemingway's 'Iceberg Theory': write only one-eighth, letting the other seven-eighths surge between the lines."

---

## III. Creative Flow: The Breath of Divergence and Convergence

Prompt design is not a one-shot process; it is a **Breathing** process.

### Phase One: Divergence — Finding the "Soul"

*   **Goal**: Maximize possibilities.
*   **Strategy**:
    *   Provide a strong "World" setting with weak "Format" limitations.
    *   Ask the model to generate multiple, distinctly different versions (Option A/B/C).
    *   Allow the model to challenge your instructions: "If you think my request is unreasonable, please point it out and propose a better solution."
    *   **Metaprompting**: Let the model help you write the Prompt. "I want to do [X], but I don't know how to best describe it. Please ask me questions to refine your System Prompt."

### Phase Two: Convergence — Shaping the "Form"

*   **Goal**: Extract order from chaos and select the optimal solution.
*   **Strategy**:
    *   Introduce the "Judge" component, having the model score and comment on the multiple versions it generated.
    *   Identify the best chain of thought (CoT) and make it explicit.
    *   Begin to solidify the tone and structure.

### Phase Three: Solidification — Handing over the "Bones"

*   **Goal**: For stability, reusability, and security.
*   **Strategy**:
    *   **This is the moment to integrate with "Prompt Engineering V3.0."**
    *   Convert the validated thought paths into `Few-shot Examples` in V3.
    *   Convert the determined format into `Schema` and `JSON Mode` in V3.
    *   Convert the style requirements into `Constraint Injection` in V3.
    *   Add `Security Guardrails` from V3.

---

## IV. The Philosophy Checklist

Before handing your draft over to an engineer (or your own engineering brain), ask yourself three questions:

1.  **Context**: Have I constructed a **self-consistent world**, or just given a pile of dry instructions?
2.  **Resonance**: Are the words I used **sexy and precise** enough to create ripples in the model's neural network?
3.  **Flow**: Have I allowed the model to **think** (diverge) before **executing** (converge)?
