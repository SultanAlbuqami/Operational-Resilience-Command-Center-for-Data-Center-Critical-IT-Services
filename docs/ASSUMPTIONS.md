# Assumptions Log

This document lists the key assumptions made during the development of the Operational Resilience Command Center MVP. These decisions were made to ensure rapid progress and focus on the core features required for the interview demo, without needing to stop for clarification.

## 1. Technical & Architectural Assumptions

-   **Target Environment:** Assumed to be a local machine for a single-user demo. No considerations were made for multi-user, high-availability, or cloud-native deployment.
-   **Authentication & Authorization:** Deliberately omitted. The application is treated as an internal tool where the user has full administrative access. This simplifies the demo flow significantly.
-   **Python & Node.js Availability:** Assumed that Python 3.11+ and Node.js 20+ are installed and available in the host environment's PATH.
-   **Database Choice:** SQLite was chosen for its zero-configuration, file-based nature, making the project self-contained and easy to run. It is not intended for production use. The database schema is assumed to be managed via the application's own startup/seeding logic, not with a formal migration tool like Alembic.
-   **Static Dependency Data:** The dependency mapping is based on the seed data. It is not discovered automatically via network scanning or CMDB integration, which would be a feature of a more mature system.
-   **Error Handling:** Focus is on graceful handling of expected scenarios for the demo. Edge-case error handling that would be critical for a production system is not exhaustively implemented.

## 2. Product & Feature Assumptions

-   **Service Criticality Tiers:** A simple 1-4 tiering system is assumed to be sufficient (Tier 1 = most critical). The business impact associated with each tier is pre-defined in the seed data.
-   **Recovery Scoring Model:** The scoring model is a deterministic, weighted algorithm. The weights and factors are chosen based on common industry best practices but are a simplified representation of a true, enterprise-specific model. The goal is to demonstrate the *concept* of explainable prioritization.
-   **Incident Scenarios:** The available incident scenarios are pre-scripted and finite. The "blast radius" of each scenario is hard-coded into the simulation logic for demo purposes.
-   **Runbook Content:** Runbooks are represented as a list of tasks. The MVP does not include capabilities for automated script execution or deep integration with other systems for task validation. Status updates are manual.
-   **Executive Brief Content:** The content for the executive brief is algorithmically generated based on the incident's impact data. The tone and structure are designed to be concise and suitable for a leadership audience, but the narrative is template-based.
-   **Data Freshness:** All data is as fresh as the last time the seed script was run or the last user action was taken. There is no background data synchronization or real-time monitoring integration.

## 3. Demo & UX Assumptions

-   **Single-Screen Demo:** The user experience is optimized for a single-screen presentation. It assumes the user is navigating through the pre-defined demo script path.
-   **Data Realism:** The seed data (service names, impacts, dependencies) is designed to be realistic and credible for a typical enterprise but is entirely fictional.
-   **Instantaneous Actions:** All actions (e.g., running a simulation) are assumed to complete nearly instantaneously to maintain a smooth demo flow. No long-running background jobs with complex progress tracking are implemented.

These assumptions enabled the focused delivery of a feature-complete MVP that effectively communicates the project's core value proposition within the constraints of an interview demonstration.
