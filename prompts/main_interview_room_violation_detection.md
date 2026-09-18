# Main Interview Room — Violation Detection Requirements

In the main interview room, the system continuously monitors the candidate for predefined interview violations.

---

## 1. Violation Detection

Whenever a violation is detected, the system automatically:

* Records the violation.
* Captures a screenshot of the candidate/video frame at the moment of the violation.
* Clearly highlights or marks the detected area in the screenshot.
* Adds a notification to the **notification bell icon**.
* Increments the violation count automatically: **1, 2, 3, 4... up to 15**.
* Displays a clear message explaining exactly what violation was detected.

The candidate is **not required to press any button** to report, submit, or process a violation.

---

## 2. Examples of Violations

The system detects violations such as:

* Candidate's face is not visible.
* Candidate leaves the camera frame.
* Candidate intentionally hides their face.
* Camera is turned off or video is unavailable.
* Microphone is muted when audio is required.
* Candidate's audio is not audible.
* Poor or insufficient lighting makes the candidate's face difficult to identify.
* Candidate exits fullscreen mode.
* Candidate attempts to copy or paste restricted content.
* Candidate attempts to take a screenshot or use restricted screen-capture functionality.
* Candidate presses restricted buttons or performs prohibited actions.
* A mobile phone or other unauthorized object is detected in the candidate's hands.
* Any other predefined interview-security violation.

---

## 3. Screenshot Evidence

For every visual violation, the system automatically captures a screenshot.

For example, if the candidate moves away from the camera:

* Capture the current video frame.
* Mark the relevant area where the candidate's face is missing.
* Display the evidence in the violation record.
* Show a message such as **"Your face is not visible"** or **"You have left the camera frame."**

If a mobile phone or another unauthorized object is detected:

* Capture the frame.
* Highlight the detected object with a visual bounding box or marker.
* Clearly identify the violation.
* Store the screenshot as evidence.

The same approach is used for other detectable visual violations.

---

## 4. Temporary Violation Notifications

Violation notifications are dynamic:

1. The candidate moves away from the camera.
2. The system detects that the face is no longer visible.
3. A violation notification appears.
4. A screenshot is captured and displayed as evidence.
5. The violation count increases.
6. The candidate returns to the correct position.
7. Their face becomes clearly visible again.
8. The active warning for that condition automatically disappears once the violation condition is resolved.

The interface distinguishes between:

* **Currently active violations**, and
* **Historical violation records/counts**.

The resolved warning disappears from the active notification area, while the violation event remains recorded in the interview's violation history.

---

## 5. Violation Notification Bell

The notification bell automatically displays the current violation count:

$$\text{Violation 1} \longrightarrow \text{Violation 2} \longrightarrow \text{Violation 3} \longrightarrow \dots \longrightarrow \text{Violation 15}$$

The notification system updates automatically without requiring the candidate to interact with it.

Each notification contains:

* Violation type.
* Short explanation.
* Timestamp.
* Screenshot evidence when applicable.
* Highlighted detection area when applicable.

---

## 6. Maximum Violation Limit

The candidate can accumulate a maximum of **15 violations**.

When the violation count reaches **15**, the system automatically terminates the interview.

The candidate does not have to press a button to terminate it.

The system displays a termination screen stating that the interview has been terminated by the selected AI recruiter.

---

## 7. Interview Termination Screen

After the 15th violation, a clean, professional termination screen is displayed with a **full white background**.

The layout contains:

* **Zavran AI logo and branding on the left side.**
* A clear termination message:
  > **"Your interview has been terminated by {Interviewer Name} AI."**
* An explanation below:
  > **"We noticed multiple violations during your interview. The maximum allowed violation limit has been reached."**
* A section explaining that violations were detected.
* A visual history of the detected violations.
* Evidence screenshots for the recorded violations.

---

## 8. Violation Evidence Cards

Below the termination message, a card-based violation history is displayed using a grid containing **4 cards per row**, with multiple rows as required.

Each card contains:

* Screenshot of the violation.
* Highlighted/marked detection area.
* Violation type.
* Short explanation.
* Violation number.
* Timestamp.

---

## 9. Restricted Candidate Actions

The candidate cannot bypass interview-security mechanisms by interacting with restricted controls.

Whenever a restricted action is detected:

1. Detect the action.
2. Record the violation.
3. Capture evidence when technically possible.
4. Highlight the relevant area when visual detection is involved.
5. Update the violation count.
6. Display the notification automatically.

---

## 10. Rejoin and End Interview Buttons

After termination, two clear options are provided:

* **Rejoin Interview**: Allows the candidate to rejoin the interview according to application security rules.
* **End Interview**: Allows the candidate to permanently leave the interview.

These buttons are only available on the termination/recovery screen and do not allow bypassing the violation-counting or security logic.

---

## 11. Temporary Violation Evidence (Session-Only Lifecycle)

The violation screenshots, highlighted evidence, violation messages, and violation cards **do not need to be permanently stored in the database**.

After the interview is terminated due to reaching 15 violations:

* Temporarily display the detected violations and their screenshots on the termination screen.
* Show the violation count and evidence only for the current interview session.
* Keep the evidence available while the termination screen is open.
* When the candidate clicks **"Rejoin Interview"** or **"End Interview"**, the temporary violation evidence, screenshots, notifications, and related UI state are cleared.
* After rejoining or ending the call, previous violation evidence disappears completely from the interface.
* Screenshots or temporary violation records are not retained in the database after the session ends.
