# Sysmon Channel Permissions

## Summary

This case documents a Splunk Universal Forwarder event-channel subscription problem for Sysmon.

## Symptom

The Splunk Universal Forwarder log reported that it could not subscribe to the Windows Event Log channel `Microsoft-Windows-Sysmon/Operational`.

## Investigation

The error was observed in forwarder log output and specifically referenced the Sysmon operational channel.

## Root Cause

The available evidence supports an event-channel subscription or access problem. This phase does not include screenshots proving a permission modification or final Sysmon ingestion validation.

## Resolution

The documented resolution direction is to review the forwarder service account and Windows Event Log channel permissions for `Microsoft-Windows-Sysmon/Operational`.

## Validation

The available validation is limited to the observed access/subscription error. Successful post-fix ingestion is not claimed in this phase.

## Engineering Lesson

Local Sysmon logging and Splunk event-channel subscription are separate requirements. The forwarder must be able to access the channel before it can ingest Sysmon events.

## Evidence

![Splunk Universal Forwarder log showing Sysmon channel subscription access error](../images/troubleshooting/sysmon-permissions/splunk-forwarder-sysmon-access-denied.png)

*The forwarder could not subscribe to `Microsoft-Windows-Sysmon/Operational`, indicating an event-channel access problem.*
