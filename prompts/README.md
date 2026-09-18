# Zavran AI — Prompt Architecture & Orchestration System

This directory contains the authoritative system prompts, schemas, and orchestration specifications for the **Zavran AI Technical Recruiter Engine**.

---

## Directory Overview

- **[interview_preparation_20_questions.md](file:///d:/Zevaran/prompts/interview_preparation_20_questions.md)**: System prompt and structured schema for compiling the exact 20-question pre-interview preparation pool prior to room readiness.
- **[answer_evaluation_and_depth.md](file:///d:/Zevaran/prompts/answer_evaluation_and_depth.md)**: Conceptual answer evaluation prompt evaluating candidate responses against hidden rubrics without keyword-matching bias.
- **[next_question_moving_logic.md](file:///d:/Zevaran/prompts/next_question_moving_logic.md)**: Controlled interview state machine and 5-tier question selection priority engine.
- **[adaptive_orchestrator.md](file:///d:/Zevaran/prompts/adaptive_orchestrator.md)**: Real-time recruiter persona and pool selection rules for dynamic 30-minute adaptive interview progression.
- **[post_interview_evaluation_report.md](file:///d:/Zevaran/prompts/post_interview_evaluation_report.md)**: Comprehensive post-interview synthesis prompt producing topic scorecards, JD coverage matrices, and resume verification audits.
- **[main_interview_room_violation_detection.md](file:///d:/Zevaran/prompts/main_interview_room_violation_detection.md)**: Automated proctoring, visual screenshot evidence with highlighted target boxes, dynamic notification bell counter, and 15-violation termination screen specifications.

---

## Core Principles

### 1. Exact 20-Question Preparation Pattern

Before the live interview room becomes ready, Zavran AI generates an internal 20-question pool structured into three distinct sourcing zones:

| Question Range | Primary Source | Core Purpose |
| :--- | :--- | :--- |
| **Questions 1–3** | **Resume** | Deeply verify candidate's projects, technical contributions, and claimed experience. |
| **Questions 4–10** | **Resume + JD** | Test the candidate's resume skills directly against the requirements and constraints of the job description. |
| **Questions 11–20** | **JD** | Evaluate role-specific technical skills, practical scenarios, system design, and problem-solving. |

> **Note**: The 20 questions serve as an **adaptive preparation pool**, not a rigid checklist to exhaust. The AI selects and adapts questions based on candidate depth, uncovered topics, and remaining time in the 30-minute window.

---

### 2. Conceptual Evaluation Flow

For every question in the preparation pool:

$$\text{Question} \longrightarrow \text{Hidden Expected Answer Model} \longrightarrow \text{Candidate Actual Answer} \longrightarrow \text{Covered / Missing / Inaccurate Concepts} \longrightarrow \text{Depth Level Evaluation (1–5)}$$

- **No Pure Keyword Matching**: Evaluation evaluates architectural understanding, trade-off reasoning, and practical engineering nuances.
- **Hidden Rubrics**: Expected answers and evaluation criteria remain strictly internal to the server; candidates only receive the verbatim audio/text question.
- **Evidence-Backed**: Every evaluation point is backed by verbatim transcript citations.
