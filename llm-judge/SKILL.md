---
name: llm-judge
description: >
  Evaluate any system against its requirements. Trigger only when user explicitly asks for a "judge report" or similar evaluation. Follow the structured process in SKILL.md to produce a comprehensive, evidence-based assessment. Do not use with others skills or for tasks other than system evaluation.
disable-model-invocation: true
---

# Judge Skill

## Purpose

Perform an independent, evidence-based evaluation of a system against its stated
requirements. The judge does not propose redesigns or regenerate artifacts — it
only reports what it finds. Every finding must be grounded in the provided
materials.

Works for:
- Conceptual-only designs (architecture documents, GAIA models, system specs)
- Mixed systems (design documents + code)
- Code-only projects

---

## Output Schema

Produce a **JudgeReport** with the following fields. Emit it as structured JSON
at the end of your analysis.

```
JudgeReport {
  summary:                  str          # 2–4 sentences, overall verdict
  recommendation:           "pass" | "needs_revision" | "fail"
  scores:                   JudgeScores
  findings:                 JudgeFinding[]
  missing_requirements:     str[]        # requirements not addressed at all
  logical_inconsistencies:  str[]        # internal contradictions in the system
  implementation_risks:     str[]        # risks if system is built/deployed as-is
}

JudgeScores {
  requirements_fit:      int  # 0–10  How well the system addresses all stated requirements
  logical_consistency:   int  # 0–10  Internal coherence; no contradictions or gaps
  component_coverage:    int  # 0–10  All required components/agents/services are present
  interface_logic:       int  # 0–10  Communication, APIs, event flows are well-defined
  implementation_alignment: int # 0–10  Code matches the described design (n/a → 5 for conceptual-only)
  overall:               int  # 0–10  Holistic score; not an arithmetic average
}

JudgeFinding {
  category:       str                              # Area being evaluated (e.g. "Security", "Requirements", "API Design")
  severity:       "low" | "medium" | "high" | "critical"
  description:    str                              # Specific issue or strength found
  evidence:       str                              # Short quote or reference from the materials
}
```

> **Mapping note for GAIA / multi-agent systems:** `component_coverage` maps to
> `agent_service_coverage` and `interface_logic` maps to `communication_logic`
> in the original JudgeReport schema. Use the original field names when writing
> JSON if the consuming system expects them.

---

## Evaluation Process

Work through the five phases in order. Do not skip a phase even if materials
seem thin — note what is absent instead.

---

### Phase 1 — Intake & Classification

1. Read every provided artifact: requirements list, description, design
   documents, architecture diagrams, code files, test files.
2. Classify the system:
   - **conceptual-only** — no code present
   - **design + code** — both design docs and implementation exist
   - **code-only** — implementation with no separate design docs
3. Detect programming languages if code is present.
4. **If code is present**, load the language-specific checklist before Phase 4:

   | Language | File to read |
   |----------|-------------|
   | Python   | `references/review-checklist/python.md` |
   | C++      | `references/review-checklist/cpp.md`    |
   | C#       | `references/review-checklist/csharp.md` |
   | Kotlin   | `references/review-checklist/kotlin.md` |
   | Go       | `references/review-checklist/golang.md` |

   Load only the files for languages actually present. Do not load all of them.

---

### Phase 2 — Requirements Analysis

1. List every stated requirement (functional and non-functional).
2. For each requirement, determine:
   - **Satisfied** — explicit evidence in the design or code
   - **Partially satisfied** — addressed but incomplete
   - **Missing** — no evidence of it being addressed
3. Note conflicting or ambiguous requirements.
4. Populate `missing_requirements` with requirements that are absent entirely.

---

### Phase 3 — System Consistency & Coverage

Check the system as a whole, independent of individual requirements:

**Logical consistency**
- Are component responsibilities clearly defined and non-overlapping?
- Do data flows make sense end-to-end?
- Are there circular dependencies, undefined states, or unreachable paths?
- Are assumptions stated and reasonable?

**Component coverage** (agents / services / modules)
- Does every required capability have a responsible component?
- Are there orphaned components with no role?
- For multi-agent systems: are agent roles justified and non-redundant?

**Interface logic** (communication / APIs / events)
- Are all communication paths between components defined?
- Are request/response contracts specified?
- Are error paths and fallbacks defined on interfaces?
- For multi-agent systems: are message formats, protocols, and orchestration logic clear?

**Implementation alignment** (skip for conceptual-only, score `null`)
- Does the code structure match the described architecture?
- Are all described components implemented?
- Does the implementation introduce components or behaviors not in the design?

Populate `logical_inconsistencies` with contradictions or structural gaps found.

---

### Phase 4 — Code Review (skip for conceptual-only)

Apply the rules below in severity order. Load the language-specific reference
from Phase 1 before starting this phase.

Use the **confidence filter**:

| Confidence | Action |
|------------|--------|
| >80%       | Include the finding |
| 50–80%     | Omit unless security-related |
| <50%       | Always omit |

Consolidate: multiple instances of the same issue → one finding with count.

#### CRITICAL — Security (flag unconditionally, no confidence threshold)

- **Hardcoded credentials** — keys/passwords/tokens in source → env vars or secret manager
- **SQL injection** — string concatenation in queries → parameterized queries
- **Command injection** — user input in subprocess/shell → validate + `shell=False`
- **Path traversal** — user-controlled paths unsanitized → resolve + prefix check
- **Auth bypass** — missing auth checks on protected routes
- **Insecure deserialization** — `pickle`/`eval`/`exec` on untrusted data
- **Secrets in logs** — logging tokens, passwords, or PII
- **XSS** — unescaped user input rendered in HTML
- **CSRF** — state-changing endpoints without CSRF protection

#### CRITICAL — Error Handling

- **Empty except/catch** — `except: pass` or `catch {}` swallows failures silently
- **Missing resource cleanup** — no `with`/`using`/`try-finally` for files, sockets, DB connections
- **Blocking async** — sync I/O or `.result()`/`.wait()` inside an async context

#### HIGH — Code Quality

- **Large functions** (>50 lines) → extract helpers
- **Large files** (>500 lines) → extract modules
- **Deep nesting** (>4 levels) → use early returns
- **Dead code** — commented-out blocks, unused imports, unreachable branches
- **Debug artifacts** — `print()`, `console.log`, `debugger` left in production paths
- **Magic numbers** — unexplained numeric literals → named constants
- **Missing cancellation/timeout** — async or HTTP calls with no timeout or cancellation support

#### HIGH — File Hygiene

- **Excessive trailing blank lines** (>5 at end of file)
- **Duplicate function/class definitions** at module scope — silent overwrite in Python, dead code elsewhere
- **AI-generated header comments** that conflict with project style rules

#### MEDIUM — Performance

- String concatenation in loops → `"".join()` or equivalent
- Unnecessary re-computation inside loops that could be hoisted
- Missing caching for repeated identical external calls
- Wrong collection type (list where set/dict lookup would be O(1))

#### LOW — Best Practices

- TODO/FIXME without a linked ticket or issue number
- Missing docstrings on public APIs
- Poor naming (single-letter variables in non-trivial contexts)
- Missing type hints on public function signatures

#### Code Quality Principles (check holistically)

- **Readability first** — code is read more than written; prefer clarity over cleverness
- **Single responsibility** — every function, class, and module does one thing
- **Explicit over implicit** — no hidden defaults or surprising side effects
- **Fail loudly** — errors surface immediately; never silently swallowed
- **No commented-out code** in commits
- **No hardcoded configuration** — environment variables for all configuration values
- **Dependencies pinned** — `requirements.txt`, `pyproject.toml`, or equivalent

Populate `implementation_risks` with code-level issues that could cause failures
in production.

---

### Phase 5 — Score & Report

Score each dimension using the guide below, then write the summary and
determine the recommendation.

#### Scoring Guide

**requirements_fit**
| Score | Meaning |
|-------|---------|
| 9–10  | All requirements clearly addressed with evidence |
| 7–8   | Most requirements addressed; minor gaps only |
| 5–6   | Several requirements partially addressed or thin |
| 3–4   | Multiple requirements missing or contradicted |
| 0–2   | Fundamental requirements unmet |

**logical_consistency**
| Score | Meaning |
|-------|---------|
| 9–10  | No contradictions; all flows and responsibilities are coherent |
| 7–8   | Minor ambiguities; no structural contradictions |
| 5–6   | Notable gaps or unclear responsibilities |
| 3–4   | Contradictions between components or stated goals |
| 0–2   | System is internally incoherent |

**component_coverage**
| Score | Meaning |
|-------|---------|
| 9–10  | All required components present and justified |
| 7–8   | Mostly complete; one or two minor omissions |
| 5–6   | Significant components missing or redundant |
| 3–4   | Core components absent |
| 0–2   | Coverage is severely incomplete |

**interface_logic**
| Score | Meaning |
|-------|---------|
| 9–10  | All interfaces defined; error paths covered |
| 7–8   | Most interfaces defined; minor gaps in error handling |
| 5–6   | Some interfaces undefined or contracts vague |
| 3–4   | Major communication paths missing |
| 0–2   | Interfaces are largely undefined |

**implementation_alignment** (score 5 for conceptual-only)
| Score | Meaning |
|-------|---------|
| 9–10  | Code fully matches design; no undocumented deviations |
| 7–8   | Mostly aligned; minor deviations noted |
| 5–6   | Noticeable divergence between design and code |
| 3–4   | Significant parts of design not implemented or contradicted |
| 0–2   | Implementation bears little resemblance to design |

**overall**
A holistic score reflecting the system's readiness. Not an arithmetic average —
weight requirements_fit and logical_consistency more heavily, and penalize
any CRITICAL findings by at least 2 points regardless of other scores.

#### Recommendation Rules

| Recommendation    | Condition |
|-------------------|-----------|
| `pass`            | No CRITICAL findings AND overall ≥ 7 |
| `needs_revision`  | No CRITICAL findings AND overall 4–6, OR HIGH findings present |
| `fail`            | Any CRITICAL finding present, OR overall ≤ 3 |

---

## Output Format

After completing all phases, produce:

1. A brief prose walkthrough of your analysis (optional, aids transparency).
2. The `JudgeReport` as a JSON block.

```json
{
  "summary": "...",
  "recommendation": "pass | needs_revision | fail",
  "scores": {
    "requirements_fit": 0,
    "logical_consistency": 0,
    "component_coverage": 0,
    "interface_logic": 0,
    "implementation_alignment": 0,
    "overall": 0
  },
  "findings": [
    {
      "category": "...",
      "severity": "critical | high | medium | low",
      "description": "...",
      "evidence": "..."
    }
  ],
  "missing_requirements": [],
  "logical_inconsistencies": [],
  "implementation_risks": []
}
```

---

## Evaluation Constraints

- **Report only.** Do not propose regeneration, rewrite, or redesign steps.
- **Ground every criticism.** Each finding must cite evidence from the provided
  materials — a requirement text, a code line, a document excerpt.
- **Prefer concrete over general.** "Function `process_data` has no error
  handling on line 42" beats "error handling is missing."
- **No phantom findings.** Do not invent problems not evidenced in the materials.
  If information is absent, note the absence rather than guessing intent.
- **Acknowledge strengths.** Use `low`-severity positive findings to document
  what the system does well — findings are not exclusively negative.
