from datetime import datetime, timezone
from typing import Any, Dict, List

from app.models.service import Service

# --- Weighting Factors ---
W_IMPACT = 2.0
W_TIME = 1.5
W_DEPENDENCY = 1.0


def calculate_recovery_scores(
    services: List[Service], incident_start_time: datetime
) -> List[Dict[str, Any]]:
    """
    Calculates a recovery score for each service based on BIA, time pressure,
    and dependencies. Returns a sorted list of services with their scores and the rationale.
    """
    scored_services = []
    now_utc = datetime.now(timezone.utc)

    for service in services:
        if service.current_status == "Operational":
            continue

        # 1. Business Impact Score
        tier_score = {1: 100, 2: 75, 3: 50, 4: 25}.get(service.criticality_tier, 0)

        financial_multiplier = 1.2 if service.bia.financial_impact == "High" else 1.0
        regulatory_multiplier = 1.2 if service.bia.regulatory_impact == "High" else 1.0
        reputational_multiplier = (
            1.1 if service.bia.reputational_impact == "High" else 1.0
        )

        business_impact_score = (
            tier_score
            * financial_multiplier
            * regulatory_multiplier
            * reputational_multiplier
        )

        # 2. Time Pressure Score
        time_since_outage = (now_utc - incident_start_time).total_seconds() / 60
        mtd_minutes = service.bia.rto_target_hours * 60
        urgency_ratio = (
            min(time_since_outage / mtd_minutes, 1.0) if mtd_minutes > 0 else 1.0
        )

        if urgency_ratio < 0.5:
            time_pressure_score = (urgency_ratio * 100) * 0.5
        else:
            time_pressure_score = 50 + ((urgency_ratio - 0.5) * 100)

        # 3. Dependency Score
        downstream_impact_score = 0
        for dep in service.upstream_dependencies:
            if dep.service.current_status != "Operational":
                # Simple sum of tier scores of dependent services
                downstream_impact_score += {1: 100, 2: 75, 3: 50, 4: 25}.get(
                    dep.service.criticality_tier, 0
                )

        dependency_score = downstream_impact_score / 10

        # Final Weighted Score
        total_score = (
            (business_impact_score * W_IMPACT)
            + (time_pressure_score * W_TIME)
            + (dependency_score * W_DEPENDENCY)
        )

        scored_services.append(
            {
                "service_id": service.id,
                "name": service.name,
                "total_score": round(total_score, 2),
                "rationale": {
                    "business_impact_score": round(business_impact_score, 2),
                    "time_pressure_score": round(time_pressure_score, 2),
                    "dependency_score": round(dependency_score, 2),
                    "urgency_ratio": round(urgency_ratio, 2),
                    "time_since_outage_minutes": round(time_since_outage, 2),
                },
            }
        )

    # Sort services by score in descending order
    return sorted(scored_services, key=lambda x: x["total_score"], reverse=True)
