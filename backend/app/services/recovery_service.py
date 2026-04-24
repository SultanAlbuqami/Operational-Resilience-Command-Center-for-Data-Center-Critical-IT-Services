from datetime import datetime
from typing import Any, Dict, List

from app.models.service import Service

# --- Weighting Factors ---
W_IMPACT = 2.0
W_TIME = 1.5
W_DEPENDENCY = 1.0
W_RPO = 1.0
W_VENDOR = 1.0
W_DR = 1.0
W_BLOCKAGE = 2.0


def calculate_recovery_scores(
    services: List[Service], incident_start_time: datetime
) -> List[Dict[str, Any]]:
    """
    Calculates a recovery score for each service based on BIA, time pressure,
    and dependencies. Returns a sorted list of services with their scores and the rationale.
    """
    scored_services = []
    now_utc = datetime.now()

    for service in services:
        if service.current_status == "Operational":
            continue

        # 1. Business Criticality & Operational Impact
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

        # 2. Time Pressure Score (Time to RTO breach)
        time_since_outage = (now_utc - incident_start_time).total_seconds() / 60
        mtd_minutes = service.bia.rto_target_hours * 60
        urgency_ratio = (
            min(time_since_outage / mtd_minutes, 1.0) if mtd_minutes > 0 else 1.0
        )

        if urgency_ratio < 0.5:
            time_pressure_score = (urgency_ratio * 100) * 0.5
        else:
            time_pressure_score = 50 + ((urgency_ratio - 0.5) * 100)

        # 3. Dependency Score (Others depending on this service)
        downstream_impact_score = 0
        for dep in service.upstream_dependencies:
            if dep.service.current_status != "Operational":
                downstream_impact_score += {1: 100, 2: 75, 3: 50, 4: 25}.get(
                    dep.service.criticality_tier, 0
                )
        dependency_score = downstream_impact_score / 10

        # 4. Dependency Blockage (This service blocked by others)
        blockage_penalty = 0
        for dep in service.downstream_dependencies:
            if dep.depends_on.current_status != "Operational":
                blockage_penalty += 50  # heavily penalize if blocked
        dependency_blockage_score = -blockage_penalty

        # 5. Backup freshness / RPO exposure
        rpo_exposure_score = 0
        if (
            service.bia.rpo_target_minutes > 0
            and time_since_outage > service.bia.rpo_target_minutes
        ):
            rpo_exposure_score = min(
                (
                    (time_since_outage - service.bia.rpo_target_minutes)
                    / service.bia.rpo_target_minutes
                )
                * 50,
                100,
            )
        else:
            rpo_exposure_score = (
                (time_since_outage / service.bia.rpo_target_minutes) * 20
                if service.bia.rpo_target_minutes > 0
                else 0
            )

        # 6. Vendor Readiness
        vr = getattr(service, "vendor_readiness", "High")
        vendor_readiness_score = {"High": 100, "Medium": 50, "Low": 0}.get(vr, 100)

        # 7. DR Site Readiness
        dr_stat = getattr(service, "dr_site_status", "Ready")
        dr_site_readiness_score = {"Ready": 100, "Degraded": 50, "Offline": 0}.get(
            dr_stat, 100
        )

        # Final Weighted Score
        total_score = (
            (business_impact_score * W_IMPACT)
            + (time_pressure_score * W_TIME)
            + (dependency_score * W_DEPENDENCY)
            + (rpo_exposure_score * W_RPO)
            + (vendor_readiness_score * W_VENDOR)
            + (dr_site_readiness_score * W_DR)
            + (dependency_blockage_score * W_BLOCKAGE)
        )

        scored_services.append(
            {
                "service_id": service.id,
                "name": service.name,
                "total_score": round(max(0, total_score), 2),  # avoid negative score
                "rationale": {
                    "business_impact_score": round(business_impact_score, 2),
                    "time_pressure_score": round(time_pressure_score, 2),
                    "dependency_score": round(dependency_score, 2),
                    "urgency_ratio": round(urgency_ratio, 2),
                    "time_since_outage_minutes": round(time_since_outage, 2),
                    "dependency_blockage_score": round(dependency_blockage_score, 2),
                    "rpo_exposure_score": round(rpo_exposure_score, 2),
                    "vendor_readiness_score": round(vendor_readiness_score, 2),
                    "dr_site_readiness_score": round(dr_site_readiness_score, 2),
                },
            }
        )

    # Sort services by score in descending order
    sorted_list = sorted(scored_services, key=lambda x: x["total_score"], reverse=True)

    # Add recovery_order
    for i, srv in enumerate(sorted_list):
        srv["recovery_order"] = i + 1

    return sorted_list
