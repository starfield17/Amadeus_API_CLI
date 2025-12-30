# The Complete Prompt Engineering Handbook

> A systematic guide covering the theoretical foundations, practical strategies, engineering standards, and quality assurance for prompt engineering, suitable for scenarios from beginner to production-level applications.

---

## Contents

- [Part 1: Foundational Concepts](#part-1-foundational-concepts)
- [Part 2: Task-Specific Strategies](#part-2-task-specific-strategies)
- [Part 3: Workflow Standards](#part-3-workflow-standards)
- [Part 4: Quality Evaluation Framework](#part-4-quality-evaluation-framework)
- [Part 5: Common Pitfalls & Mitigations](#part-5-common-pitfalls--mitigations)
- [Part 6: Structured Markup & Delimiter Engineering](#part-6-structured-markup--delimiter-engineering)
- [Part 7: Context Window Management](#part-7-context-window-management)
- [Part 8: Multi-Turn Dialogue Engineering](#part-8-multi-turn-dialogue-engineering)
- [Part 9: Parameter Tuning Guide](#part-9-parameter-tuning-guide)
- [Part 10: Dynamic Prompt Templating](#part-10-dynamic-prompt-templating)
- [Part 11: Testing & Validation Framework](#part-11-testing--validation-framework)
- [Part 12: Debugging & Observability](#part-12-debugging--observability)
- [Part 13: Model-Specific Adaptation](#part-13-model-specific-adaptation)
- [Part 14: Cost Optimization Strategies](#part-14-cost-optimization-strategies)
- [Appendix: Cheat Sheets & Checklists](#appendix-cheat-sheets--checklists)

---

# Part 1: Foundational Concepts

## 1.1 How LLMs Work

Large Language Models (LLMs) are fundamentally **probabilistic next-token predictors**. Understanding their core characteristics is essential for writing effective prompts:

| Characteristic | Description | Implication for Prompt Design |
|---|---|---|
| **Probabilistic Prediction** | Predicts the most likely next token given context. | Provide clear context to guide prediction. |
| **Primacy/Recency Effect** | Better memory for content at the beginning and end. | Place key instructions at the start or end of the prompt. |
| **Style Imitation** | Tends to mimic the format and style of the input. | Use examples to guide the desired output style. |
| **Information Dilution** | Key information can get lost in long contexts. | Emphasize or repeat critical instructions. |
| **Literal Understanding** | Infers intent only from literal expressions. | Avoid ambiguity; state intentions explicitly. |
| **No True Comprehension** | Pattern matching, not semantic understanding. | Do not rely on the model to "read between the lines." |

## 1.2 Core Techniques

| Technique | Best For | Implementation | Complexity |
|---|---|---|---|
| **Zero-shot** | Simple, well-defined tasks | Direct, explicit instruction | ★☆☆☆☆ |
| **Few-shot** | Tasks needing specific format/style | Provide 2-5 input→output examples | ★★☆☆☆ |
| **Chain-of-Thought (CoT)** | Reasoning, math, logic tasks | Request "think step-by-step" or provide reasoning examples | ★★★☆☆ |
| **Self-Consistency** | High-reliability reasoning | Generate multiple answers and take majority vote | ★★★☆☆ |
| **Persona** | Tasks requiring an expert perspective | Assign an expert identity + behavioral traits | ★★☆☆☆ |
| **Decomposition** | Complex multi-step tasks | Break down into a series of subtasks | ★★★★☆ |
| **Constraint Injection** | Tasks requiring precise output control | Specify exact format/length/style boundaries | ★★☆☆☆ |
| **Meta-Cognitive Prompting** | Tasks requiring self-checking | Add instructions like "Check if your answer..." | ★★★☆☆ |

---

# Part 2: Task-Specific Strategies

## 2.1 Content Generation

### Key Elements
- **Genre**: Article, email, ad copy, script, etc.
- **Audience**: Background, knowledge level, expectations.
- **Tone**: Formal/informal, humorous/serious, enthusiastic/reserved.
- **Length**: Word or paragraph count.
- **Structure**: Specific framework (e.g., introduction-body-conclusion).

### Example Prompt
```
You are a seasoned tech copywriter skilled at turning complex concepts into engaging stories.

Audience: Urban professionals aged 25-35, interested in tech but not experts.

Task: Write a blog post about AI applications in daily life.

Requirements:
- Tone: Light and engaging, use metaphors/analogies appropriately.
- Structure: Start with a relatable scenario, three main sections, end with reflection.
- Length: 1500-2000 words.

Avoid:
- Buzzwords like "empowerment" or "leverage."
- Exaggerated claims or fear-mongering.

Reference style: Similar to "LatePost" narrative style.
```

## 2.2 Analysis/Reasoning Tasks

### Recommended Frameworks
| Framework | Use Case | Structure |
|---|---|---|
| **SWOT** | Strategic analysis | Strengths, Weaknesses, Opportunities, Threats |
| **5W1H** | Event/Problem analysis | What, Why, Who, When, Where, How |
| **MECE** | Problem decomposition | Mutually Exclusive, Collectively Exhaustive |
| **Pyramid Principle** | Argumentation | Conclusion first, supported by layers of evidence |
| **First Principles** | Root cause analysis | Break down to fundamental assumptions |

### Example Prompt
```
Analyze the following business case using the SWOT framework.

Requirements:
1. List 3-5 points per dimension.
2. Distinguish between 【Fact】 and 【Inference】.
3. Provide overall recommendations.

Case Material:
{case_content}

Output Format:
## Strengths
- [Point 1]【Fact/Inference】: Explanation...

## Weaknesses
...

## Recommendations
Based on the analysis, recommend...
```

## 2.3 Programming/Technical Tasks

### Essential Elements
- **Language & Version**: Python 3.10, Node.js 18, etc.
- **Dependencies**: Required libraries/frameworks.
- **Code Standards**: Naming conventions, comments.
- **Error Handling**: Exception handling strategy.
- **Edge Cases**: Null values, extreme inputs.

### Example Prompt
```
Write a Python function to validate user input.

Environment:
- Python 3.9+
- Standard library only.

Functionality:
Validate email address format.

Input/Output:
- Input: String email address.
- Output: Boolean (True=valid, False=invalid).

Edge Cases:
- Empty string → False
- None input → False
- Leading/trailing spaces → Trim then validate.

Code Requirements:
- Add docstring.
- Add type hints.
- Include at least 5 unit test cases.

Examples:
Input: "user@example.com" → Output: True
Input: "invalid-email" → Output: False
```

---

# Part 3: Workflow Standards

## 3.1 Phase 1: Requirements Gathering

### Information Checklist
| Question | Purpose |
|---|---|
| What is the core objective? | Define main task. |
| What is the input format/source? | Understand data characteristics. |
| What is the expected output format? | Define deliverable. |
| What is the usage scenario? | One-off/batch/embedded application. |
| What defines success? | Establish evaluation criteria. |
| What is absolutely unacceptable? | Identify failure boundaries. |
| How are multiple objectives prioritized? | Clarify priority. |
| What are the hard constraints? | Identify unbreakable rules. |
| Any style/tone requirements? | Determine expression. |
| Any length limits? | Control output size. |

## 3.2 Phase 2: Prompt Architecture

### Modular Structure Template
```
[Module 1] Role & Identity
  → Professional background, capabilities, behavioral principles.

[Module 2] Task Definition
  → Clear, specific, unambiguous one-sentence goal.

[Module 3] Context Injection
  → Background info, domain knowledge, external constraints.

[Module 4] Method Guidance
  → Thinking steps, analytical framework, processing flow.

[Module 5] Output Specification
  → Format, structure, style, length.

[Module 6] Examples (if needed)
  → 1-3 complete input→output examples.

[Module 7] Boundaries & Taboos
  → Explicit prohibitions, content to avoid, exception handling.

[Module 8] Quality Check Instructions
  → Self-checklist, common error reminders, validation steps.
```

## 3.3 Phase 3: Language Optimization

| Principle | ❌ Not Recommended | ✅ Recommended |
|---|---|---|
| Specific over Abstract | "Summarize concisely" | "Summarize into 3 bullet points, ≤20 words each" |
| Positive over Negative | "Don't be biased" | "Remain objective and neutral" |
| Structured over Prose | Long paragraph of instructions | Use numbering, labels, delimiters |
| Example over Description | "Output should be professional" | Provide an example of professional output |
| Hierarchical over Flat | All instructions flattened | Use XML tags or Markdown headings |

---

# Part 4: Quality Evaluation Framework

## 4.1 Six-Dimension Evaluation Matrix

| Dimension | Evaluation Questions | Scoring (1-5) |
|---|---|---|
| **Clarity** | Is it ambiguous? Can a novice understand immediately? | |
| **Completeness** | Does it cover all necessary information? | |
| **Precision** | Are constraints specific and actionable? | |
| **Robustness** | Does it guide handling of edge cases? | |
| **Efficiency** | Is there redundancy? Can it be simplified? | |
| **Testability** | Can output quality be judged objectively? | |

## 4.2 Pre-Release Checklist
```
□ Basic Checks
  □ Clear task objective?
  □ Input/output format defined?
  □ Sufficient context provided?

□ Constraint Checks
  □ All constraints quantifiable?
  □ Any conflicting constraints?
  □ Edge cases covered?

□ Example Checks
  □ Examples cover typical scenarios?
  □ Example format matches requirements?
  □ Counter-examples included?

□ Language Checks
  □ Ambiguous expressions removed?
  □ Unnecessary redundancy removed?
  □ Logical instruction order?

□ Security Checks
  □ Injection prevention measures?
  □ Prohibited behaviors stated?
  □ Sensitive content handling strategy?
```

---

# Part 5: Common Pitfalls & Mitigations

| Pitfall | Symptoms | Mitigation |
|---|---|---|
| **Conflicting Instructions** | Output wavers between different requirements | Review for contradictions; set clear priority. |
| **Implicit Assumptions** | Model misinterprets "obvious" facts | State even "obvious" facts explicitly. |
| **Over-Constraint** | Output is rigid, unnatural | Distinguish hard vs. soft constraints; allow some flexibility. |
| **Under-Constraint** | Output is too random, uncontrollable | Add specific format/length/style requirements. |
| **Ignored Boundaries** | Crashes on empty/abnormal input | Define exception handling strategy. |
| **Style Drift** | Style deviates over long outputs | Reiterate style requirements at the end. |
| **Example Overfitting** | Output copies example details too closely | Provide diverse examples; state examples are illustrative. |
| **Instruction Forgetting** | Early instructions forgotten in long dialogues | Repeat key instructions; use persistent markers. |

---

# Part 6: Structured Markup & Delimiter Engineering

## 6.1 Delimiter Selection Guide

| Delimiter | Example | Best For | Pros | Cons |
|---|---|---|---|---|
| **XML Tags** | `<context>...</context>` | Complex nesting, clear boundaries | Semantic clarity, supports nesting | Token-heavy |
| **Markdown Headings** | `## Section` | Hierarchical instructions | Readable, token-efficient | Not for deep nesting |
| **Triple Backticks** | ```code``` | Code blocks, raw text | Clear isolation | Mainly for code |
| **Bracket Tags** | `[INSTRUCTION]...[/INSTRUCTION]` | Simple separation | Concise | Less semantic clarity |
| **Horizontal Rules** | `---`, `===` | Logical separation | Simple, visual | No nesting |
| **Numbered Lists** | `1. 2. 3.` | Sequential steps | Shows order | Not for complex structures |

## 6.2 Injection Prevention

### Protection Strategies
1. **Input Isolation**: Wrap user input in dedicated tags treated as data, not instructions.
2. **Permission Declaration**: State that system instructions have highest priority; ignore user commands attempting to change behavior.
3. **Input Sanitization**: Escape potential delimiters in user input.
4. **Behavior Anchoring**: State core principles that persist regardless of user input.

---

# Part 7: Context Window Management

## 7.1 Token Budget Allocation

| Model Context | System Instructions | Context/History | User Input | Output Reserve |
|---|---|---|---|---|
| 4K tokens | 600-800 | 1200-1600 | 400-800 | 1200-1600 |
| 8K tokens | 1200-1600 | 2400-3200 | 800-1600 | 2400-3200 |
| 32K tokens | 4800-6400 | 9600-12800 | 3200-6400 | 9600-12800 |
| 128K+ tokens | As needed | Mainly for long docs | As needed | As needed |

## 7.2 Long Text Processing

### Chunking Strategies
| Strategy | Description | Best For |
|---|---|---|
| Fixed-Length Chunking | Split by token count | Simple, fast (may break semantics) |
| Semantic Boundary Chunking | Split by paragraphs/sections | Preserves semantic integrity |
| Overlapping Chunks | Keep overlap between chunks | Prevents boundary information loss |
| Hierarchical Chunking | Coarse then fine splitting | Very long documents |

### Information Density Optimization
- Remove redundant polite phrases.
- Replace prose with tables.
- Use an abbreviation glossary.
- Compress examples.

---

# Part 8: Multi-Turn Dialogue Engineering

## 8.1 State Management Modes

| Mode | Description | Pros | Cons | Best For |
|---|---|---|---|---|
| **Stateless** | Full context each turn | Simple, reliable | High token cost | Simple Q&A |
| **Sliding Window** | Keep last N turns | Balanced | May lose early info | General dialogue |
| **Summary Compression** | Periodically compress history | Saves tokens | Compression may lose details | Long conversations |
| **Keyframe Extraction** | Keep only key turns | Efficient, precise | Complex to implement | Task-oriented dialogues |
| **Hybrid Mode** | Combine strategies | Flexible | Most complex | Complex applications |

## 8.2 Instruction Persistence

### Anti-Forgetting Strategies
- **Persistent Rules Section**: Define immutable core rules with highest priority.
- **Periodic Reminders**: Inject rule reminders every N turns.
- **State Tracking**: Maintain conversation state (intent, collected info, next action).

---

# Part 9: Parameter Tuning Guide

## 9.1 Core Parameters

### Temperature
Controls randomness/creativity.

| Value Range | Effect | Best For |
|---|---|---|
| 0.0 | Nearly deterministic output | Factual queries, code generation, data extraction |
| 0.1-0.3 | Low randomness, high consistency | Translation, summarization, format conversion |
| 0.4-0.6 | Balanced | General writing, Q&A |
| 0.7-0.9 | High creativity | Creative writing, brainstorming |
| 1.0+ | Very random | Extreme creativity (use cautiously) |

### Top-p (Nucleus Sampling)
Controls the probability mass to sample from.

| Value Range | Effect | Best For |
|---|---|---|
| 0.1-0.3 | Only highest probability tokens | Tasks requiring high precision |
| 0.4-0.6 | Focuses on mainstream expressions | General tasks |
| 0.7-0.9 | Allows diverse expressions | Creative tasks |
| 0.95-1.0 | Minimal filtering | Maximum diversity |

### Max Tokens
Set to ~1.3-1.5x the expected output length to avoid truncation.

## 9.2 Parameter Combinations by Task

| Task Type | Temperature | Top-p | Notes |
|---|---|---|---|
| Code Generation | 0.0-0.2 | 0.1-0.3 | Precision first |
| JSON Output | 0.0 | 0.1 | Format must be exact |
| Factual Q&A | 0.0-0.3 | 0.3-0.5 | Accuracy first |
| Document Translation | 0.2-0.4 | 0.5-0.7 | Balance accuracy & fluency |
| Business Copywriting | 0.5-0.7 | 0.7-0.9 | Creative but controlled |
| Creative Writing | 0.7-1.0 | 0.9-1.0 | Maximize creative space |
| Poetry Generation | 0.8-1.0 | 0.95-1.0 | Break conventional expression |

---

# Part 10: Dynamic Prompt Templating

## 10.1 Variable Interpolation

### Basic Syntax
```
Single variable: {{variable_name}}
With default: {{variable_name|default:"Default Value"}}
Conditional: {{#if condition}}...{{/if}}
Loop: {{#each items}}{{this}}{{/each}}
```

### Example
```
Analyze the following {{doc_type|default:"document"}} and extract {{extract_fields}}.

Audience: {{audience}}
Language: {{language|default:"Chinese"}}

{{#if include_summary}}
Provide a ≤100-word summary at the beginning.
{{/if}}
```

## 10.2 Conditional Branching

### User-Level Adaptation
```xml
<dynamic_instructions>
  {{#if user_level == "expert"}}
    <instruction>
      Use professional terminology with technical details. Industry abbreviations OK; no need to explain basics.
    </instruction>
  {{else if user_level == "intermediate"}}
    <instruction>
      Use professional terms but briefly explain key concepts. Balance depth and understandability.
    </instruction>
  {{else}}
    <instruction>
      Use plain language, avoid jargon. Explain complex concepts with analogies and examples.
    </instruction>
  {{/if}}
</dynamic_instructions>
```

---

# Part 11: Testing & Validation Framework

## 11.1 Test Case Types

| Test Type | Purpose | # of Cases | Example |
|---|---|---|---|
| **Golden Tests** | Verify core functionality | 5-10 | Standard input → Expected output |
| **Edge Case Tests** | Verify handling of extremes | 10-20 | Empty input, very long input, special characters |
| **Format Tests** | Verify output format stability | 5-10 | JSON validity, required fields present |
| **Consistency Tests** | Verify results are consistent | 3-5 sets × 5 runs | Run same input 5 times, compare |
| **Adversarial Tests** | Verify security boundaries | 10-15 | Prompt injection, role hijacking |
| **Regression Tests** | Verify updates don't break old functionality | All historical cases | Run after every update |

## 11.2 Evaluation Metrics

### For Deterministic Tasks
- Accuracy, Precision, Recall, F1 Score, Exact Match Rate.

### For Generative Tasks
- Human Evaluation (1-5 score).
- GPT-as-Judge (using another LLM as evaluator).
- BLEU/ROUGE (compares to reference text).
- Pairwise Comparison (choose better of two outputs).

### GPT-as-Judge Prompt Example
```
You are a professional text quality evaluator. Assess the following AI-generated content.

Evaluation Dimensions (1-5 each):
1. Relevance
2. Accuracy
3. Completeness
4. Readability
5. Format Compliance

Task: {{task}}
Criteria: {{criteria}}
AI Output: {{output}}

Output in JSON format with scores and reasons.
```

---

# Part 12: Debugging & Observability

## 12.1 Logging Standards

### Essential Log Fields
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "uuid-xxx",
  "prompt": { "version": "2.0.0", "system_prompt": "...", "user_input": "...", "full_prompt": "..." },
  "parameters": { "model": "gpt-4", "temperature": 0.7, "max_tokens": 1000, "top_p": 0.9 },
  "response": { "content": "...", "finish_reason": "stop", "tokens_used": { "prompt": 500, "completion": 300, "total": 800 } },
  "metrics": { "latency_ms": 2500, "cost_usd": 0.024 }
}
```

## 12.2 Failure Diagnosis

### Quick Checklist
```
□ Basic Checks
  □ API call successful?
  □ Token limits exceeded?
  □ Parameters reasonable?

□ Prompt Checks
  □ Instructions clear and unambiguous?
  □ Any conflicting constraints?
  □ Examples correct?

□ Context Checks
  □ Enough information provided?
  □ Key information in effective positions?
  □ Any noise interfering?

□ Parameter Checks
  □ Temperature appropriate for task?
  □ max_tokens sufficient?
  □ Top-p needs adjustment?
```

---

# Part 13: Model-Specific Adaptation

## 13.1 Cross-Model Migration Checklist
```
□ Context Window
  □ Target model's window size sufficient?
  □ Prompt length adjustment needed?

□ Instruction Format
  □ System Message supported?
  □ Special markup syntax compatible?

□ Capability Differences
  □ Instruction-following capability different?
  □ Certain tasks need more detailed guidance?

□ Output Style
  □ Default output style different?
  □ Additional style constraints needed?

□ Safety Boundaries
  □ Safety restrictions different?
  □ Some tasks need rephrasing?
```

## 13.2 Model Capability Boundaries

### Strong Areas
- Text understanding, logical reasoning, code generation, creative writing, multilingual processing, format conversion.

### Weak Areas
- Precise mathematical calculation (needs tools), real-time information (knowledge cutoff), visual-spatial reasoning (text-only models), long-term memory (context window limit), personal preferences (no persistent state), latest domain-specific developments.

---

# Part 14: Cost Optimization Strategies

## 14.1 Cost Composition

### Typical Distribution
- **Total Cost = Input (60%) + Output (40%)**
- **Input Breakdown**: System Prompt (20%), Context (25%), User Input (15%)
- **Output**: Response (40%)

### Optimization Priority
1. System Prompt compression (highest impact for frequent calls).
2. Context management (controls long conversation cost).
3. Output control (avoid redundant output).

## 14.2 Prompt Compression Techniques

| Strategy | Compression Rate | Risk | Best For |
|---|---|---|---|
| Remove Redundant Politeness | 10-15% | Low | All scenarios |
| Use Abbreviation Glossary | 15-25% | Low | Terminology-dense scenarios |
| Replace Prose with Tables | 20-40% | Low | Options/rules description |
| Compress Examples | 30-50% | Medium | Scenarios with many examples |
| Dynamic Module Loading | Variable | Medium | Multi-task scenarios |

## 14.3 Caching & Reuse

### Prompt Caching
Use model-provided prompt caching features where fixed prefixes are billed only once.

### Response Caching
Cache responses based on prompt + parameters hash with a TTL.

## 14.4 Model Tiering

### Task Routing
Route simple tasks to cheaper models (e.g., GPT-3.5), complex tasks to more capable models (e.g., GPT-4).

| Tier | Cost Ratio | Best For | Quality |
|---|---|---|---|
| Lightweight | 1x | Simple Q&A, format conversion | Adequate |
| Standard | 10-20x | General writing, analysis | Good |
| Premium | 30-50x | Complex reasoning, professional tasks | Best |

## 14.5 Batch Processing

Combine multiple tasks into a single prompt request if the model supports it to reduce API call overhead.

---

# Appendix: Cheat Sheets & Checklists

## Appendix A: Prompt Writing Cheat Sheet

### Task Type → Technique Selection
| Task Type | Recommended Technique | Temperature | Key Elements |
|---|---|---|---|
| Factual Q&A | Zero-shot | 0.0-0.2 | Clear question |
| Format Conversion | Zero-shot + Constraint | 0.0 | Format specification |
| Text Classification | Few-shot | 0.0-0.3 | Label examples |
| Text Summarization | Zero-shot + Constraint | 0.2-0.4 | Length limit |
| Creative Writing | Persona + Few-shot | 0.7-1.0 | Style examples |
| Logical Reasoning | CoT | 0.0-0.3 | Step-by-step guidance |
| Complex Analysis | Decomposition + CoT | 0.3-0.5 | Framework guidance |
| Code Generation | Few-shot + Constraint | 0.0-0.2 | Specification examples |

### Common Constraint Expressions
| Constraint Type | Expression |
|---|---|
| Length Limit | "Keep within X words/paragraphs/items." |
| Format Requirement | "Output format must be JSON/Markdown/..." |
| Style Requirement | "Tone should be formal/casual/professional/..." |
| Prohibitions | "Do not include X / Avoid Y / Never Z." |
| Required Content | "Must include X / Ensure to mention Y." |
| Structure Requirement | "Organize in A → B → C structure." |

## Appendix B: Pre-Release Checklist
```
□ 1. Functionality Verified
   □ All golden tests pass.
   □ Edge cases handled correctly.
   □ Output format compliant.

□ 2. Security Verified
   □ Passed adversarial tests.
   □ Input isolation effective.
   □ Sensitive information handled properly.

□ 3. Performance Verified
   □ Token usage within budget.
   □ Response latency acceptable.
   □ Consistency tests pass.

□ 4. Documentation Complete
   □ Version number updated.
   □ Changelog recorded.
   □ Usage instructions updated.

□ 5. Rollback Prepared
   □ Previous version accessible.
   □ Rollback procedure tested.
```

---

## Version Info

- **Version**: 2.0.0
- **Last Updated**: 2025
- **Language**: English

---

*This handbook is continuously updated. Feedback and contributions are welcome.*