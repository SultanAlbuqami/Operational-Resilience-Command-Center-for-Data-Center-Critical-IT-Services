import sqlite3

conn = sqlite3.connect('resilience_command_center.db')
c = conn.cursor()
print(f"Services: {c.execute('SELECT COUNT(*) FROM services').fetchone()[0]}")
print(f"Dependencies: {c.execute('SELECT COUNT(*) FROM dependencies').fetchone()[0]}")
print(f"Incidents: {c.execute('SELECT COUNT(*) FROM incidents').fetchone()[0]}")
print(f"Runbook Tasks: {c.execute('SELECT COUNT(*) FROM runbook_tasks').fetchone()[0]}")
print(f"DR Exercises: {c.execute('SELECT COUNT(*) FROM dr_exercises').fetchone()[0]}")
print(f"Vendors: {c.execute('SELECT COUNT(DISTINCT vendor) FROM services WHERE vendor IS NOT NULL').fetchone()[0]}")
