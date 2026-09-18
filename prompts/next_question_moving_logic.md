# Zavran AI — Next Question Moving Logic & Conversational Progression Specification

## Core Conversational Principle

The interview must feel like a completely natural, flowing conversation between the candidate and the AI interviewer:

$$\text{AI asks question} \longrightarrow \text{Candidate answers} \longrightarrow \text{AI listens and understands} \longrightarrow \text{Candidate pauses for }\sim 3\text{s} \longrightarrow \text{AI automatically asks next question}$$

* **No Manual Buttons**: Do **not** display or use a **"Submit & Next"** button in the interview UI.
* **No Manual Triggering**: Do **not** require the candidate to click buttons or say voice commands (e.g., "next", "submit", "done").
* **No Linear Dependency**: Do **not** depend on visible question numbers to determine when to move forward.
* **No UI Transcript Clutter**: Do **not** display speech-to-text transcripts in the interview interface. Candidate audio is captured and analyzed purely internally.

---

## 1. Automatic Next Question Logic

1. **Continuous Contextual Listening**:
   - The AI actively listens to the candidate throughout the interview turn.
   - The AI evaluates the **meaning, context, and semantic completeness** of the candidate's speech rather than merely matching isolated keywords.

2. **Pause & Completion Handling**:
   - **0–2 seconds silence**: Treated as a natural thinking pause or mid-sentence contemplation. The AI continues listening attentively.
   - **~3 seconds silence**: When the candidate finishes answering and remains silent for approximately 3 seconds, the system treats the response as complete (`ANSWER_COMPLETE`).
   - **Early Confident Completion**: If the candidate clearly finishes their answer earlier and the engine confidently determines completeness, it may naturally proceed to the next step.

3. **Autonomous Transition**:
   - Immediately following confirmed completion, the AI evaluates the response against expected answer concepts and speaks the acknowledgement and next technical question.

---

## 2. Multi-Modal Body Language & Environmental Evaluation

* **Holistic Observation**:
   - The system continuously observes relevant candidate visual cues: facial orientation, head movement, shoulders framing, posture, gaze direction, and oral zone movement.
* **Contextual Interpretation**:
   - Visual and posture signals are interpreted in context (e.g., glancing at a scratchpad vs. looking away continuously), avoiding brittle false alarms.
* **Unified Evidence Synthesis**:
   - The engine combines **what the candidate says**, **how they behave/present**, and the **overall interview context** into a single evaluation matrix.

---

## 3. Turn-Taking State Machine

```
[ AI_SPEAKING ]
Zaroon speaks question naturally. Dialogue renders synchronously with speech start.
      │
      ▼
[ LISTENING ]
Speech ends. Candidate responds naturally. Audio captured and processed purely internally (NO UI TRANSCRIPT).
      │
      ▼
[ PAUSE / COMPLETION DETECTION ]
├─ 0–2s pause    ──► Continue LISTENING (Thinking pause)
└─ ~3s silence   ──► ANSWER_COMPLETE confirmed automatically (NO SUBMIT BUTTON)
      │
      ▼
[ CONCEPTUAL EVALUATION ]
Hidden evaluation against expected concepts, depth rubrics (Levels 1–5), and multi-modal signals.
      │
      ▼
[ NEXT_QUESTION_SELECTION ]
Orchestrator evaluates competencies and dynamically selects the next technical dimension:
      ├─ Follow-up probe on edge case / ambiguity
      ├─ Next competency question from prepared pool
      └─ Session completion when time / coverage is reached
```

---

## 4. Final Submission & 10-Minute Verification

When all competencies are covered or the session concludes:
1. Zaroon speaks the formal closing notice:
   > *"Thank you for completing your technical interview with Zavran AI. Your responses have been recorded and submitted. Our evaluation engine is now performing a deep, rigorous verification against the job requirements. Your detailed evaluation report and answer review will be ready in your candidate dashboard and sent to your registered email in approximately 10 minutes."*
2. The UI transitions to the **10-Minute In-Depth Technical Verification** status screen. No fake instant scores are presented.
