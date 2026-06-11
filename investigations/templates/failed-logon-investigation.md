# Incident Response: Failed Logon Investigation

This document serves as a template and exercise for incident response analysis. Use this format when investigating any alert from the SOC lab.

---

## Executive Summary

**Status**: [Investigation In Progress / Resolved / Escalated]

**Incident Title**: [Brief title, e.g., "Suspected Password Spray Attack on WIN-WS01"]

**Detection Method**: [e.g., "4625 Password Spray detection from Splunk search"]

**Timeline**: [Start time] - [End time / Ongoing]

**Affected Systems**: [Hosts, IP addresses, accounts]

**Initial Assessment**: [1-2 sentences on severity and immediate action taken]

---

## Technical Summary

### Detection Details
- **Alert Name**: [Detection that fired, e.g., "4625_password_spray"]
- **Alert Threshold**: [Condition that triggered, e.g., ">5 failed logons from same source in 10 minutes"]
- **First Alert Time**: [Timestamp]
- **Last Alert Time**: [Timestamp or Ongoing]
- **Source System**: [e.g., "WIN-WS01"]

### Observed Indicators
- **Source IP Address**: [IP that initiated attack, if applicable]
- **Targeted Accounts**: [List of accounts targeted, e.g., admin, user1, user2, ...]
- **Success/Failure Ratio**: [e.g., "25 failed logons, 0 successful"]
- **Attack Vector**: [e.g., RDP brute-force, LDAP enumeration, etc.]

### Event Data
- **Windows Event ID(s)**: [e.g., 4625 for failed logon]
- **Sysmon Event ID(s)**: [If Sysmon was involved, e.g., 1, 10, 22]
- **Other Log Sources**: [e.g., Wazuh alerts, network flows]

---

## MITRE ATT&CK Mapping

| Phase | Technique | Tactic ID | Description |
|---|---|---|---|
| Initial Access | Password Spray | T1110.003 | Repeated failed logons on multiple accounts |
| Execution | PowerShell | T1059.001 | Suspicious PowerShell command execution (if found) |
| Credential Access | LSASS Memory Dump | T1003.001 | Process access on LSASS (if found) |
| Persistence | Registry Run Key | T1112 / T1547 | Registry modification for startup persistence (if found) |
| Command & Control | DNS Tunneling | T1071.004 | Suspicious DNS queries (if found) |

---

## Investigation Timeline

| Time | Source | Event | Details | Analyst |
|---|---|---|---|---|
| [T+0 min] | Splunk Alert | Alert fired | Password spray detected | [SOC 1 analyst] |
| [T+5 min] | SOC 1 Triage | Initial validation | Confirmed repeated 4625 events | [SOC 1 analyst] |
| [T+10 min] | Splunk Query | Success check | Searched for 4624 success events | [SOC 1 analyst] |
| [T+15 min] | SOC 2 Escalation | Escalated to SOC 2 | No successful logon found; escalated for deeper analysis | [SOC 1 analyst] |
| [T+30 min] | Threat Intel | IP reputation | IP checked against VirusTotal, no known issues | [SOC 2 analyst] |
| [T+45 min] | Forensics | Evidence collection | Process dumps captured for offline analysis | [SOC 2 analyst] |

---

## Evidence & Artifacts

### Search Queries Used
```splunk
# Password spray detection
index=wineventlog host=WIN-WS01 EventCode=4625
| stats count by Account_Name, Source_Network_Address, host
| where count >= 5
| sort - count

# Check for successful logons after failures
index=wineventlog host=WIN-WS01 EventCode=4624
Source_Network_Address=<SOURCE_IP> earliest=<ATTACK_START>
| stats count by Account_Name, Logon_Type, Source_Network_Address
| sort - count

# Process creation on target account (if applicable)
index=sysmon host=WIN-WS01 EventID=1
User=<ACCOUNT> earliest=<ATTACK_START>
| fields _time, User, Image, CommandLine, ParentImage, ParentCommandLine
| sort _time
```

### Captured Events
- **Event Count**: [e.g., 25 failed logon events]
- **Event Export**: [Link or attachment to exported search results]
- **Log Files**: [Any raw log files captured]
- **Process Dumps**: [Memory dumps, if applicable]

### Threat Intelligence
- **Source IP Reputation**: [e.g., "Not flagged in VirusTotal, abuse.ch, or internal threat feeds"]
- **Domain Reputation** (if C2 suspected): [e.g., "Known malicious C2 domain per URLhaus"]
- **File Hash Reputation** (if malware found): [e.g., "Unknown file, submitted to VirusTotal"]

---

## Root Cause Analysis

### Attack Chain
1. **Initial Access**: Attacker located target and enumerated accounts
   - Source: [External IP / Internal IP / VPN]
   - Method: [RDP brute-force / LDAP / Kerberos spray]
   - Duration: [Time from first to last attempt]

2. **Exploitation** (if successful): [Describe how attacker gained access]
   - Which account was compromised?
   - How was access obtained (credentials leaked, MFA bypass)?

3. **Post-Compromise Activity** (if applicable): [Describe what attacker did]
   - Privilege escalation?
   - Lateral movement?
   - Data access?
   - Persistence mechanism?

### Contributing Factors
- [ ] Weak or default passwords
- [ ] No MFA enforcement
- [ ] Lack of rate limiting on logon attempts
- [ ] Excessive account exposure / RDP exposed to internet
- [ ] Delayed detection or monitoring gap
- [ ] Insufficient logging or alerting

### Why Detection Occurred
- Splunk search threshold exceeded (e.g., >5 failed logons from same source in 10 min)
- Pattern matched known attack signature
- Anomaly detection rule triggered

---

## Detection Gaps & Improvements

### What Worked
- [e.g., "Splunk alert fired correctly within 2 minutes of attack"]
- [e.g., "All event logs were properly forwarded and indexed"]

### What Didn't Work / Gaps
- [ ] Detection delay (how long before alert fired?)
- [ ] False positives (any alerts that were not true positives?)
- [ ] Missing context (what additional data would have helped?)
- [ ] Incomplete logging (were all relevant events captured?)
- [ ] Correlation gaps (did we miss lateral movement?)

### Improvements to Implement
1. [e.g., "Enable MFA on all high-value accounts within 2 weeks"]
2. [e.g., "Increase Sysmon Event ID 10 (LSASS access) monitoring sensitivity"]
3. [e.g., "Add alert for RDP logon success immediately after failures"]
4. [e.g., "Implement DNS query baselining and anomaly alerting"]
5. [e.g., "Review and remove excessive RDP exposure"]

---

## Business Impact

### Confidentiality Risk
- [ ] Potential credential exposure
- [ ] Potential data access by unauthorized user
- Estimated exposure: [e.g., "None if attack was unsuccessful"]

### Integrity Risk
- [ ] Potential unauthorized changes to systems or data
- [ ] Potential malware/persistence installation
- Estimated risk: [e.g., "Low if no successful logon occurred"]

### Availability Risk
- [ ] Potential system unavailability or service disruption
- [ ] Potential ransom-ware or destructive malware
- Estimated risk: [e.g., "Low; no service disruption observed"]

### Overall Severity Assessment
- **Risk Score**: [1-10, where 10 is critical]
- **Justification**: [e.g., "Score 3/10 because attack was unsuccessful and detected within SLA"]

---

## Corrective Actions

### Immediate (0-24 hours)
- [ ] Reset passwords for targeted accounts
- [ ] Enable MFA for all high-value accounts
- [ ] Block source IP at firewall if external
- [ ] Increase monitoring on targeted accounts for 7 days
- [ ] Notify account owners

### Short-term (1-2 weeks)
- [ ] Review and audit RDP exposure and access controls
- [ ] Implement network-based rate limiting on failed logon attempts
- [ ] Strengthen password policies or enforce longer passwords
- [ ] Enable and tune process creation logging (Sysmon Event ID 1)
- [ ] Review and validate MFA implementation

### Long-term (1-3 months)
- [ ] Implement Just-In-Time (JIT) privileged access
- [ ] Deploy endpoint protection / EDR on all critical systems
- [ ] Implement conditional access policies
- [ ] Increase security awareness training
- [ ] Conduct penetration testing on authentication mechanisms
- [ ] Review and harden DNS security

### Assigned Owner & Due Date
| Action | Owner | Due Date | Status |
|---|---|---|---|
| Reset passwords for targeted accounts | [Identity team] | [Date] | [ ] |
| Enable MFA | [Access mgmt] | [Date] | [ ] |
| Block IP at firewall | [Network team] | [Date] | [ ] |
| Review RDP exposure | [Network security] | [Date] | [ ] |

---

## Lessons Learned

### What Did the Team Do Well?
- [e.g., "Detection alert fired quickly"]
- [e.g., "SOC 1 validated alert within SLA"]
- [e.g., "Good coordination between teams during response"]

### What Could Be Improved?
- [e.g., "Alert could have included more context in the title"]
- [e.g., "Playbook was not clear on escalation criteria"]
- [e.g., "Took too long to coordinate with Identity team"]

### Team Feedback
- [SOC 1 analyst]: [Comments on alert, detection, process]
- [SOC 2 analyst]: [Comments on investigation, escalation]
- [Incident responder]: [Comments on response and remediation]

### Updated Procedures
- [ ] Playbook refined based on lessons learned
- [ ] Training scheduled for [team]
- [ ] Alert tuning completed
- [ ] Documentation updated

---

## Approval & Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| SOC 1 Analyst | [Name] | [Date] | ☐ |
| SOC 2 Analyst | [Name] | [Date] | ☐ |
| Incident Response Lead | [Name] | [Date] | ☐ |
| Security Manager | [Name] | [Date] | ☐ |

---

## Attachments

- [ ] Splunk search export (CSV)
- [ ] Process dumps or memory captures
- [ ] Full event logs
- [ ] Network traffic capture (if available)
- [ ] Forensic report (if applicable)
- [ ] Threat intelligence report
- [ ] Updated playbook or procedures

---

## References

- MITRE ATT&CK: https://attack.mitre.org/
- Windows Event Log Guide: https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/audit-failure-logon-events
- Sysmon Documentation: https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon
- Incident Response Framework: [Link to internal IR policy]

---

*This document should be completed during and immediately after an incident investigation. Use it to document findings, improve detections, and build institutional knowledge.*
