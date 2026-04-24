from typing import List, Set

from sqlalchemy.orm import Session

from app import crud, models, schemas


def get_affected_services_by_scenario(
    db: Session, scenario_name: str
) -> List[models.Service]:
    """
    Identify all services impacted by a given incident scenario.
    This is the core of the "blast radius" calculation.
    """
    initial_impact: List[models.Service] = []

    if scenario_name == "Primary Data Center Power Failure":
        initial_impact = (
            db.query(models.Service)
            .filter(models.Service.primary_site == "us-east-1")
            .all()
        )
    elif scenario_name == "Ransomware on Virtualization Cluster":
        cluster = (
            db.query(models.Service)
            .filter(models.Service.name.like("%Virtualization%"))
            .first()
        )
        if cluster:
            initial_impact.append(cluster)
            for dep in cluster.upstream_dependencies:
                initial_impact.append(dep.service)
    elif scenario_name == "WAN Outage between Primary and DR Site":
        dr_services = (
            db.query(models.Service)
            .filter(models.Service.name.like("%Replication%"))
            .all()
        )
        initial_impact.extend(dr_services)
    elif scenario_name == "Cooling Failure":
        facility = (
            db.query(models.Service)
            .filter(models.Service.name.like("%Cooling%"))
            .first()
        )
        if facility:
            initial_impact.append(facility)
            # Find heavy compute services
            heavy = (
                db.query(models.Service)
                .filter(
                    models.Service.name.in_(["Virtualization Cluster", "Storage Array"])
                )
                .all()
            )
            initial_impact.extend(heavy)
    elif scenario_name == "Backup Corruption":
        backup = (
            db.query(models.Service)
            .filter(models.Service.name.like("%Backup%"))
            .first()
        )
        if backup:
            initial_impact.append(backup)
    elif scenario_name == "Identity Platform Outage":
        iam = (
            db.query(models.Service)
            .filter(models.Service.name.like("%Identity%"))
            .first()
        )
        if iam:
            initial_impact.append(iam)
    elif scenario_name == "Core DNS Service Unavailability":
        dns = db.query(models.Service).filter(models.Service.name.like("%DNS%")).first()
        if dns:
            initial_impact.append(dns)
    else:
        # Fallback to name search or everything if "All" is in it
        all_services = db.query(models.Service).all()
        if "All" in scenario_name:
            return all_services
        return []

    # Traverse the dependency graph to find all downstream services
    affected_services: Set[models.Service] = set(initial_impact)
    queue: List[models.Service] = list(initial_impact)

    while queue:
        current_service = queue.pop(0)
        for dependency in current_service.upstream_dependencies:
            if dependency.service not in affected_services:
                affected_services.add(dependency.service)
                queue.append(dependency.service)

    return list(affected_services)


def trigger_incident(
    db: Session, scenario_name: str, description: str
) -> models.Incident:
    """
    Triggers an incident simulation.
    """
    affected_services = get_affected_services_by_scenario(db, scenario_name)
    if not affected_services:
        return None

    incident = crud.incident.create(
        db, obj_in=schemas.IncidentCreate(name=scenario_name, description=description)
    )

    for service in affected_services:
        service.current_status = "Offline"
        incident.affected_services.append(service)
        db.add(service)

    db.commit()
    db.refresh(incident)
    return incident


def generate_executive_brief(incident: models.Incident) -> schemas.ExecutiveBrief:
    """
    Generates a leadership-ready executive brief for the incident.
    """
    affected = [s.name for s in incident.affected_services]

    impacts = set()
    risks = set()
    max_rto = 0
    tier_1_affected = False
    for s in incident.affected_services:
        if s.criticality_tier == 1:
            tier_1_affected = True

        impact_str = f"Financial Impact: {s.bia.financial_impact} | Regulatory Impact: {s.bia.regulatory_impact}"
        impacts.add(impact_str)

        if getattr(s, "vendor_readiness", "High") == "Low":
            risks.add(f"Vendor readiness for {s.name} is Low.")
        if getattr(s, "dr_site_status", "Ready") == "Offline":
            risks.add(f"DR Site for {s.name} is currently Offline.")

        if s.bia.rto_target_hours > max_rto:
            max_rto = s.bia.rto_target_hours

    top_business_impacts = list(impacts)[:3]
    top_risks = list(risks)[:3]
    if not top_risks:
        top_risks = [
            "Risk of extended downtime impacting SLA",
            "Potential reputational damage if not resolved quickly",
        ]

    recommendation = "Follow standard DR runbooks."
    if tier_1_affected:
        recommendation = "Immediate executive escalation required. Activate primary DR failover procedures."

    escalation = "Manager Level"
    if tier_1_affected:
        escalation = "C-Level Executive and Crisis Management Team"

    summary = (
        f"Incident '{incident.name}' triggered affecting {len(affected)} services."
    )

    return schemas.ExecutiveBrief(
        incident_summary=summary,
        affected_services=affected,
        top_business_impacts=top_business_impacts,
        recovery_recommendation=recommendation,
        estimated_restoration_timeline=f"{max_rto} hours estimated from incident start based on max RTO targets.",
        top_risks=top_risks,
        escalation_recommendation=escalation,
    )
