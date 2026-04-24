import logging

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.database import SessionLocal, engine
from app.models import bia, dependency, dr_exercise, runbook, service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_data():
    db: Session = SessionLocal()
    try:
        logger.info("Recreating database tables...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        logger.info("Seeding data...")
        services_map = _seed_services_and_bia(db)
        _seed_dependencies(db, services_map)
        _seed_runbooks(db, services_map)
        _seed_dr_exercises(db, services_map)

        logger.info("Data seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


def _seed_services_and_bia(db: Session):
    services_to_create = {
        "Customer Identity Platform": {
            "owner": "Identity Team",
            "business_unit": "Digital",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "Okta",
            "vendor_readiness": "High",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 1,
                "rpo_target_minutes": 5,
                "financial_impact": "High",
                "regulatory_impact": "High",
                "reputational_impact": "High",
                "key_business_process_supported": "Customer Authentication",
            },
        },
        "Billing Core": {
            "owner": "Finance Tech",
            "business_unit": "Finance",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "Stripe",
            "vendor_readiness": "High",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 4,
                "rpo_target_minutes": 15,
                "financial_impact": "Very High",
                "regulatory_impact": "High",
                "reputational_impact": "High",
                "key_business_process_supported": "Revenue Collection",
            },
        },
        "CRM Platform": {
            "owner": "Sales Operations",
            "business_unit": "Sales",
            "criticality_tier": 2,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "Salesforce",
            "vendor_readiness": "High",
            "dr_site_status": "Ready",
            "continuity_posture": "At Risk",
            "bia": {
                "rto_target_hours": 8,
                "rpo_target_minutes": 60,
                "financial_impact": "Medium",
                "regulatory_impact": "Low",
                "reputational_impact": "Medium",
                "key_business_process_supported": "Lead Management",
            },
        },
        "Customer Digital Channels": {
            "owner": "Digital Products",
            "business_unit": "Marketing",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "AWS",
            "vendor_readiness": "High",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 2,
                "rpo_target_minutes": 30,
                "financial_impact": "High",
                "regulatory_impact": "Low",
                "reputational_impact": "High",
                "key_business_process_supported": "Public Web Presence",
            },
        },
        "Network Monitoring Platform": {
            "owner": "NOC",
            "business_unit": "Technology",
            "criticality_tier": 1,
            "primary_site": "Global",
            "dr_site": "Global",
            "vendor": "Datadog",
            "vendor_readiness": "Medium",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 0.5,
                "rpo_target_minutes": 5,
                "financial_impact": "Low",
                "regulatory_impact": "N/A",
                "reputational_impact": "Low",
                "key_business_process_supported": "Infrastructure Visibility",
            },
        },
        "Enterprise Backup Platform": {
            "owner": "IT Operations",
            "business_unit": "Technology",
            "criticality_tier": 2,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "Veeam",
            "vendor_readiness": "High",
            "dr_site_status": "Degraded",
            "continuity_posture": "Degraded",
            "bia": {
                "rto_target_hours": 24,
                "rpo_target_minutes": 60,
                "financial_impact": "Low",
                "regulatory_impact": "Medium",
                "reputational_impact": "Low",
                "key_business_process_supported": "Data Protection",
            },
        },
        "Virtualization Cluster A": {
            "owner": "Infrastructure",
            "business_unit": "Technology",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "VMware",
            "vendor_readiness": "High",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 4,
                "rpo_target_minutes": 0,
                "financial_impact": "High",
                "regulatory_impact": "N/A",
                "reputational_impact": "Medium",
                "key_business_process_supported": "Compute Foundation",
            },
        },
        "Storage Array X": {
            "owner": "Infrastructure",
            "business_unit": "Technology",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "NetApp",
            "vendor_readiness": "Low",
            "dr_site_status": "Offline",
            "continuity_posture": "At Risk",
            "bia": {
                "rto_target_hours": 4,
                "rpo_target_minutes": 0,
                "financial_impact": "High",
                "regulatory_impact": "N/A",
                "reputational_impact": "Medium",
                "key_business_process_supported": "Data Storage Foundation",
            },
        },
        "DR Replication Service": {
            "owner": "Storage Team",
            "business_unit": "Technology",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "us-west-1",
            "vendor": "Zerto",
            "vendor_readiness": "Medium",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 2,
                "rpo_target_minutes": 5,
                "financial_impact": "Medium",
                "regulatory_impact": "High",
                "reputational_impact": "Medium",
                "key_business_process_supported": "Data Replication",
            },
        },
        "Core DNS Service": {
            "owner": "Network Team",
            "business_unit": "Technology",
            "criticality_tier": 1,
            "primary_site": "Global",
            "dr_site": "Global",
            "vendor": "Cloudflare",
            "vendor_readiness": "High",
            "dr_site_status": "Ready",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 1,
                "rpo_target_minutes": 5,
                "financial_impact": "Very High",
                "regulatory_impact": "N/A",
                "reputational_impact": "High",
                "key_business_process_supported": "Service Discovery",
            },
        },
        "Facilities Power and Cooling": {
            "owner": "Facilities",
            "business_unit": "Real Estate",
            "criticality_tier": 1,
            "primary_site": "us-east-1",
            "dr_site": "N/A",
            "vendor": "Schneider Electric",
            "vendor_readiness": "High",
            "dr_site_status": "N/A",
            "continuity_posture": "Healthy",
            "bia": {
                "rto_target_hours": 1,
                "rpo_target_minutes": 0,
                "financial_impact": "Very High",
                "regulatory_impact": "Medium",
                "reputational_impact": "High",
                "key_business_process_supported": "Data Center Environment",
            },
        },
    }

    services_map = {}
    for name, data in services_to_create.items():
        bia_data = data.pop("bia")
        new_service = service.Service(name=name, **data)
        new_bia = bia.BIA(service=new_service, **bia_data)
        db.add(new_service)
        db.add(new_bia)
        services_map[name] = new_service

    db.commit()
    for s in services_map.values():
        db.refresh(s)

    logger.info(f"Created {len(services_map)} services.")
    return services_map


def _seed_dependencies(db: Session, services: dict):
    dependencies_to_create = [
        ("Customer Digital Channels", "Customer Identity Platform"),
        ("Customer Digital Channels", "Core DNS Service"),
        ("Customer Digital Channels", "CRM Platform"),
        ("Billing Core", "CRM Platform"),
        ("Billing Core", "Customer Identity Platform"),
        ("Billing Core", "Virtualization Cluster A"),
        ("CRM Platform", "Customer Identity Platform"),
        ("CRM Platform", "Storage Array X"),
        ("CRM Platform", "Virtualization Cluster A"),
        ("Customer Identity Platform", "Core DNS Service"),
        ("Customer Identity Platform", "Storage Array X"),
        ("Customer Identity Platform", "Virtualization Cluster A"),
        ("Virtualization Cluster A", "Storage Array X"),
        ("Virtualization Cluster A", "Facilities Power and Cooling"),
        ("Storage Array X", "Facilities Power and Cooling"),
        ("Network Monitoring Platform", "Core DNS Service"),
        ("Network Monitoring Platform", "Virtualization Cluster A"),
        ("Enterprise Backup Platform", "Storage Array X"),
        ("Enterprise Backup Platform", "Virtualization Cluster A"),
        ("DR Replication Service", "Storage Array X"),
        ("DR Replication Service", "Virtualization Cluster A"),
    ]

    for dependant, dependency_service in dependencies_to_create:
        new_dep = dependency.Dependency(
            service_id=services[dependant].id,
            depends_on_id=services[dependency_service].id,
        )
        db.add(new_dep)

    db.commit()
    logger.info(f"Created {len(dependencies_to_create)} dependencies.")


def _seed_runbooks(db: Session, services: dict):
    runbooks_to_create = {
        "Customer Identity Platform": [
            {
                "step_number": 1,
                "task_description": "Failover database to secondary site",
                "owner": "DBA Team",
                "eta_minutes": 15,
            },
            {
                "step_number": 2,
                "task_description": "Update DNS records to point to DR site IP",
                "owner": "Network Team",
                "eta_minutes": 10,
            },
            {
                "step_number": 3,
                "task_description": "Restart application servers in DR site",
                "owner": "Identity Team",
                "eta_minutes": 5,
            },
            {
                "step_number": 4,
                "task_description": "Verify login functionality",
                "owner": "QA Team",
                "eta_minutes": 20,
            },
        ],
        "Billing Core": [
            {
                "step_number": 1,
                "task_description": "Restore database from last snapshot",
                "owner": "DBA Team",
                "eta_minutes": 60,
            },
            {
                "step_number": 2,
                "task_description": "Deploy application stack to DR servers",
                "owner": "Finance Tech",
                "eta_minutes": 45,
            },
            {
                "step_number": 3,
                "task_description": "Run data integrity checks",
                "owner": "Finance Tech",
                "eta_minutes": 30,
            },
        ],
        "Storage Array X": [
            {
                "step_number": 1,
                "task_description": "Assess physical damage to arrays",
                "owner": "Storage Team",
                "eta_minutes": 30,
            },
            {
                "step_number": 2,
                "task_description": "Activate Zerto replication failover",
                "owner": "Storage Team",
                "eta_minutes": 45,
            },
            {
                "step_number": 3,
                "task_description": "Verify LUN visibility in DR",
                "owner": "Storage Team",
                "eta_minutes": 15,
            },
        ],
    }

    count = 0
    for service_name, tasks in runbooks_to_create.items():
        for task_data in tasks:
            new_task = runbook.RunbookTask(
                service_id=services[service_name].id, **task_data
            )
            db.add(new_task)
            count += 1

    db.commit()
    logger.info(f"Created {count} runbook tasks.")


def _seed_dr_exercises(db: Session, services: dict):
    exercises_to_create = [
        {
            "name": "Q1 Billing DR Failover Test",
            "scenario": "Primary DB server outage for Billing Core",
            "target_rto_minutes": 240,
            "target_rpo_minutes": 15,
            "actual_rto_minutes": 210,
            "actual_rpo_minutes": 12,
            "passed": True,
            "issues_observed": "Minor delays in DNS propagation.",
            "lessons_learned": "DNS update script needs performance tuning.",
            "corrective_actions": "Automate DNS updates via new script; assigned to Network Team.",
            "owner": "Finance Tech",
            "services": [services["Billing Core"]],
        },
        {
            "name": "Full DC Failover Simulation (Tabletop)",
            "scenario": "Loss of primary data center (us-east-1)",
            "target_rto_minutes": 240,
            "target_rpo_minutes": 15,
            "actual_rto_minutes": 360,
            "actual_rpo_minutes": 25,
            "passed": False,
            "issues_observed": "Dependency mapping for CRM Platform was inaccurate, leading to incorrect recovery sequence. Runbook for storage failover was outdated.",
            "lessons_learned": "Live dependency data and runbook validation are critical.",
            "corrective_actions": "Update CRM dependencies in Command Center. Revise storage runbook.",
            "owner": "IT Operations",
            "services": [
                services["CRM Platform"],
                services["Customer Identity Platform"],
                services["Billing Core"],
            ],
        },
        {
            "name": "Ransomware Tabletop - Identity",
            "scenario": "Okta sync compromised",
            "target_rto_minutes": 60,
            "target_rpo_minutes": 5,
            "actual_rto_minutes": 45,
            "actual_rpo_minutes": 5,
            "passed": True,
            "issues_observed": "None, runbook worked as expected.",
            "lessons_learned": "Regular review of vendor readiness is helpful.",
            "corrective_actions": "None.",
            "owner": "Identity Team",
            "services": [services["Customer Identity Platform"]],
        },
    ]

    for ex_data in exercises_to_create:
        new_exercise = dr_exercise.DRExercise(**ex_data)
        db.add(new_exercise)

    db.commit()
    logger.info(f"Created {len(exercises_to_create)} DR exercises.")


if __name__ == "__main__":
    logger.info("Starting database seeding process...")
    seed_data()
