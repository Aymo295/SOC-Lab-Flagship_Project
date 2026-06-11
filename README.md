# Cybersecurity Flagship SOC Lab

## Project Purpose

Build a realistic SOC environment focused on telemetry validation, detection engineering, incident response, and business impact analysis. This lab simulates a full attack lifecycle from initial access through persistence, with corresponding detection coverage, analyst workflows, and security operations improvements.

---

## Environment Architecture

### SOC Brain (Ubuntu)
- **Splunk Enterprise** — centralized log ingestion, search, and alerting
- **Wazuh Manager** — agent-based telemetry collection and behavioral alerting
- **Chrony NTP Server** — time synchronization for event correlation

### Monitored Endpoint (Windows 11 Enterprise)
- **Hostname**: WIN-WS01
- **Telemetry sources**:
  - Windows Security Event Log (4625, 4624, 4672, etc.)
  - Sysmon (Process creation, network connections, registry, LSASS access, DNS, etc.)
- **Forwarder**: Splunk Universal Forwarder

### Attacker Node (Kali Linux)
- **Status**: Provisioned; awaiting active use for controlled attack simulation
- **Purpose**: Execute attack scenarios against WIN-WS01 under observation

---

## Current Project Status

### Phase 1 / Phase 1.5: Telemetry Validation (Complete/In Progress)
- ✅ Sysmon Event ID 1 ingestion verified into Splunk
- ✅ Windows Security event log forwarding verified
- ✅ Wazuh manager/agent pipeline active
- ✅ Host-only network isolation and firewall validated
- ✅ Time synchronization baseline established
- ⏳ Ingestion delay monitoring and heartbeat validation in progress

### Phase 2: Detection Engineering (Planned)
- Priority detections:
  - `4625` — Failed logon password spray detection
  - `4624` — Successful RDP logon detection (Logon Type 10)
  - `4672` — Privileged logon anomalies
  - `Sysmon Event ID 1` — Suspicious PowerShell execution
  - `Sysmon Event ID 10` — LSASS credential access
  - Process chain correlations (parent/child relationships)
  - DNS tunneling / C2-style communication
  - Registry persistence modification

### Phase 3: Controlled Attack Simulation (Planned)
- Password spray / RDP brute-force entry
- Suspicious PowerShell execution and parent-child process abuse
- DNS tunneling or safe C2-style communication
- Registry persistence

### Phase 4+: Incident Response, Automation, Dashboards (Future)

---

## Attack and Detection Roadmap

### Attack Flow
1. **Initial Access**: Password spray / brute-force RDP entry → detect via `4625` threshold, escalate on `4624` success
2. **Execution**: Suspicious PowerShell command-line execution → detect via Sysmon Event ID 1 anomalies
3. **Process Abuse**: Parent-child process chains (PowerShell → cmd/wmic/etc.) → detect via process chain correlation
4. **Persistence/C2**: Registry modification or DNS tunneling → detect via Sysmon Event ID 12/13 or network DNS analysis
5. **Impact**: Timeline reconstruction, containment planning, business impact assessment

### Detection Coverage
- `splunk/searches/` — production-ready SPL queries for each detection
- `sigma/` — portable detection rules for portability and future SIEM migration
- `notes/response_playbooks.md` — SOC 1/2 analyst workflows and triage steps

---

## Live Validation Goals

The lab validates both detection logic and SOC analyst capability:

1. **Telemetry validation** — confirm all expected event types flow into Splunk and Wazuh
2. **Detection validation** — run searches against live data and confirm precision/recall
3. **Response validation** — use real search output to drive incident response workflows
4. **Business impact mapping** — tie technical findings to organizational risk and remediation priorities

---

## Repository Structure

```
soc-analst-lab/
├── README.md                              # This file
├── notes/
│   ├── lab_overview.md                    # Live environment status and troubleshooting
│   ├── response_playbooks.md              # SOC 1/2 workflows for each detection
│   ├── failed_logon_investigation.md      # Incident response template and exercise
│   └── live_log_capture.md                # Methods for collecting Splunk evidence
├── splunk/
│   └── searches/
│       ├── failed_logons.spl              # Password spray detection (updated)
│       ├── 4625_password_spray.spl        # Failed logon threshold logic
│       ├── 4624_rdp_success.spl           # Successful RDP logon detection
│       ├── 4672_privileged_logon.spl      # Privileged logon anomalies
│       ├── sysmon_powershell_abuse.spl    # Suspicious PowerShell commands
│       ├── sysmon_parent_child_process.spl # Process chain detection
│       ├── sysmon_dns_tunneling.spl       # DNS-based C2 indicators
│       ├── sysmon_registry_persistence.spl # Registry modification detection
│       └── telemetry_health.spl           # Ingestion health and heartbeat
├── sigma/
│   ├── 4625_password_spray.yml            # Portable failed logon spray rule
│   ├── 4624_rdp_success.yml               # Portable RDP detection rule
│   ├── 4672_privileged_logon.yml          # Portable privileged logon rule
│   ├── sysmon_powershell_abuse.yml        # Portable PowerShell detection rule
│   ├── sysmon_parent_child_process.yml    # Portable process chain rule
│   ├── sysmon_dns_tunneling.yml           # Portable DNS tunneling rule
│   └── sysmon_registry_persistence.yml    # Portable persistence detection rule
└── logs/
    └── (Live Splunk-ingested logs only; no simulated attack data)
```

---

## Getting Started

1. **Review the lab environment**
   - See `notes/lab_overview.md` for current telemetry pipeline status
   - Run the troubleshooting checklist to validate live ingestion

2. **Validate Splunk ingestion**
   ```
   # In Splunk, run:
   host=WIN-WS01 | stats count by sourcetype
   ```
   - Verify Windows Security and Sysmon Event Log sourcetypes are present

3. **Run a detection search**
   - Navigate to `splunk/searches/failed_logons.spl`
   - Adapt field names to your Splunk configuration if needed
   - Run the search to verify 4625 events are detected

4. **Generate attack logs**
   - Use your Kali attacker node to execute a password spray or RDP brute-force attack
   - Monitor the Splunk search output in real time
   - Document observations in `notes/failed_logon_investigation.md`

5. **Document your response**
   - Follow the SOC workflows in `notes/response_playbooks.md`
   - Complete the incident response exercise in `notes/failed_logon_investigation.md`
   - Map findings to business impact

---

## Key Concepts

### Telemetry Generation vs. Collection
- Telemetry generation (Sysmon, Windows Event Log) and collection (Splunk UF, Wazuh agent) are separate systems
- A running service does not guarantee network accessibility; firewall scope and connectivity must be validated
- Time synchronization is foundational for event correlation across multiple hosts

### Detection Philosophy
- **Build controls, test controls, break controls, improve controls**
- Validate detections using live attacks before rolling to production
- Reduce false positives iteratively based on environment tuning
- Establish correlation logic to chain related events into incident timelines

### SOC Analyst Maturity
- **SOC 1**: Triage, validation, basic containment, analyst notes
- **SOC 2**: Deeper investigation, correlation, escalation, root cause analysis
- **SOC 3**: Strategic recommendations, threat hunting, process improvement

---

## Next Steps

1. Complete Phase 1.5 telemetry reliability monitoring (heartbeat validation, ingestion delay analysis)
2. Populate `splunk/searches/` with queries tuned to your live Splunk environment
3. Execute controlled attack simulations against WIN-WS01
4. Validate each detection and capture evidence in `notes/`
5. Build incident response playbooks based on observed attack patterns
6. Iterate on detection logic and false positive tuning

---

## References

- **MITRE ATT&CK Framework** — https://attack.mitre.org/
- **Sigma Rules** — https://github.com/SigmaHQ/sigma
- **Windows Event Log IDs** — 4625, 4624, 4672, etc.
- **Sysmon Event IDs** — 1 (Process Create), 10 (LSASS Access), 12/13 (Registry), 22 (DNS Query)

---

## Project Owner

Aaron Mitchell Oldham

---

## Last Updated

2026-06-10

---

*This is a practical, hands-on learning environment designed to develop SOC analyst skills through realistic attack simulation and detection engineering.*
