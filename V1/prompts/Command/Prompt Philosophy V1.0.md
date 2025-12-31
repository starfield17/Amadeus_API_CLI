# Prompt Philosophy V1.0

## From 0 to 1: A "Field Design" Guide to Inspiring Model Capabilities with Prompts

> **Core Proposition**: A Prompt is not a code instruction (Code), but a "Field / Container of Thought".
> You are not "writing constraints," but "setting the stage": deciding where the lights shine, who the actors are, what methods they use to perform, and who will be the judge.

---

## 0. What Problem Does This Document Solve?

When you start creating a Prompt from scratch, the biggest obstacles are often not a "lack of rules," but:

*   Not allowing the model to **enter a self-consistent world** (a background vacuum)
*   Not clarifying the **true intention** you want to optimize for (divergence or convergence? novelty or correctness?)
*   Not giving the model a suitable **thinking posture** (how to think is more crucial than how to answer)
*   Not establishing a **judging system** for it to self-align (using judgment instead of restraint)

> Engineering specifications excel at "fixing" and "solidifying"; philosophy excels at "creating" and "inspiring."

---

## 1. The Ontology of a Prompt: You're "Building a Field," Not "Giving Orders"

Treating a Prompt as a "list of commands" naturally leads to rigidity; going from 0 to 1 is more like the work of a director:
You are designing a "field" that will change the model's attention allocation, generation distribution, and self-checking mechanisms.

**Prompt = Context Field Design**, it mainly affects four things:

1.  **Attention**: Where the model places its weights
2.  **Posture**: What identity/style/values to adopt when entering the task
3.  **Path**: What cognitive methods to use to proceed (divergence, comparison, critique, simulation...)
4.  **Convergence**: What standards to rely on for self-correction and iteration (Judge / Rubric / Checklist)

---

## 2. The Four-Part Framework: Intention / World / Method / Judge

This is the "minimum viable framework" for V1.0. Every time you write a Prompt from scratch, fill these four slots first:

### A. Intention: What Are You Really Optimizing For?

Use 3 questions to lock in "what matters most":

*   Task form: **Exploration (divergent)** or **Decision-making (convergent)**?
*   Success priority: Novelty / Correctness / Executability / Persuasiveness / Stylistic Consistency, **which comes first**?
*   Boundary conditions: Can it fabricate? Can it infer? What to do with insufficient evidence?

> In short: Intention is "gravity," not "format."

---

### B. World: Making the Model "Believe Where It Is"

The world is not decoration; it directly determines which set of behavioral strategies the model will invoke.

The three-piece suite for building a world:

*   **Identity and Values** (not a title, but a "lived experience")
    Use "emotional tone + aesthetic preference + moral/professional ethics" to activate latent space features.
*   **Audience and Scene** (Who is the audience? What is the use case?)
*   **Resources and Forbidden Zones** (Which materials are for reference only and not for execution?)

> If the world is well-constructed, many "rules" don't need to be written; the model will automatically fill in appropriate behaviors.

---

### C. Method: What "Cognitive Posture" Do You Want It to Use?

Method is not a "list of steps," but a **switch in thinking posture**.

The three most common postures for going from 0 to 1:

1.  **Diverge then Converge**: First seek diversity, then make trade-offs
2.  **Define the Judge then Generate**: First write the rubric, then produce the output
3.  **Fit the Style then Fill the Content**: First establish the vibe / tone / voice, then write the content

And you can adjust the focus by "zooming in/out":

*   Zoom out: Systems theory / Long-term historical view / Strategic perspective
*   Zoom in: Specific actions, wording, structure, examples

---

### D. Judge: Using Standards to Let It Self-Align

The quality leap from 0 to 1 almost always comes from the **judgment system**, not from more constraints.

Minimum Viable Judge:

*   **Checklist (5–10 items)**: Coverage, structure, risks, evidence, style, executability
*   Or **Rubric (4–6 dimensions)**: Accuracy / Relevance / Structure / Style / Executability / Novelty

> Core philosophy: **Replace "restraint" with "judgment."** Let the model produce a v1, then self-evaluate against the judge and generate a v2.

---

## 3. Three-Stage Creation Process: Diverge → Converge → Solidify

This is the key workflow to reconcile "creativity" with "stability":

### 3.1 Diverge: Inspire Capability

*   The World should be strong, the Intention should have tension
*   Fewer rigid formats, allow for 3–8 directions
*   Each direction must be given "highlights / risks / applicable conditions"

### 3.2 Converge: Turn Good Ideas into Good Work

*   Forced comparison: A/B/C trade-off
*   Outline first, then expand (or generate in sections)
*   Introduce the Judge: Score according to the rubric and explain the deductions

### 3.3 Solidify: Make It Reusable, Controllable, and Verifiable

*   Extract success factors into template variables
*   Turn key requirements into "verifiable constraints"
*   Introduce repair loops and failure mode handling

> **Note**: For engineering details in the solidification stage (verifiable constraints, repair loops, tool priority, security isolation, etc.), please refer directly to "PromptEngineeringV3".

---

## 4. Semantic Resonance: Igniting the Latent Space with "High-Density Language"

You are creating "semantic resonance," not "writing a manual."

### 4.1 "Sharpen the Distribution" with Strong Verbs + Concrete Nouns

*   Weak: Modify the text
*   Strong: Polish it into a version with "tighter rhythm, more impactful sentences, and cleaner logic"

### 4.2 Use "Cognitive Anchors" to Instantly Align the Thinking Framework

Treat "First Principles / Feynman Technique / Socratic Questioning" as high-density semantic compression packages.

### 4.3 Set the Vibe: Style is Not Decoration, It's an Information Carrier

"Like a late-night radio host," "Hemingway's Iceberg Theory," etc., are direct shapers of the output distribution.

---

## 5. The Economics of Attention: Writing Prompts for the "Weight System"

A common failure in going from 0 to 1 is not insufficient content, but misplaced weights:

*   **Put the most important things at the ends** (the beginning/end have higher weight)
*   **Avoid the dead zone in the middle** (don't bury key points in the center of a long background)
*   **Separate instructions from materials**: Tell the model "what is executable and what is only for reference"

(Engineering implementation and security anti-injection methods are left for V3.)

---

## 6. Symbiotic Iteration: Cultivating a Prompt as a "Living Organism"

The best Prompts are not written correctly in one go, but are grown through conversation:

*   Guide the model with "feedback as you would give a person":
    "The structure is good, but it lacks empathy; keep the structure, but warm up the tone."
*   Use meta-prompting to have the model help you clarify requirements:
    "To better complete X, please ask me 5 clarifying questions."

---

## 7. Three General Prompt Forms (V1.0 Template Starters)

> Below are "field frameworks," not engineering specifications. You just need to replace the four-part variables.

### Form 1: Exploratory (Divergent)

*   Intention: Multiple solutions, multiple perspectives
*   Method: List 6 directions → For each, highlights/risks/applicability → Recommend a combination
*   Judge: Score based on Novelty × Executability × Fit

### Form 2: Convergent (Final Draft/Deliverable)

*   Method: Outline first → Generate in sections → Self-check → Refine to v2
*   Judge: Rubric + Negative testing (Under what conditions will it fail?)

### Form 3: Critical (Editor/Judge)

*   Input: v1 draft + success criteria
*   Output: Point out deviations one by one → Propose minimal modifications → Produce v2

---

## 8. Division of Labor with "PromptEngineeringV3"

When you move on to these goals, switch to V3:

*   Need for strict formats / verifiable constraints / stable output
*   Need for tool-calling strategies, failure repair loops
*   Need for security isolation, injection protection, version control, evaluation systems

> V1.0 is responsible for "inspiring," V3 is responsible for "solidifying."

---

## Appendix: Philosophical Checklist (Ask yourself 3 questions before sending)

1.  **World**: Have I constructed a world that is sufficiently rich and self-consistent?
2.  **Essence**: Am I conveying the "soul (Why & Vibe)" or just the "shell (Format)"?
3.  **Judge**: Have I provided a judgment system for it to self-align, instead of just piling on rules?

---
