import httpx
import json

base_url = "http://127.0.0.1:8000/api/v1"

def fetch_and_print(endpoint):
    print(f"\n--- GET {endpoint} ---")
    try:
        r = httpx.get(f"{base_url}{endpoint}")
        data = r.json()
        if isinstance(data, list):
            print(json.dumps(data[:2], indent=2))
            print(f"... (total {len(data)} items)")
        else:
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

def trigger_and_check():
    print(f"\n--- POST /incidents/trigger ---")
    try:
        r = httpx.post(f"{base_url}/incidents/trigger", json={"name": "Primary Data Center Power Failure", "description": "Full site loss test"})
        inc = r.json()
        print(json.dumps(inc, indent=2))
        
        incident_id = inc['id']
        fetch_and_print(f"/incidents/{incident_id}/executive-brief")
        fetch_and_print(f"/recovery/prioritization/{incident_id}")
    except Exception as e:
        print(f"Error: {e}")

fetch_and_print("/services/")
fetch_and_print("/incidents/")
trigger_and_check()