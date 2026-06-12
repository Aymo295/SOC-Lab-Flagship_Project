# Cybersecurity Flagship SOC Lab

This repository documents a home SOC lab focused on telemetry validation, detection engineering, controlled testing, and analyst workflow development. The lab uses Splunk, Wazuh, Sysmon, Windows Security events, a monitored Windows endpoint, an Ubuntu monitoring server, and a Kali system reserved for controlled simulations.

The repository also records engineering lessons from configuring, troubleshooting, and validating the telemetry pipeline.

The project is intentionally evidence-driven. Planned work, draft detections, and validation tasks are separated from completed findings so the repository does not overstate results.

## Lab Architecture

- **Ubuntu monitoring server:** Splunk Enterprise, Wazuh Manager, and Chrony.
- **Windows endpoint:** Windows 11 Enterprise with Sysmon, Splunk Universal Forwarder, and Wazuh Agent.
- **Kali system:** isolated node for future controlled simulations.

## Current Status

| Area | Status | Notes |
|---|---|---|
| Telemetry pipeline | Partially validated | Sysmon Event ID 1 ingestion, Windows Security event forwarding, Wazuh connectivity, network isolation, firewall configuration, and time synchronization have been documented as validated. Ongoing work remains for ingestion delay, heartbeat, source silence, and drift monitoring. |
| Detection engineering | Experimental | SPL and Sigma content is organized by detection category. Searches and rules still require syntax review, field mapping, tuning, and live validation against lab telemetry. |
| Controlled attack simulation | Planned | Controlled attack simulations and completed investigations have not yet been published. Results will be added only after execution, validation, and sanitization. |
| Evidence handling | Draft guidance | Evidence handling procedures exist, but raw telemetry and private evidence must not be committed. |
| Completed investigations | Not yet populated | Completed cases will be added only after real validation evidence exists. |

## Repository Navigation

- [Lab overview](docs/lab-overview.md) - environment summary, telemetry status, validation checklist, troubleshooting, and next steps.
- [Troubleshooting evidence](docs/troubleshooting/README.md) - documented setup and telemetry troubleshooting case studies with curated screenshots.
- [Response playbooks](docs/response-playbooks.md) - SOC 1 and SOC 2 triage workflows for the planned detection areas.
- [Evidence handling](docs/evidence-handling.md) - guidance for exporting, preserving, and sanitizing investigation evidence.
- [Splunk detections](detections/splunk/) - experimental SPL searches grouped by detection category.
- [Sigma detections](detections/sigma/) - portable draft detection rules grouped by detection category.
- [Telemetry health searches](detections/splunk/telemetry/) - separate SPL searches for ingestion delay, source silence, and event-volume baselines.
- [Investigation templates](investigations/templates/) - reusable investigation documentation templates.
- [Completed investigations](investigations/completed/) - validated investigation records with sanitized supporting evidence will be added here.
- [Attack simulations](attack-simulations/) - controlled simulation plans and observed results will be documented here after execution.
- [Evidence publication area](evidence/) - guidance and repository locations for sanitized investigation artifacts.
- [Utility scripts](scripts/python/) - supporting scripts for lab workflows.

## Project Phases

1. **Telemetry validation** - confirm endpoint, Splunk, Wazuh, and time-synchronization behavior.
2. **Detection engineering** - organize and tune experimental SPL and Sigma detections.
3. **Controlled simulation** - execute safe attack scenarios only when ready, then validate detections against real lab telemetry.
4. **Investigation and response** - document confirmed findings, analyst decisions, evidence, and business impact.
5. **Automation and dashboards** - build repeatable reporting and monitoring once the underlying detections are validated.

## Detection Areas

The lab is organized around these planned detection themes:

- Failed logon and password spray activity.
- Successful RDP logon after repeated failures.
- Privileged logon anomalies.
- Suspicious PowerShell execution.
- Suspicious parent-child process chains.
- DNS tunneling or C2-style communication.
- Registry persistence behavior.
- Telemetry health and ingestion reliability.

## Evidence and Privacy Rules

- Do not commit raw telemetry, private logs, screenshots with sensitive data, credentials, tokens, or public IP addresses.
- Store private evidence outside the repository or sanitize it before publication.
- Add completed investigations only after real validation evidence exists.
- Keep detection status accurate: draft, experimental, validated, or completed.

## Manual Validation Still Required

- Confirm SPL syntax and field mappings in the live Splunk environment.
- Confirm Sigma rule syntax and intended backend compatibility.
- Run controlled simulations before claiming detection validation.
- Capture and sanitize evidence before publishing screenshots or investigation writeups.
- Review any lab-specific IP addresses or hostnames before public release.

## References

- [MITRE ATT&CK](https://attack.mitre.org/)
- [Sigma project](https://github.com/SigmaHQ/sigma)
- Windows Security Event IDs: 4625, 4624, 4672.
- Sysmon Event IDs: 1, 10, 12, 13, 22.

## Project Owner

Aaron Oldham
