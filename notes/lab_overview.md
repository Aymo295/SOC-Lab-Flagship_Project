# SOC Lab Environment Overview

## Live Environment Summary

### SOC Brain (Ubuntu)
- **Splunk Enterprise** on Ubuntu with Splunk Universal Forwarder configured
- **Wazuh Manager** with Windows agent deployed and active
- **Chrony NTP Server** configured as time reference for both hosts

### Monitored Endpoint (Windows 11 Enterprise)
- **Hostname**: WIN-WS01
- **Sysmon**: Installed and actively logging
- **Splunk Universal Forwarder**: Configured to forward Windows Security and Sysmon events
- **Wazuh Agent**: Installed and connected to manager
- **Network**: Host-only isolated network for security purposes

### Attacker Node (Kali Linux)
- **Status**: Provisioned but not yet used for active attack simulation
- **Purpose**: Execute controlled attacks against WIN-WS01 under Splunk/Wazuh observation
- **Next Step**: Deploy attack tools and begin password spray simulation

---

## Telemetry Pipeline Status

### Completed ✅
- Sysmon Event ID 1 ingestion into Splunk verified
- Windows Security event forwarding verified
- Wazuh manager/agent connection established
- Host-only network connectivity validated
- Firewall rules (UFW) configured and tested
- Time synchronization baseline established

### In Progress ⏳
- Ingestion delay analysis (`_indextime - _time`)
- Telemetry heartbeat monitoring (scheduled tasks)
- TCP reachability alerting
- Sysmon zero-volume alerting
- Time drift anomaly detection

---

## Expected Log Sources for Live Validation

### Windows Security Events (WinEventLog:Security)
- **EventCode 4625** — Failed logon attempt
  - Fields: Account_Name, Source_Network_Address, Workstation_Name, LogonType
  - Use case: Detect password spray and brute force
- **EventCode 4624** — Successful logon
  - Fields: Account_Name, Source_Network_Address, Logon_Type
  - Use case: Detect suspicious successful logons after failures
- **EventCode 4672** — Assignment of admin rights
  - Fields: Account_Name, Privileges
  - Use case: Detect privilege escalation or unusual privileged logons

### Sysmon Events (XmlWinEventLog:Microsoft-Windows-Sysmon/Operational)
- **EventID 1** — Process creation
  - Fields: Image, CommandLine, ParentImage, ParentCommandLine, User, ProcessId, ParentProcessId
  - Use case: Detect suspicious PowerShell execution, process chains
- **EventID 10** — Process access (LSASS)
  - Fields: SourceImage, TargetImage, ProcessId, TargetProcessId, GrantedAccess
  - Use case: Detect credential dumping attempts
- **EventID 12/13** — Registry modification
  - Fields: TargetObject, Details, Image
  - Use case: Detect persistence mechanism installation
- **EventID 22** — DNS query
  - Fields: QueryName, QueryStatus, Image, ProcessId
  - Use case: Detect DNS tunneling or C2 communication

---

## Planned Detection Phases

### Phase 2 (Initial Detections)
1. **4625 Password Spray** — Threshold-based detection across multiple accounts from one source
2. **4624 RDP Success** — Successful logon (Logon Type 10) after repeated failures
3. **4672 Privileged Logon** — Unusual or anomalous privileged logon events
4. **Sysmon PowerShell Abuse** — Suspicious PowerShell command-line parameters
5. **Sysmon Parent-Child Process** — Process chain detection (PowerShell → cmd, wmic, etc.)
6. **Sysmon DNS Tunneling** — Suspicious DNS query patterns or C2 indicators
7. **Sysmon Registry Persistence** — Registry modification under common persistence keys

### Phase 3 (Controlled Attack Simulation)
- Execute each attack scenario in the attack flow
- Validate corresponding detection fires
- Document evidence and analyst response

---

## Attack Sequence and Expected Behavior

### Stage 1: Initial Access (Password Spray / RDP Brute Force)
- **Expected logs**: 4625 events (many failures), followed by 4624 success (if brute force succeeds)
- **Detection**: `4625_password_spray.spl` on repeated failures from same source across multiple accounts
- **SOC 1 response**: Identify source IP, lock accounts, validate MFA, consider host isolation
- **SOC 2 response**: Correlate with threat intelligence, estimate dwell time, escalate to identity team

### Stage 2: Execution (Suspicious PowerShell)
- **Expected logs**: Sysmon Event ID 1 with PowerShell command-line containing suspicious parameters
- **Detection**: `sysmon_powershell_abuse.spl` filtering for `-EncodedCommand`, `Invoke-Expression`, `DownloadString`, etc.
- **SOC 1 response**: Capture command line, review script block logging, isolate host if confirmed malicious
- **SOC 2 response**: Analyze script behavior, determine attacker objective, plan remediation

### Stage 3: Persistence / Process Abuse (Parent-Child Chains)
- **Expected logs**: Sysmon Event ID 1 showing PowerShell parent spawning cmd/wmic/other tools
- **Detection**: `sysmon_parent_child_process.spl` on suspicious parent-child relationships
- **SOC 1 response**: Validate process lineage, gather artifact paths, document timeline
- **SOC 2 response**: Determine attack intent, identify lateral movement risk

### Stage 4: C2 Communication (DNS Tunneling / Network)
- **Expected logs**: Sysmon Event ID 22 (DNS) or Event ID 3 (Network Connect) with suspicious patterns
- **Detection**: `sysmon_dns_tunneling.spl` on DNS query frequency, unusual hostnames, long names
- **SOC 1 response**: Document DNS requests, isolate host, notify network team
- **SOC 2 response**: Analyze beacon frequency, estimate data exfiltration, escalate to incident response

### Stage 5: Persistence (Registry Modification)
- **Expected logs**: Sysmon Event ID 12/13 under HKLM\Software\Microsoft\Windows\Run, etc.
- **Detection**: `sysmon_registry_persistence.spl` on persistence key modifications
- **SOC 1 response**: Capture registry modification, remove persistence mechanism
- **SOC 2 response**: Determine persistence intent, assess re-compromise risk, plan remediation

---

## Live Validation Checklist

### Pre-Validation (Environment Health)
- [ ] Splunk Universal Forwarder service status: running
- [ ] Wazuh agent status: connected
- [ ] Network connectivity: host-only interface active
- [ ] Firewall rules: UFW configured and allow rules verified
- [ ] Time sync: Windows w32time service running, Splunk/Wazuh timestamps synchronized

### Splunk Ingestion Checks
- [ ] Run: `host=WIN-WS01 | stats count by sourcetype`
  - Verify `WinEventLog:Security` and `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` are present
- [ ] Run: `host=WIN-WS01 EventCode=4625 | stats count`
  - Verify 4625 events are ingested
- [ ] Run: `host=WIN-WS01 EventID=1 | stats count`
  - Verify Sysmon Event ID 1 (process creation) is ingested
- [ ] Run: `index=_internal host=WIN-WS01 | stats count`
  - Verify forwarder health and metrics

### Wazuh Health Checks
- [ ] Wazuh manager dashboard: Agent WIN-WS01 shown as connected
- [ ] Wazuh alerts: Events flowing from WIN-WS01
- [ ] Sysmon integration: Sysmon events visible in Wazuh if configured

### Detection Search Validation
- [ ] Run each search stub against live data
- [ ] Document baseline event counts
- [ ] Prepare to generate attacks and validate alert firing

---

## Troubleshooting Checklist

### Splunk Forwarder Not Sending Data
- [ ] Check forwarder service status: `Get-Service SplunkForwarder` on WIN-WS01
- [ ] Verify UF outputs.conf points to Splunk Enterprise IP and port 9997
- [ ] Check firewall rules on both sides (Ubuntu UFW and Windows Firewall)
- [ ] Review forwarder logs: `%ProgramFiles%\SplunkUniversalForwarder\var\log\splunk\splunkd.log`

### Sysmon Events Not Reaching Splunk
- [ ] Verify Sysmon service is running: `Get-Service Sysmon`
- [ ] Check Sysmon configuration XML: `C:\ProgramData\Sysmon\Sysmon.xml`
- [ ] Verify Windows Event Viewer shows Sysmon logs under Applications and Services
- [ ] Check Splunk UF input configuration for Sysmon channel permissions
- [ ] Consider running Splunk UF service account as Local System (vs. NT SERVICE\SplunkForwarder)

### Wazuh Agent Not Connected
- [ ] Verify Wazuh agent service status on WIN-WS01
- [ ] Check agent configuration in `C:\Program Files (x86)\ossec-agent\ossec.conf`
- [ ] Verify manager IP and port are correct
- [ ] Check Windows Firewall allows outbound communication to manager IP:1514

### Time Synchronization Issues
- [ ] Verify Windows w32time service is running: `Get-Service w32time`
- [ ] Check time sync status: `w32tm /status`
- [ ] Verify Splunk and Wazuh are using the same NTP reference
- [ ] If timestamps drift, restart w32time and resync: `w32tm /resync`

### Firewall / Network Issues
- [ ] Test connectivity from Windows to Ubuntu Splunk: `Test-NetConnection <Ubuntu IP> -Port 9997`
- [ ] Check UFW rules on Ubuntu: `sudo ufw status verbose`
- [ ] Verify host-only network subnet matches both sides
- [ ] Check iptables rules if UFW shows allow but traffic is still blocked

---

## Key Investigation Questions

1. **Does the Windows endpoint forward Sysmon events reliably?**
   - Check Splunk ingestion rates over time for Sysmon sourcetype
   - Look for gaps or silence periods
   - Add heartbeat monitoring to alert on >10 minute silence

2. **Which sources are silent or unreliable?**
   - Monitor ingestion delay (`_indextime - _time`) per sourcetype
   - Establish baseline and alert on anomalies
   - Use `notes/telemetry_health.spl` search

3. **Does the detection logic fire on real attack behavior?**
   - After executing a controlled attack, run the detection search
   - Compare results to expected attack pattern
   - Tune field names and thresholds as needed

4. **What is the SOC analyst's triage workflow?**
   - For each alert, follow steps in `notes/response_playbooks.md`
   - Document containment options and business impact
   - Test both SOC 1 (quick triage) and SOC 2 (deep investigation) workflows

---

## Notes for Live Tuning

### Splunk Field Adaptation
- Windows Event Log field names may vary by Splunk version and UF configuration
- Common variations: `Account_Name` vs. `user`, `Source_Network_Address` vs. `src_ip`
- Each search stub includes placeholder field names; adapt to your environment

### Sysmon Field Mapping
- Sysmon fields vary between Windows and Splunk parsing
- Verify exact field names in Splunk: run a search and inspect the raw event
- Example: `ParentImage` vs. `parent_image`, `CommandLine` vs. `command_line`

### Threshold Tuning
- Initial thresholds (e.g., "5 failed logons") are starting points
- Adjust based on environment baseline (normal user behavior, service accounts, etc.)
- Use `notes/failed_logon_investigation.md` to document tuning decisions

---

## Success Metrics

- [ ] Splunk ingests all expected event types (Windows, Sysmon) with <5 min latency
- [ ] Wazuh agent is connected and reporting without errors
- [ ] Time drift between Splunk and endpoint is <1 second
- [ ] Each detection search fires reliably on controlled attack simulation
- [ ] SOC 1/2 workflows are documented and tested
- [ ] Incident response team can investigate and respond to alerts within SLA

---

## Next Steps

1. Run the pre-validation checklist daily during Phase 1.5
2. Document any ingestion issues in this file
3. Begin populating `splunk/searches/` with tuned queries
4. Prepare attack scenarios in `notes/attack_playbooks.md` (future)
5. Establish alerting and dashboards in Splunk
6. Schedule Phase 3 attack simulation exercises
