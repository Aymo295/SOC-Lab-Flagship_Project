# SOC Response Playbooks

This document outlines SOC 1 and SOC 2 analyst workflows for each detection type in the lab environment. SOC 1 focuses on rapid triage, validation, and initial containment; SOC 2 focuses on deeper investigation, correlation, and strategic escalation.

---

## Password Spray / Failed Logon Detection (4625)

### Alert Trigger
- Detection: `4625_password_spray.spl`
- Condition: ≥5 failed logons from same source IP targeting multiple accounts in 10 minutes

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Verify the alert is legitimate (not a scan, vulnerability assessment, or known process)
   - Check if source IP is known internal IP or external
   - Check if targeted accounts include service accounts, disabled accounts, or high-value targets
2. Identify the source IP and determine if it is expected
   - Is this a known employee device, VPN, or internal server?
   - Is this an external IP?
3. Check if any logons succeeded after the failures
   - Query: `index=wineventlog host=WIN-WS01 EventCode=4624 Source_Network_Address=<source_ip>`
   - If successes found, escalate to SOC 2 immediately

**Containment Options (if attack confirmed)**
- [ ] Temporarily disable targeted accounts (coordinate with Identity team)
- [ ] Reset passwords for compromised accounts
- [ ] Block source IP at firewall if external
- [ ] Isolate the endpoint if local attack (e.g., WS01 from domain)

**Documentation**
- [ ] Record source IP, targeted accounts, timestamp
- [ ] Note number of failures and success/failure ratio
- [ ] Capture alert output and search results

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Correlate with threat intelligence
   - Is the source IP known for password spray attacks?
   - Is there active threat hunting data on this IP?
2. Determine attacker objective
   - Which accounts were targeted? (service accounts, admins, generic users?)
   - Does targeting suggest insider knowledge?
3. Estimate dwell time and exposure
   - When did the attack begin and end?
   - Were any accounts compromised during this window?
4. Collect and preserve evidence
   - Export full event logs for forensics
   - Capture network traffic if available (Wazuh, Sysmon network events)

**Escalation Path**
- [ ] Notify Identity and Access Management team
- [ ] Notify Network Security team if IP blocking needed
- [ ] Escalate to incident response if compromise suspected
- [ ] Update threat intelligence feed with attacker IP

**Follow-up Actions**
- [ ] Enable MFA on high-value accounts if not already enabled
- [ ] Increase monitoring for accounts targeted in the attack
- [ ] Review and strengthen password policies
- [ ] Document lessons learned in incident writeup

---

## Successful RDP Logon After Failed Attempts (4624)

### Alert Trigger
- Detection: `4624_rdp_success.spl`
- Condition: Logon Type 10 (RDP) following ≥5 failed logons from same source IP in previous 15 minutes

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Verify the successful logon
   - Check source IP, account name, logon time
   - Determine if logon is expected (e.g., administrator, support team)
2. Check account activity after successful logon
   - Query: `index=wineventlog host=WIN-WS01 EventCode=4688 Account_Name=<account>`
   - Look for process creation events, privilege escalation, unusual commands
3. Determine if source IP is expected
   - Internal IP? External? VPN?
   - Known location? Unusual geolocation?

**Containment Options (if attack confirmed)**
- [ ] Disconnect RDP session immediately
- [ ] Reset password for compromised account
- [ ] Force logout from all sessions
- [ ] Block source IP at firewall
- [ ] Isolate endpoint from network if evidence of malicious activity

**Documentation**
- [ ] Record account, source IP, logon time, session duration
- [ ] Capture all process creation events from that session
- [ ] Document any lateral movement attempts

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Analyze post-compromise activity
   - What processes were executed?
   - What files were accessed or modified?
   - Any evidence of credential dumping (mimikatz, procdump)?
   - Any evidence of lateral movement?
2. Determine attack objective
   - Was the account a stepping stone or the final target?
   - Did the attacker establish persistence?
3. Assess lateral movement risk
   - Can the compromised account access other systems?
   - Are there sensitive data stores accessible from this account?

**Escalation Path**
- [ ] Notify Identity and Access Management
- [ ] Escalate to incident response if lateral movement detected
- [ ] Notify stakeholders of compromised account
- [ ] Preserve forensic evidence for root cause analysis

**Follow-up Actions**
- [ ] Implement conditional access policies
- [ ] Require MFA for RDP sessions
- [ ] Monitor for re-compromise using the same account
- [ ] Review and harden RDP exposure (NAT, port changes, VPN-only)

---

## Privileged Logon Anomaly (4672)

### Alert Trigger
- Detection: `4672_privileged_logon.spl`
- Condition: EventCode 4672 from unusual account, host, or logon type

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Verify the account performing privileged operation
   - Is this a known service account, admin, or unexpected?
   - What operation is being performed?
2. Check if the privilege escalation is expected
   - Scheduled task? Batch process? Manual admin action?
   - Timing and frequency consistent with baseline?
3. Check for post-escalation activity
   - What did the privileged process do?
   - File modifications? Registry changes? Network connections?

**Containment Options (if attack confirmed)**
- [ ] Disable or quarantine the service account
- [ ] Reset password and re-authorize access
- [ ] Revoke elevated privileges temporarily
- [ ] Isolate the endpoint if evidence of misuse

**Documentation**
- [ ] Record privileged account, operation, timestamp
- [ ] Capture all activity performed under elevated privilege
- [ ] Note any lateral movement or data access

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Determine legitimacy of privilege escalation
   - Owner of account? Expected operation?
   - Approval workflow? Change management record?
2. Analyze privilege abuse risk
   - What sensitive data or systems became accessible?
   - Did the privilege holder compromise data or systems?
3. Check for persistence mechanisms
   - Did the escalation install scheduled tasks, services, registry entries?
   - Evidence of backdoor or remote access tool?

**Escalation Path**
- [ ] Notify account owner and manager
- [ ] Escalate to incident response if abuse confirmed
- [ ] Notify access control team for privilege review
- [ ] Document policy violations

**Follow-up Actions**
- [ ] Implement Just-In-Time (JIT) privileged access if not already in place
- [ ] Strengthen logging and alerting on privileged account usage
- [ ] Review access approvals and compliance
- [ ] Implement privilege escalation monitoring via Splunk or EDR

---

## Suspicious PowerShell Execution (Sysmon Event ID 1)

### Alert Trigger
- Detection: `sysmon_powershell_abuse.spl`
- Condition: Sysmon Event ID 1 with CommandLine containing: `-EncodedCommand`, `Invoke-Expression`, `DownloadString`, `IEX`, base64, or other obfuscation

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Capture the full PowerShell command line
   - Decode base64 if present
   - Examine syntax and intent
   - Look for obvious malicious indicators
2. Check context: who ran PowerShell and why?
   - User account? Service account?
   - Parent process (explorer.exe? cmd.exe? outlook.exe?)?
   - Timing and frequency?
3. Determine if process is still running
   - `tasklist | findstr powershell.exe` on WIN-WS01
   - If running, capture network connections and file handles

**Containment Options (if attack confirmed)**
- [ ] Kill the PowerShell process
- [ ] Isolate the endpoint from network
- [ ] Preserve process dump for analysis
- [ ] Reset user password

**Documentation**
- [ ] Record full command line (including encoded payload if possible to decode)
- [ ] Capture parent process, user, timestamp
- [ ] Document network connections and file access

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Decode and analyze the PowerShell payload
   - What is the intent? (C2 beacon? Credential dumping? Data exfil?)
   - What frameworks are used? (Empire? Cobalt Strike? Custom?)
2. Determine if attacker achieved execution
   - Network connections made?
   - Files downloaded or executed?
   - Persistence mechanisms installed?
3. Correlate with attack timeline
   - Does this follow a successful RDP logon?
   - Parent process = cmd.exe (chained execution)?

**Escalation Path**
- [ ] Escalate to incident response immediately
- [ ] Notify endpoint protection / EDR team
- [ ] Preserve forensic evidence (memory dump, disk capture)
- [ ] Prepare for full incident investigation

**Follow-up Actions**
- [ ] Enable PowerShell script block logging and auditing
- [ ] Implement Constrained Language Mode or AppLocker policies
- [ ] Increase monitoring on PowerShell Event ID 4104 (script block logs)
- [ ] Review and remove any persistence mechanisms found

---

## Parent-Child Process Abuse (Sysmon Event ID 1 Process Chains)

### Alert Trigger
- Detection: `sysmon_parent_child_process.spl`
- Condition: Suspicious parent-child relationships (e.g., PowerShell → cmd, wmic, regsvcs, mshta)

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Verify the parent-child relationship is suspicious
   - Is PowerShell spawning cmd.exe expected? Why?
   - Is cmd.exe spawning wmic.exe expected? Why?
   - Is explorer.exe spawning cmd.exe expected? (No, this is suspicious)
2. Check the process command lines
   - What arguments are being passed?
   - Any encoded commands or suspicious paths?
3. Determine if chain is still active
   - Are the parent and child processes still running?
   - Are they communicating (network connections)?

**Containment Options (if attack confirmed)**
- [ ] Kill the process chain (kill child first, then parent)
- [ ] Capture process handles and network connections before killing
- [ ] Isolate endpoint from network
- [ ] Preserve forensic evidence

**Documentation**
- [ ] Record parent and child process names, PIDs, command lines
- [ ] Capture all network connections from the process chain
- [ ] Document file access and registry modifications

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Analyze the attack objective
   - Is cmd being used for data enumeration? (dir, net.exe, ipconfig)
   - Is wmic being used for lateral movement or WMI events?
   - Is mshta being used for UAC bypass or malware download?
2. Determine lateral movement risk
   - Did the process chain access network shares?
   - Did it enumerate Active Directory or local groups?
3. Check for persistence
   - Did any child processes install registry entries, services, or scheduled tasks?

**Escalation Path**
- [ ] Escalate to incident response
- [ ] Notify endpoint security team
- [ ] Prepare for full forensic analysis

**Follow-up Actions**
- [ ] Enable Sysmon Event ID 10 (Process Access) monitoring for LSASS
- [ ] Implement process allowlisting / AppLocker for suspicious parent-child chains
- [ ] Increase monitoring on cmd.exe and wmic.exe execution
- [ ] Review and strengthen execution policy (e.g., PowerShell, script execution)

---

## DNS Tunneling / C2 Communication (Sysmon Event ID 22)

### Alert Trigger
- Detection: `sysmon_dns_tunneling.spl`
- Condition: Sysmon Event ID 22 (DNS query) with high volume, unusual hostnames, subdomain patterns, or TXT record queries from unusual processes

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Identify the source process making DNS queries
   - Which executable? Unusual process? (DNS from chrome.exe is normal; from svchost.exe may not be)
   - What user context?
2. Examine the DNS queries
   - Are they to known CDNs, cloud services, or unknown domains?
   - Do hostnames suggest data exfiltration? (e.g., `<base64>.attacker.com`)
   - Query frequency? (Bursts? Consistent beacon?)
3. Check endpoint DNS resolver logs
   - Are queries being resolved or failing?
   - Any DNS sinkhole blocks?

**Containment Options (if attack confirmed)**
- [ ] Block egress DNS to known attacker domain
- [ ] Isolate endpoint from network
- [ ] Kill the suspicious process
- [ ] Reset DNS resolver to block external queries

**Documentation**
- [ ] Record source process, user, query names, destination IPs
- [ ] Capture query frequency and timing patterns
- [ ] Document any resolved destination IPs and geolocation

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Perform DNS and threat intelligence lookup
   - Is the domain known C2? Check VirusTotal, abuse.ch, Shodan
   - Whois registration? Hosting provider? Geolocation?
2. Analyze query patterns for C2 beaconing
   - Is there a regular interval? (e.g., every 5 minutes = beacon)
   - Volume of queries? (Large volume = data exfiltration?)
3. Correlate with other detections
   - Does DNS tunneling follow a successful RDP logon?
   - Does it coincide with PowerShell execution or process chains?

**Escalation Path**
- [ ] Escalate to incident response and network security
- [ ] Notify DNS/network team for domain blocking
- [ ] Preserve DNS query logs for forensics
- [ ] Prepare for C2 takedown coordination if applicable

**Follow-up Actions**
- [ ] Implement DNS query monitoring and allowlisting
- [ ] Block external DNS queries to unknown domains via firewall/DNS sinkhole
- [ ] Enable Sysmon Event ID 22 (DNS Query) monitoring
- [ ] Consider DNS-based content filtering / DNS security service (e.g., Cisco Umbrella)

---

## Registry Persistence Modification (Sysmon Event ID 12/13)

### Alert Trigger
- Detection: `sysmon_registry_persistence.spl`
- Condition: Sysmon Event ID 12/13 (Registry Create/Set) under persistence keys: `HKLM\Software\Microsoft\Windows\Run`, `CurrentVersion\RunOnce`, etc.

### SOC 1 (Triage & Containment)

**Immediate Actions**
1. Identify the source process creating/modifying registry
   - Which executable? User context?
   - Is this a known installer or legitimate process?
2. Examine the registry modification
   - What value is being set? What does it point to?
   - Is it a file path? Command? Encoded payload?
3. Check if the referenced file exists
   - Does the binary exist at the path specified?
   - Can you capture a copy for analysis?

**Containment Options (if attack confirmed)**
- [ ] Delete the malicious registry entry
- [ ] Delete or quarantine the referenced file
- [ ] Reboot the endpoint to prevent persistence loading
- [ ] Isolate endpoint from network

**Documentation**
- [ ] Record registry key, value name, data/target
- [ ] Capture source process and user
- [ ] Document file path and file hash (MD5/SHA256)

### SOC 2 (Investigation & Escalation)

**Deep Investigation**
1. Analyze persistence mechanism
   - What is the intent? (Remote access? Worm propagation? Backdoor?)
   - What binary will be executed at next boot?
2. Check for additional persistence mechanisms
   - Search for other registry entries set by the same process
   - Check for scheduled tasks, services, startup folders
3. Determine persistence scope
   - User-level persistence (HKCU) or system-level (HKLM)?
   - Will it survive reboot? User logoff?

**Escalation Path**
- [ ] Escalate to incident response and forensics
- [ ] Notify endpoint security / EDR team
- [ ] Preserve registry hive and malicious binary for analysis
- [ ] Prepare for full forensic investigation

**Follow-up Actions**
- [ ] Enable registry modification monitoring and alerting
- [ ] Implement registry allowlisting for persistence keys
- [ ] Use endpoint protection to prevent unauthorized registry writes
- [ ] Document persistence patterns in threat hunting rules
- [ ] Educate users on suspicious installs and registry changes

---

## Incident Response Escalation Matrix

| Alert Type | Severity | SOC 1 Max Hold | Escalate If | SOC 2 Required |
|---|---|---|---|---|
| Password spray | Medium | 15 min | Success logon or >20 accounts | Yes |
| RDP success | High | 5 min | Success after failures | Yes |
| Privileged logon | Medium | 10 min | Unusual account or operation | Yes |
| PowerShell abuse | High | 5 min | Encoded/suspicious command | Yes |
| Process chain | High | 5 min | Suspicious parent/child | Yes |
| DNS tunneling | High | 5 min | C2-like patterns | Yes |
| Registry persistence | Critical | 3 min | Any suspicious persistence | Yes |

---

## Common Questions During Triage

**Q: Is this a false positive?**
- A: Check against known baselines (e.g., admin activities, service accounts, known scripts)
- Correlate with change management or deployment windows
- When in doubt, escalate to SOC 2

**Q: What's the user context?**
- A: Check if account is human, service, or system
- Verify account has legitimate business purpose
- Check if account access is unexpected (unusual time/location)

**Q: Is this lateral movement?**
- A: Check source and destination hosts
- Verify credentials used (local vs. domain)
- Look for further stage attacks (C2, persistence, data access)

**Q: Should I isolate the endpoint?**
- A: Isolate if: confirmed malicious activity, unknown risk, or ongoing investigation
- Coordinate with business owners before isolation
- Preserve forensic evidence before remediation

**Q: How do I preserve evidence?**
- A: Capture event logs, process dumps, network connections
- Use Splunk export to save full event context
- Document chain of custody
- Coordinate with forensics/IR team for full disk capture if needed

---

## Next Steps

1. Test each playbook with simulated alerts
2. Refine based on your Splunk environment and event data
3. Train SOC analysts on escalation criteria
4. Document lessons learned from each incident
5. Update playbooks iteratively based on real-world incidents
