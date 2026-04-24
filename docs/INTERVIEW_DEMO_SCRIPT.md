# Interview Demo Script: Operational Resilience Command Center

**Presenter:** (You, the candidate)
**Audience:** Senior Interview Panel
**Time:** 5-7 Minutes

---

### Introduction (30 seconds)

"Good morning. I built this prototype, the 'Operational Resilience Command Center,' to demonstrate how we can operationalize business continuity, dependency intelligence, and incident management into a single, coherent platform. It’s designed to give leaders a real-time, data-driven view of our resilience posture and to enable faster, smarter decisions during a crisis."

"Let's start at the **Executive Dashboard**, which is what a leader would see on a day-to-day basis."

---

### 1. The "Peace Time" View: The Dashboard (60 seconds)

**(Action: Have the main dashboard page open)**

"This dashboard provides an at-a-glance summary of our critical service landscape. We can see key metrics like the **total number of critical services** we're tracking and, more importantly, how many are currently **at risk** due to known issues."

"It also highlights proactive indicators, such as **upcoming RTO breaches** for services that are currently down, the results of our **latest DR exercises**, and our overall **vendor readiness posture**."

"This view allows us to move from a reactive to a proactive stance on resilience. For example, we can drill into the 'Services at Risk' to understand which dependencies are fragile before they cause an incident."

**(Action: Briefly hover over a chart or two to show interactivity if available.)**

---

### 2. The "Crisis" View: Simulating an Incident (90 seconds)

"Now, let's see what happens when a disruption occurs. I'm going to use the **Incident Simulator** to trigger a realistic scenario: a **total power failure at our primary data center**."

**(Action: Navigate to the Incident Simulator page. Select the 'Primary Data Center Power Failure' scenario and click 'Trigger Incident'.)**

"Immediately, the system calculates the blast radius. The dashboard and service views are updated in real-time. As you can see, multiple services are now marked as 'Offline' or 'Degraded'."

**(Action: Navigate back to the main service list or dashboard, which should now show the impact.)**

"But simply knowing what's down isn't enough. The critical question is: **what do we recover first?**"

"This is where the **Recovery Prioritization Engine** comes in. The system has already analyzed all impacted services."

**(Action: Navigate to the 'Recovery Prioritization' page.)**

"Here, we see a ranked list of services in the exact order we should recover them. This isn't a guess; it's the output of a deterministic scoring model based on business criticality, RTO targets, and dependency blockages. For each service, like the 'Customer Identity Platform,' we can see the **exact rationale** for its score, ensuring the logic is transparent and defensible."

---

### 3. The "Response" View: Tracking Recovery (60 seconds)

"Once we have our plan, execution is key. Let's look at the top-priority service, the 'Customer Identity Platform'."

**(Action: Click on the 'Customer Identity Platform' to navigate to its details or a runbook view.)**

"The **Runbook Execution Tracker** gives us the step-by-step recovery plan. Each task is clearly defined with an owner, an ETA, and its current status."

"As the recovery teams work, they can update the status of each task. For example, when the 'Verify Database Connectivity' step is completed, they mark it as 'Done'."

**(Action: Change the status of one or two tasks from 'Not Started' to 'In Progress' or 'Completed'.)**

"This provides leadership with a clear, real-time view of our recovery progress against our timeline."

---

### 4. The "Governance" View: Learning and Improving (45 seconds)

"Of course, resilience isn't just about responding to incidents; it's about continuously improving. The platform includes a **DR Exercise Scorecard**."

**(Action: Navigate to the DR Exercise Scorecard page.)**

"Here, we track the results of all our disaster recovery tests. We can see the scenario tested, whether we met our target RTO and RPO, and, most importantly, the **lessons learned** and **corrective actions** assigned. This creates a closed-loop system for improvement, ensuring we're always getting better."

---

### 5. The "Communication" View: The Executive Brief (30 seconds)

"Finally, in a real incident, clear communication is critical. The platform can instantly generate a concise **Executive Incident Brief**."

**(Action: Navigate to the reporting section and generate the brief for the simulated incident.)**

"This report summarizes the incident, lists the top business impacts, presents the recommended recovery plan, and highlights key risks. It’s designed to be immediately shareable with the executive team, ensuring everyone has consistent, accurate information."

---

### Conclusion (15 seconds)

"In summary, this platform integrates the key pillars of operational resilience—from proactive analysis to crisis management and governance—into a single, data-driven command center. Thank you."
