# Operational Resilience Command Center: System Architecture

## 1. System Overview

The Operational Resilience Command Center is a full-stack web application designed to provide a centralized platform for managing and visualizing the resilience posture of critical IT services. It follows a classic, robust, and scalable client-server architecture.

-   **Frontend (Client):** A modern, responsive web interface built with Next.js and React. It is responsible for all user interaction, data visualization, and communication with the backend.
-   **Backend (Server):** A powerful REST API built with FastAPI (Python). It handles all business logic, data processing, database interactions, and the execution of resilience-specific engines (e.g., scoring, simulation).
-   **Database:** A self-contained SQLite database for portability and ease of setup for the MVP. It stores all application data, from service catalogs to incident reports.
-   **API:** A contract-driven RESTful API using typed request/response models (Pydantic for the backend, Zod for the frontend) ensures data integrity and consistency between the frontend and backend.

This separation of concerns allows for independent development, scaling, and maintenance of the frontend and backend components.

## 2. Frontend Architecture

The frontend is a single-page application (SPA) built on Next.js 15 and React 19, leveraging server-side rendering (SSR) for fast initial page loads and improved SEO where applicable.

-   **Framework:** Next.js (App Router)
-   **Language:** TypeScript
-   **UI Library:** React 19
-   **Styling:** Tailwind CSS for a utility-first styling approach, enabling rapid development of a clean, executive-grade UI.
-   **State Management:** React Context API and `useState`/`useReducer` hooks for managing local and global application state. For a project of this scale, this avoids introducing external libraries unless absolutely necessary.
-   **Data Fetching & Caching:** A dedicated API client module using `fetch` to interact with the backend REST API.
-   **Validation:** Zod for runtime validation of API responses and form inputs, ensuring type safety.
-   **Component Structure:** A modular structure with clear separation between pages, reusable components, layouts, and API services.
-   **Quality:** ESLint and Prettier for maintaining code quality and consistency.

## 3. Backend Architecture

The backend is a high-performance asynchronous API powered by Python 3.11 and the FastAPI framework.

-   **Framework:** FastAPI
-   **Language:** Python 3.11+
-   **Asynchronous Processing:** Built on Starlette and Uvicorn, FastAPI provides a fully asynchronous request-handling pipeline, ideal for I/O-bound operations like database queries and API calls.
-   **Domain Model:**
    -   **Pydantic Models:** Used for request/response validation, serialization, and defining clear data contracts for the API.
    -   **SQLAlchemy ORM:** Used to define the database schema and interact with the SQLite database. A repository pattern is used to abstract database logic from the business services.
-   **Database:** SQLite, chosen for its simplicity and file-based nature, is perfect for a self-contained MVP. The application is designed to easily swap this out for a more robust production database like PostgreSQL if needed.
-   **Layers:**
    1.  **API/Routes:** The entry point for all HTTP requests. Handles request validation (via Pydantic) and calls the appropriate service.
    2.  **Services:** Contains the core business logic (e.g., running simulations, calculating recovery scores). It orchestrates calls to the data/repository layer.
    3.  **Repository:** The data access layer (DAL). It encapsulates all direct database interactions (CRUD operations) using SQLAlchemy, keeping the rest of the application agnostic to the database implementation.
    4.  **Database Models:** SQLAlchemy models that define the database tables and their relationships.
-   **Quality:** Ruff and Black for linting and code formatting, ensuring a high standard of Python code.
-   **Testing:** A comprehensive test suite using `pytest` to cover domain models, services, and API endpoints.

## 4. API Structure

The API is designed to be RESTful, resource-oriented, and self-documenting (via FastAPI's OpenAPI/Swagger integration).

-   **Base URL:** `/api/v1`
-   **Authentication:** Not implemented for the MVP to simplify the demo, but the architecture allows for easy integration of OAuth2 or token-based authentication.
-   **Core Endpoints:**
    -   `/services`: CRUD operations for the Service Registry.
    -   `/bia`: Access Business Impact Analysis data for services.
    -   `/dependencies`: Manage and visualize service dependencies.
    -   `/incidents`: Trigger simulations and view incident impact.
    -   `/recovery/prioritization`: Get recovery scoring and ordering.
    -   `/runbooks`: Track runbook execution status.
    -   `/dr-exercises`: Manage DR exercise scorecards.
    -   `/reports/executive-brief`: Generate executive-level incident summaries.
    -   `/dashboard`: Provide aggregated data for the main dashboard.

## 5. Recovery Scoring Design

The Recovery Prioritization Engine is a deterministic, rule-based model implemented in the backend. It is designed for transparency and explainability, avoiding any "black box" logic.

-   **Input:** The engine takes the current state of all services, their BIA data, and dependencies as input.
-   **Logic:** It calculates a numerical score for each impacted service based on a weighted formula. The `RECOVERY_SCORING_LOGIC.md` document contains the detailed breakdown of the scoring algorithm.
-   **Output:** A ranked list of services in their recommended recovery order, along with the score and the rationale for that score. The rationale explains which factors contributed most significantly to the service's position.

## 6. Data Flow for Incident Simulation

1.  **User Action:** The user triggers an incident scenario from the frontend UI (e.g., "Data Center Power Failure").
2.  **API Request:** The frontend sends a POST request to the `/api/v1/incidents` endpoint with the scenario ID.
3.  **Backend Simulation:**
    -   The backend's Incident Simulator service identifies all components and services directly affected by the scenario (e.g., all services in the primary data center).
    -   It traverses the dependency graph to determine the full "blast radius" of downstream impacted services.
    -   The status of all affected services is updated in the database to reflect the impact (e.g., "Offline," "Degraded").
4.  **Recovery Prioritization:** The Recovery Prioritization Engine is automatically invoked to score and rank all impacted services.
5.  **API Response:** The backend returns the results of the simulation, including the list of impacted services and their recovery priority.
6.  **Frontend Visualization:** The frontend receives the data and updates the UI in real-time to show the impact, new service statuses, and the prioritized recovery list.

## 7. Assumptions & Tradeoffs

-   **Single Tenancy:** The system is designed for a single organization and does not include multi-tenant data isolation.
-   **Simplified Auth:** Authentication and authorization are omitted for MVP simplicity. In a real-world scenario, this would be a critical addition.
-   **SQLite for MVP:** SQLite is used for ease of setup. It is not suitable for a large-scale, multi-user production environment where a client-server database like PostgreSQL would be required.
-   **Real-time is Simulated:** "Real-time" updates are based on user-triggered actions and subsequent API calls, not WebSockets, which would be an enhancement for a more dynamic experience.

## 8. Future Enhancements

-   **Authentication & RBAC:** Implement OAuth2 and Role-Based Access Control to secure the platform.
-   **Live Monitoring Integration:** Integrate with monitoring tools (e.g., Prometheus, Datadog) to reflect the real-time status of services automatically.
-   **CI/CD Automation:** Build a full CI/CD pipeline for automated testing and deployment.
-   **WebSocket Notifications:** Add WebSockets for real-time notifications and updates without needing to refresh the UI.
-   **Production Database:** Migrate from SQLite to a production-grade database like PostgreSQL.
-   **Advanced Visualizations:** Introduce more complex and interactive dependency graphs and charts.
