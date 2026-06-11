# Live Log Capture and Evidence Methods

This document describes how to capture, export, and preserve evidence from Splunk and Wazuh for incident investigation and forensic analysis.

---

## Splunk Search Export

### Method 1: Export from Splunk Web UI

1. Run the detection search in Splunk
2. Click **Export** at the bottom of the search results
3. Choose format:
   - **CSV** — recommended for Excel analysis and sharing
   - **JSON** — recommended for API integration and automation
   - **Raw** — recommended for full event context
4. Select time range for export
5. Click **Export** and save to local machine

### Method 2: Export via SPL Command

```splunk
# Export password spray events to CSV
index=wineventlog host=WIN-WS01 EventCode=4625
| export output=csv
```

### Method 3: Export via CLI (Linux)

```bash
# Use Splunk CLI to export search results programmatically
cd /opt/splunk/bin
./splunk search "search index=wineventlog EventCode=4625 host=WIN-WS01" \
  -auth <username>:<password> \
  -output csv > password_spray_export.csv
```

---

## Capturing Full Event Context

### Method 1: Splunk All Fields Export

When exporting, include the following fields to capture full event context:

- `_time` — event timestamp
- `_indextime` — ingestion timestamp
- `_raw` — original unparsed event
- `host` — source host
- `sourcetype` — log type (WinEventLog:Security, sysmon, etc.)
- `source` — log file path or source identifier
- All parsed fields (EventCode, Account_Name, Source_Network_Address, etc.)

### Method 2: Raw Event Extraction

```splunk
# Export raw XML events (includes all Windows Event Log metadata)
index=wineventlog host=WIN-WS01 EventCode=4625 earliest=<time>
| table _raw, _time, host
| export output=csv
```

The `_raw` field contains the original Windows Event XML, which can be re-parsed or imported into other tools.

---

## Evidence Preservation for Forensics

### For Windows Event Log Analysis

1. Export full event logs from WIN-WS01 using Event Viewer
   - Right-click on Security log → Save All Events As... → Select XML format
   - Save to network share or removable media

2. Alternatively, use PowerShell to export logs:
   ```powershell
   # On WIN-WS01, export Security event log
   Get-WinEvent -LogName Security -FilterXPath "*[System[EventID=4625]]" `
     -MaxEvents 10000 | Export-Csv -NoTypeInformation password_spray_events.csv
   
   # Export Sysmon logs (if Event ID 1, 10, etc.)
   Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" `
     -FilterXPath "*[System[EventID=1 or EventID=10]]" `
     -MaxEvents 10000 | Export-Csv -NoTypeInformation sysmon_process_events.csv
   ```

### For Sysmon Event Analysis

1. Export via Splunk (recommended)
   ```splunk
   index=sysmon host=WIN-WS01 EventID=1 earliest=<attack_start> latest=<attack_end>
   | export output=csv
   ```

2. Alternatively, use Process Monitor or similar EDR tools to capture process tree

### For DNS Query Analysis

1. Export Sysmon DNS events
   ```splunk
   index=sysmon host=WIN-WS01 EventID=22 earliest=<time>
   | table _time, Image, QueryName, QueryStatus, ProcessId
   | export output=csv
   ```

2. Alternatively, extract from Windows DNS logs (if available)

---

## Chain of Custody

When preserving evidence, document:

| Field | Example |
|---|---|
| Evidence ID | INC-2024-001-EVIDENCE-001 |
| Description | Password spray events from 4625 detection |
| Source System | WIN-WS01 / Splunk Enterprise |
| Date/Time Captured | 2024-06-10 14:30 UTC |
| Captured By | SOC 1 Analyst (John Doe) |
| File Hash (MD5) | a1b2c3d4e5f6... |
| File Hash (SHA256) | 1a2b3c4d5e6f7g8h... |
| Storage Location | \\forensics-share\INC-2024-001\ |
| Authorized Access | [List authorized forensic/IR personnel] |

---

## Evidence Storage Best Practices

1. **Store on secure network share** with restricted access
   - Path: `\\forensics-share\INC-XXXXX\`
   - NTFS permissions: Administrators, IR Team, Compliance

2. **Use consistent naming convention**
   - Format: `INC-XXXXX_YYYY-MM-DD_DescriptionOfEvidence.csv`
   - Example: `INC-001_2024-06-10_PasswordSprayExport.csv`

3. **Calculate and store file hashes**
   - MD5 for quick reference
   - SHA256 for forensic integrity
   - Method: `Get-FileHash <file> -Algorithm SHA256`

4. **Document retention policy**
   - Keep evidence for minimum [company policy] days
   - Encrypt if stored on removable media
   - Destroy after retention period per policy

---

## Automated Evidence Collection

### Script Example: Splunk Evidence Collector

```bash
#!/bin/bash
# Collect evidence from Splunk for a given incident

INCIDENT_ID=$1
EXPORT_DIR="/forensics/${INCIDENT_ID}"
SPLUNK_HOST="splunk.lab.local"
SPLUNK_USER="admin"
SPLUNK_PASS="password"

# Create export directory
mkdir -p $EXPORT_DIR

# Export 4625 events
curl -k -u ${SPLUNK_USER}:${SPLUNK_PASS} \
  "https://${SPLUNK_HOST}:8089/services/search/jobs" \
  -d search="search index=wineventlog host=WIN-WS01 EventCode=4625 earliest=-24h@h" \
  -d output_mode=csv \
  > ${EXPORT_DIR}/4625_events.csv

# Export Sysmon events
curl -k -u ${SPLUNK_USER}:${SPLUNK_PASS} \
  "https://${SPLUNK_HOST}:8089/services/search/jobs" \
  -d search="search index=sysmon host=WIN-WS01 EventID=1 earliest=-24h@h" \
  -d output_mode=csv \
  > ${EXPORT_DIR}/sysmon_process_creation.csv

# Calculate hashes
sha256sum ${EXPORT_DIR}/* > ${EXPORT_DIR}/hashes.txt

echo "Evidence exported to: ${EXPORT_DIR}"
```

---

## Evidence for Wazuh Analysis

### Export Wazuh Alerts via API

```bash
# Query Wazuh API for alerts related to incident
curl -s -X GET \
  "https://wazuh-manager.lab.local:55000/api/v1/events" \
  -H "Authorization: Bearer <AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "rule.description: password_spray"}' \
  | jq . > wazuh_alerts.json
```

### Export via Wazuh Dashboard

1. Log into Wazuh Dashboard
2. Navigate to Threat Intelligence → Events
3. Apply filters for incident time range and relevant rule names
4. Click **Export** → **JSON** or **CSV**

---

## Chain of Custody Form Template

```
INCIDENT EVIDENCE CHAIN OF CUSTODY FORM

Incident Number: _______________
Evidence ID: _______________
Description: _______________
Source System: _______________

Date/Time Collected: _______________
Collected By: _______________ (signature)

Date/Time Received: _______________
Received By: _______________ (signature)

File Hash (MD5): _______________
File Hash (SHA256): _______________

Storage Location: _______________
Access Restrictions: _______________

Date Released: _______________
Released To: _______________ (signature)

Disposition: [ ] Archived [ ] Destroyed [ ] Transferred
Date: _______________
Authorized By: _______________ (signature)
```

---

## Legal and Compliance Notes

- Ensure evidence preservation complies with internal policy and applicable law
- Do not modify evidence after collection
- Maintain chain of custody documentation
- Restrict access to authorized personnel only
- Follow data retention and destruction policies
- If evidence may be used in legal proceedings, coordinate with Legal/Compliance teams

---

*Use this document to standardize evidence collection and preservation across the SOC lab.*
