# Seed Data Design

The seed data is designed to create a realistic and compelling ecosystem of services, dependencies, and operational metrics to make the MVP demo credible. The data populates all modules of the application.

## 1. Guiding Principles

-   **Credibility:** Service names, descriptions, and metrics should reflect a plausible enterprise environment.
-   **Interconnectivity:** Create a rich web of dependencies to showcase the power of the dependency mapping and incident simulation features.
-   **Variety:** Use a mix of criticality tiers, RTO/RPO values, and readiness postures to create a non-uniform landscape with interesting risks.
-   **Demo-driven:** Ensure the data directly supports the key talking points in the `INTERVIEW_DEMO_SCRIPT.md`.

## 2. Core Entities

### a. Services (10-15 total)

A mix of customer-facing, business-supporting, and foundational IT services.

| Service Name                 | Owner                  | Business Unit   | Criticality | RTO    | RPO    | Status      | Posture  |
| ---------------------------- | ---------------------- | --------------- | ----------- | ------ | ------ | ----------- | -------- |
| **Customer Identity Platform** | Identity Team          | Digital         | 1           | 1 hr   | 5 mins | Operational | Healthy  |
| **Billing Core**             | Finance Tech           | Finance         | 1           | 4 hrs  | 15 mins| Operational | Healthy  |
| **CRM Platform**             | Sales Operations       | Sales           | 2           | 8 hrs  | 1 hr   | Operational | At Risk  |
| **Customer Digital Channels**| Digital Products       | Marketing       | 1           | 2 hrs  | 30 mins| Operational | Healthy  |
| **Enterprise Backup Platform** | IT Operations          | Technology      | 2           | 24 hrs | 1 hr   | Operational | Degraded |
| **Virtualization Cluster A** | Infrastructure         | Technology      | 1           | 4 hrs  | 0 (HA) | Operational | Healthy  |
| **Storage Array X**          | Infrastructure         | Technology      | 1           | 4 hrs  | 0 (HA) | Operational | Healthy  |
| **Core DNS Service**         | Network Team           | Technology      | 1           | 30 mins| 5 mins | Operational | Healthy  |
| **Primary DC WAN**           | Network Team           | Technology      | 1           | 2 hrs  | N/A    | Operational | Healthy  |
| **Facilities Power & Cooling**| Facilities             | Operations      | 1           | N/A    | N/A    | Operational | Healthy  |
| **Vendor Payments Gateway**  | Finance Tech           | Finance         | 2           | 12 hrs | 1 hr   | Operational | Healthy  |

-   **Posture Rationale:**
    -   `CRM Platform` is 'At Risk' because it depends on a legacy database not configured for DR.
    -   `Enterprise Backup Platform` is 'Degraded' because recent backup jobs have a high failure rate.

### b. Dependencies

Create a dependency graph that tells a story.

-   **Customer Digital Channels** depends on:
    -   `Customer Identity Platform` (for login)
    -   `CRM Platform` (for user data)
-   **Billing Core** depends on:
    -   `CRM Platform` (for account info)
    -   `Vendor Payments Gateway`
-   **CRM Platform** depends on:
    -   `Customer Identity Platform`
    -   `Storage Array X`
    -   `Virtualization Cluster A`
-   **Customer Identity Platform** depends on:
    -   `Core DNS Service`
    -   `Storage Array X`
    -   `Virtualization Cluster A`
-   **All application services** depend on:
    -   `Primary DC WAN`
    -   `Virtualization Cluster A`
    -   `Core DNS Service`
-   **Virtualization Cluster A** depends on:
    -   `Storage Array X`
    -   `Facilities Power & Cooling`

### c. Incident Scenarios (3-5 total)

Scenarios should have a clear "blast radius" defined by the dependency graph.

1.  **Primary Data Center Power Failure:**
    -   **Direct Impact:** `Facilities Power & Cooling`.
    -   **Cascading Impact:** All services hosted in the primary DC, including `Virtualization Cluster A`, `Storage Array X`, and therefore almost every application.
2.  **Ransomware on Virtualization Cluster:**
    -   **Direct Impact:** `Virtualization Cluster A`.
    -   **Cascading Impact:** All VMs and the services they host (`CRM`, `Billing`, `Identity`, etc.).
3.  **Core DNS Service Unavailability:**
    -   **Direct Impact:** `Core DNS Service`.
    -   **Cascading Impact:** Nearly all services that rely on hostname resolution, which is most of them.
4.  **Backup Corruption Detected:**
    -   **Direct Impact:** `Enterprise Backup Platform`.
    -   **Cascading Impact:** Does not cause an immediate outage, but changes the `Continuity Posture` of all services to 'At Risk' because their RPO can no longer be met.

### d. DR Exercises (2-3 total)

Show a history of testing with varied results.

1.  **Scenario:** Billing Core DR Failover Test
    -   **Date:** Last Quarter
    -   **Target RTO/RPO:** 4 hrs / 15 mins
    -   **Actual RTO/RPO:** 3.5 hrs / 12 mins
    -   **Result:** Pass
    -   **Issues:** Minor delays in DNS propagation.
    -   **Corrective Action:** Automate DNS updates via script. Owner: Network Team.
2.  **Scenario:** Full Data Center Failover Simulation (Tabletop)
    -   **Date:** Last Month
    -   **Target RTO/RPO:** 4 hrs (for Tier 1s) / 15 mins
    -   **Actual RTO/RPO:** 6 hrs (projected) / 25 mins (projected)
    -   **Result:** Fail
    -   **Issues:** Dependency mapping for `CRM Platform` was inaccurate, leading to an incorrect recovery sequence. Runbook for storage failover was outdated.
    -   **Corrective Action:** Update CRM dependencies in the Command Center. Revise storage runbook. Owner: IT Operations.

This seed data provides a rich, interconnected dataset that will make the application feel alive and demonstrate its full capabilities during the interview demo.
