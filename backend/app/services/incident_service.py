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

    # Define the direct impact of each scenario
    if scenario_name == "Primary Data Center Power Failure":
        # This affects all services hosted in the primary DC
        initial_impact = (
            db.query(models.Service)
            .filter(models.Service.primary_site == "us-east-1")
            .all()
        )

    elif scenario_name == "Ransomware on Virtualization Cluster":
        # This affects the cluster and everything on it
        cluster = (
            db.query(models.Service)
            .filter(models.Service.name == "Virtualization Cluster A")
            .first()
        )
        if cluster:
            initial_impact.append(cluster)
            # And all services that depend on it
            for dep in cluster.upstream_dependencies:
                initial_impact.append(dep.service)

    elif scenario_name == "Core DNS Service Unavailability":
        dns = (
            db.query(models.Service)
            .filter(models.Service.name == "Core DNS Service")
            .first()
        )
        if dns:
            initial_impact.append(dns)

    else:
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
    Triggers an incident simulation:
    1. Creates an incident record.
    2. Identifies all affected services based on the scenario.
    3. Updates the status of affected services.
    4. Associates services with the incident.
    """
    # 1. Get the blast radius
    affected_services = get_affected_services_by_scenario(db, scenario_name)
    if not affected_services:
        return None

    # 2. Create the incident record
    incident = crud.incident.create(
        db, obj_in=schemas.IncidentCreate(name=scenario_name, description=description)
    )

    # 3. Update service statuses and associate with the incident
    for service in affected_services:
        service.current_status = "Offline"  # Or more nuanced logic could be here
        incident.affected_services.append(service)
        db.add(service)

    db.commit()
    db.refresh(incident)

    return incident
