# Operational Resilience Command Center for Data Center & Critical IT Services

## Overview

The Operational Resilience Command Center is a production-quality MVP designed to demonstrate how critical IT services, business continuity requirements, disaster recovery logic, dependency intelligence, recovery prioritization, and executive reporting can be operationalized into one coherent platform.

This project was built to showcase leadership capability in IT Business Continuity, Disaster Recovery, Operational Resilience, and Critical IT Service Governance for a senior interview panel.

## Problem Statement

In complex enterprise environments, understanding the real-time resilience posture of critical IT services is a significant challenge. Information is often siloed in spreadsheets, static diagrams, and disparate systems. During an incident, this lack of a unified, data-driven view hinders effective decision-making, leading to slower recovery times and increased business impact.

This platform addresses that gap by providing a single source of truth for resilience data and a command center for managing incidents.

## Architecture Summary

The application follows a robust client-server architecture:

-   **Frontend:** A modern, responsive web interface built with Next.js 15, React 19, and TypeScript, styled with Tailwind CSS. It is responsible for all user interaction and data visualization.
-   **Backend:** A high-performance REST API built with FastAPI and Python 3.11+. It handles all business logic, data processing, and database interactions.
-   **Database:** A self-contained SQLite database is used for portability and ease of setup for the MVP, pre-populated with realistic seed data.
-   **API:** A contract-driven RESTful API ensures data integrity between the frontend and backend, using Pydantic for backend validation.

For a more detailed breakdown, see [ARCHITECTURE.md](./docs/ARCHITECTURE.md).

## Features

-   **Executive Dashboard:** At-a-glance insights into service health, risks, and DR exercise outcomes.
-   **Service Registry:** A comprehensive catalog of critical IT services and their continuity posture.
-   **Business Impact Analysis (BIA):** Manages RTO, RPO, and impact data for each service.
-   **Dependency Mapping:** Visualizes the complex relationships between services and infrastructure.
-   **Incident Simulator:** Triggers realistic disruption scenarios to model their impact across the ecosystem.
-   **Recovery Prioritization Engine:** A deterministic, rule-based engine that provides an explainable recovery sequence during an incident.
-   **Runbook Execution Tracker:** Tracks the status of recovery tasks in real-time.
-   **DR Exercise Scorecard:** Documents results and corrective actions from DR tests.
-   **Executive Incident Brief Generator:** Automatically generates concise, shareable incident summaries for leadership.

## Tech Stack

-   **Frontend:** Next.js 15+, React 19, TypeScript, Tailwind CSS
-   **Backend:** FastAPI, Python 3.11+, Uvicorn
-   **Database:** SQLite
-   **API:** REST with Pydantic
-   **Data Visualization:** Recharts
-   **Backend Testing:** Pytest
-   **Code Quality:** Ruff, Black, ESLint, Prettier

## Local Setup

### Prerequisites

-   Python 3.11+
-   Node.js 20+
-   `pnpm` package manager for the frontend (`npm install -g pnpm`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SultanAlbuqami/Operational-Resilience-Command-Center-for-Data-Center-Critical-IT-Services.git
    cd Operational-Resilience-Command-Center-for-Data-Center-Critical-IT-Services
    ```

2.  **Setup the Backend:**
    ```bash
    # Navigate to the backend directory
    cd backend

    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Setup the Frontend:**
    ```bash
    # Navigate to the frontend directory
    cd ../frontend

    # Install dependencies using pnpm
    pnpm install
    ```

## Run Commands

1.  **Run the Backend Server:**
    -   Ensure you are in the `backend` directory with the virtual environment activated.
    -   The application will be available at `http://127.0.0.1:8000`.
    ```bash
    # From the ./backend directory
    uvicorn app.main:app --reload
    ```
    -   The API documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs`.

2.  **Run the Frontend Application:**
    -   Ensure you are in the `frontend` directory.
    -   The application will be available at `http://localhost:3000`.
    ```bash
    # From the ./frontend directory
    pnpm dev
    ```

## Seed the Database

The application includes a command to seed the SQLite database with realistic demo data.

-   Ensure the backend virtual environment is activated.
-   Run the seed script from the project's root `backend` directory:
```bash
# From the ./backend directory
python -m app.db.seed
```
This will create and populate the `app.db` file. It is safe to run this command multiple times; it will clear and re-populate the database each time.

## Test Commands

1.  **Run Backend Tests:**
    ```bash
    # From the ./backend directory
    pytest
    ```

2.  **Run Frontend Linting:**
    ```bash
    # From the ./frontend directory
    pnpm lint
    ```

## Project Structure

```
/
├── backend/            # FastAPI Backend
│   ├── app/            # Core application code
│   │   ├── api/        # API route definitions
│   │   ├── core/       # Configuration
│   │   ├── crud/       # Data Access Layer (Repository)
│   │   ├── db/         # Database setup and seeding
│   │   ├── models/     # SQLAlchemy ORM models
│   │   ├── schemas/    # Pydantic schemas
│   │   └── services/   # Business logic
│   ├── tests/          # Pytest tests
│   └── ...
├── docs/               # Project documentation
│   ├── ARCHITECTURE.md
│   ├── ASSUMPTIONS.md
│   ├── INTERVIEW_DEMO_SCRIPT.md
│   └── ...
├── frontend/           # Next.js Frontend
│   ├── src/
│   │   ├── app/        # Next.js App Router pages
│   │   ├── components/ # Reusable React components
│   │   ├── lib/        # API clients, utils
│   │   └── ...
│   └── ...
└── README.md
```

## Interview Demo Walkthrough

A complete walkthrough script for a 5-7 minute executive demo is available in [INTERVIEW_DEMO_SCRIPT.md](./docs/INTERVIEW_DEMO_SCRIPT.md).

## Authorship

-   **Author:** Eng. Sultan Albuqami
-   **Email:** sultan_mutep@hotmail.com
