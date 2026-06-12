# Telemetry Validation Evidence

This page collects screenshots showing successful lab end states after setup and troubleshooting. The screenshots are included to document working telemetry, connectivity, agent status, and time synchronization without overstating detection or investigation outcomes.

## Splunk Receiver and Forwarder Connectivity

The Ubuntu/Splunk system is listening on TCP port `9997`, the Windows endpoint can reach the receiver, and the Universal Forwarder shows the Splunk receiver as an active forwarding target.

![Splunk receiver listening on TCP 9997](images/network/splunk-receiver-listening-9997.png)

![Windows endpoint connectivity to Splunk TCP 9997](images/network/windows-to-splunk-9997-connectivity.png)

![Splunk Universal Forwarder active forwarding target](images/splunk/forwarder-active-to-splunk-9997.png)

## Windows Event Log Ingestion

Windows Security, Application, and System logs from host `WIN-WS01` are searchable in Splunk.

![Windows event logs ingesting in Splunk](images/splunk/windows-event-logs-ingesting.png)

## Sysmon Telemetry Ingestion

Sysmon Operational telemetry is successfully arriving in Splunk and appears alongside standard Windows event logs.

![Sysmon telemetry ingesting in Splunk](images/splunk/sysmon-telemetry-ingesting.png)

## Wazuh Agent Status

Wazuh shows the Windows endpoint as active. Any older never-connected duplicate agent entry is historical cleanup noise, not the validated endpoint.

![Wazuh agents active status](images/wazuh/wazuh-agents-active.png)

## Time Synchronization Validation

Chrony is synchronized on Ubuntu, and Windows is configured to sync against the lab time source. This supports consistent event correlation across the lab.

![Chrony current source healthy](images/time-sync/chrony-current-source-healthy.png)

![Chrony tracking healthy](images/time-sync/chrony-tracking-healthy.png)

![Windows Chrony sync validation](images/time-sync/windows-chrony-sync-validation.png)

![Windows time source synced](images/time-sync/windows-time-source-synced.png)
