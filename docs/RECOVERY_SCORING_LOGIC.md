# Recovery Prioritization Engine: Scoring Logic

The Recovery Prioritization Engine uses a deterministic, weighted scoring model to rank impacted services for recovery. The goal is to provide a transparent, explainable, and consistent recovery sequence during an incident. The principle is: **higher score = higher priority**.

The total score for a service is the sum of several weighted factors:

**Total Score** = (Business Impact Score * `W_impact`) + (Time Pressure Score * `W_time`) + (Dependency Score * `W_dependency`)

---

## 1. Component Scores

### a. Business Impact Score (Range: 0-100)

This score reflects the intrinsic importance of the service to the business. It is derived directly from the Business Impact Analysis (BIA) data.

-   **Criticality Tier:** Services are mapped to a score based on their tier.
    -   Tier 1 (Most Critical): 100 points
    -   Tier 2: 75 points
    -   Tier 3: 50 points
    -   Tier 4 (Least Critical): 25 points
-   **Financial Impact:** A multiplier is applied if the financial impact is high (e.g., >$1M/hr). For the MVP, this is a binary factor: `1.2x` multiplier if `financial_impact` is 'High', `1.0x` otherwise.
-   **Regulatory Impact:** `1.2x` multiplier if `regulatory_impact` is 'High'.
-   **Reputational Impact:** `1.1x` multiplier if `reputational_impact` is 'High'.

**Formula:**
`Business Impact Score = Tier_Score * Financial_Multiplier * Regulatory_Multiplier * Reputational_Multiplier`

### b. Time Pressure Score (Range: 0-100)

This score reflects the urgency of recovering a service based on its Recovery Time Objective (RTO). It increases as the service gets closer to breaching its RTO.

-   **Time Since Outage (TSO):** The duration the service has been down.
-   **Maximum Tolerable Downtime (MTD):** The RTO for the service.
-   **Urgency Ratio:** `(TSO / MTD)`. This value is capped at `1.0`.

A curve is applied to make the score grow exponentially as TSO approaches MTD.

-   If `Urgency Ratio` < 0.5: Score = `(Urgency Ratio * 100) * 0.5`  *(Linear growth initially)*
-   If `Urgency Ratio` >= 0.5: Score = `50 + ((Urgency Ratio - 0.5) * 100)` *(Accelerated growth as breach nears)*

**Example:**
A service with a 4-hour RTO (MTD=240 mins) that has been down for 3 hours (TSO=180 mins):
-   `Urgency Ratio` = 180 / 240 = 0.75
-   `Time Pressure Score` = 50 + ((0.75 - 0.5) * 100) = 50 + 25 = 75

### c. Dependency Score (Range: 0-100)

This score reflects a service's importance as a dependency for *other* services. A service that blocks the recovery of many other critical services should be prioritized.

-   **Impacted Downstream Services (IDS):** The set of other impacted services that depend on this service.
-   **Downstream Business Impact (DBI):** The sum of the `Business Impact Score` for all services in IDS.

The Dependency Score is a fraction of the total downstream impact this service is blocking.

**Formula:**
`Dependency Score = (Sum of Business_Impact_Score for all direct downstream services) / 10`

This ensures that foundational services (like Identity or DNS), which have high DBI, are prioritized.

---

## 2. Weighting Factors

The component scores are multiplied by weights to reflect their relative importance in the final calculation. These weights are configurable constants in the system. For the MVP, they are defined as:

-   `W_impact` = **2.0** (Business Impact is the most important factor)
-   `W_time`` = **1.5** (Time pressure is the second most important driver)
-   `W_dependency` = **1.0** (Dependency impact is a significant but secondary consideration)

## 3. Final Calculation Example

Let's calculate the final score for the "Customer Identity Platform" during an incident.

**Assumptions:**
-   **BIA:** Tier 1, High Financial Impact, High Regulatory Impact.
-   **Timeliness:** RTO is 1 hour. It has been down for 45 minutes.
-   **Dependencies:** It blocks "CRM Platform" (Tier 2) and "Customer Digital Channels" (Tier 1).

**Component Score Calculation:**
1.  **Business Impact Score:**
    -   Tier Score = 100
    -   Multipliers: 1.2 (Financial), 1.2 (Regulatory)
    -   Score = `100 * 1.2 * 1.2` = **144**

2.  **Time Pressure Score:**
    -   Urgency Ratio = 45 / 60 = 0.75
    -   Score = `50 + ((0.75 - 0.5) * 100)` = **75**

3.  **Dependency Score:**
    -   Downstream service "CRM Platform" (Tier 2) has a Business Impact Score of `75`.
    -   Downstream service "Customer Digital Channels" (Tier 1) has a Business Impact Score of `100`.
    -   Score = `(75 + 100) / 10` = **17.5**

**Final Weighted Score:**
-   **Total Score** = (`144 * 2.0`) + (`75 * 1.5`) + (`17.5 * 1.0`)
-   **Total Score** = `288 + 112.5 + 17.5` = **418**

This final score is then compared to the scores of all other impacted services to determine the final recovery prioritization.
