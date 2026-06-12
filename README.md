# Cybersecurity Flagship SOC Lab

## Overview

I built this home Security Operations Center (SOC) lab to gain hands-on experience with telemetry collection, detection development, troubleshooting, validation, and incident investigation workflows.

The environment consists of a Windows 11 endpoint running Sysmon, the Splunk Universal Forwarder, and the Wazuh Agent; an Ubuntu monitoring server running Splunk Enterprise, Wazuh Manager, and Chrony; and a Kali Linux system reserved for controlled testing and future attack simulation.

This repository documents the process of building and operating a small SOC environment, including telemetry validation, troubleshooting, detection engineering, and investigation workflow development. Planned, experimental, validated, and completed work are labeled separately to avoid overstating project results.

## Lab Architecture

```text
Kali Linux
Controlled testing and future simulations
                |
                v
Windows 11 Endpoint
Sysmon + Windows Security Events
Splunk Universal Forwarder + Wazuh Agent
                |
                v
Ubuntu Monitoring Server
Splunk Enterprise + Wazuh Manager + Chrony
```

Detailed environment and validation notes are available in the [Lab Overview](docs/lab-overview.md).

## Key Accomplishments

* Built an isolated VirtualBox SOC environment using Windows 11, Ubuntu Linux, and Kali Linux.
* Configured Windows Security Event Log and Sysmon telemetry collection.
* Integrated the Windows endpoint with Splunk Enterprise and Wazuh.
* Validated telemetry ingestion by tracing events from endpoint generation through forwarding, indexing, and search visibility.
* Configured Splunk forwarding over TCP port `9997` and independently verified the receiver, network path, and active forwarding destination.
* Diagnosed events being dropped because the configured `wineventlog` index did not exist.
* Investigated a Sysmon event-channel subscription failure and Splunk Forwarder service interruptions.
* Configured Chrony access rules and validated healthy synchronization after an authorization failure.
* Developed experimental SPL and Sigma content across authentication, execution, persistence, command-and-control, and telemetry-health use cases.
* Published troubleshooting case studies with curated screenshots and evidence-handling guidance.

## Major Troubleshooting Cases

### Splunk Events Dropped by Missing Index

Windows events were reaching Splunk but were not searchable because they were being routed to an unconfigured `wineventlog` index. This demonstrated that forwarder connectivity does not guarantee successful indexing.

[Read the full case study](docs/troubleshooting/missing-index.md)

### Sysmon Channel Subscription Failure

Sysmon events existed locally, but the Splunk Universal Forwarder reported that it could not subscribe to the `Microsoft-Windows-Sysmon/Operational` channel. This reinforced the need to validate telemetry generation, channel access, collection, transport, and indexing independently.

[Read the full case study](docs/troubleshooting/sysmon-channel-permissions.md)

### Chrony Authorization and Time Synchronization

Chrony client requests initially returned `Not authorised`. After reviewing access rules and service behavior, later tracking output showed a healthy synchronization state with normal leap status and minimal clock offset.

[Read the full case study](docs/troubleshooting/time-synchronization.md)

### Splunk Receiver and Forwarder Connectivity

The receiver, network path, and forwarding destination were validated as separate layers: Ubuntu was listening on TCP port `9997`, the Windows endpoint could reach the port, and the Universal Forwarder reported the Splunk server as an active destination.

[Read the full case study](docs/troubleshooting/receiver-and-forwarder-connectivity.md)

Additional documented issues are available in the [Troubleshooting Case-Study Index](docs/troubleshooting/README.md).

## Detection Development

The repository contains experimental detection content that still requires syntax review, field mapping, threshold tuning, and live validation.

| Detection area                                | Primary data source                          | Status                                    |
| --------------------------------------------- | -------------------------------------------- | ----------------------------------------- |
| Failed logons and password spraying           | Windows Security Event ID `4625`             | Experimental                              |
| RDP success after repeated failures           | Windows Security Event IDs `4624` and `4625` | Experimental; sequence validation pending |
| Privileged logon activity                     | Windows Security Event ID `4672`             | Experimental                              |
| Suspicious PowerShell execution               | Sysmon Event ID `1`                          | Experimental                              |
| Suspicious parent-child process relationships | Sysmon Event ID `1`                          | Hunting query                             |
| Registry persistence behavior                 | Sysmon registry telemetry                    | Experimental                              |
| Suspicious DNS or C2-style activity           | Sysmon DNS telemetry                         | Experimental                              |
| Telemetry ingestion health                    | Splunk timestamps and event volume           | Partially implemented                     |

Detection content is organized under:

* [Splunk detections](detections/splunk/)
* [Sigma detections](detections/sigma/)
* [Telemetry health searches](detections/splunk/telemetry/)

## Current Status

| Area                          | Status              | Notes                                                                                                            |
| ----------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Telemetry pipeline            | Partially validated | Core Windows, Splunk, Wazuh, receiver-connectivity, and time-synchronization workflows have been documented.     |
| Troubleshooting documentation | Documented          | Real service, access, connectivity, synchronization, and indexing failures are supported by curated screenshots. |
| Detection engineering         | Experimental        | SPL and Sigma content exists but still requires syntax review, field validation, tuning, and controlled testing. |
| Controlled attack simulation  | Planned             | Kali is provisioned, but end-to-end attack and detection results have not yet been published.                    |
| Completed investigations      | Not yet populated   | Completed cases will be added only after real validation evidence exists.                                        |

## Repository Navigation

* [Lab Overview](docs/lab-overview.md) — environment details, telemetry status, validation guidance, and project notes.
* [Troubleshooting Case Studies](docs/troubleshooting/README.md) — documented ingestion, permissions, service, connectivity, and time-synchronization issues.
* [Response Playbooks](docs/response-playbooks.md) — SOC analyst triage and investigation workflows.
* [Splunk Detections](detections/splunk/) — experimental SPL searches grouped by detection category.
* [Sigma Detections](detections/sigma/) — portable draft rules grouped by detection category.
* [Investigation Templates](investigations/templates/) — reusable analyst documentation templates.
* [Attack Simulations](attack-simulations/) — controlled simulation plans and future observed results.

Evidence preservation and sanitization procedures are documented in [Evidence Handling](docs/evidence-handling.md).

## Next Milestones

* Validate SPL searches against live Splunk field mappings.
* Validate Sigma syntax, metadata, and backend compatibility.
* Build a detection catalog linking searches, rules, playbooks, simulations, and investigations.
* Execute the first controlled authentication simulation.
* Capture sanitized end-to-end detection evidence.
* Complete and publish the first validated investigation case.
* Expand configuration examples for Splunk, Sysmon, Wazuh, and networking.
