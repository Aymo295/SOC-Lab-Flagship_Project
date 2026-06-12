# Receiver and Forwarder Connectivity

## Summary

This case documents receiver and forwarder connectivity checks for TCP port 9997.

## Symptom

The lab needed to validate that the Splunk receiver was listening, the Windows endpoint could reach it, and the forwarder recognized the configured destination.

## Investigation

Ubuntu socket output showed a listener on `0.0.0.0:9997`. Windows `Test-NetConnection` to `192.168.100.10` on TCP port 9997 succeeded. Splunk Universal Forwarder reported `192.168.100.10:9997` as an active forward server.

## Root Cause

No failure root cause is claimed from these screenshots. They document separate successful validation layers.

## Resolution

The receiver was listening on TCP 9997, the Windows endpoint could connect to the receiver, and the forwarder reported an active forwarding destination.

## Validation

The evidence validates three separate layers: receiver listening, network reachability, and forwarder destination state.

## Engineering Lesson

Receiver listening, TCP reachability, and active forwarder state are related but distinct. All three should be checked before assuming end-to-end ingestion is healthy.

## Evidence

![Ubuntu socket output showing Splunk receiver listening on 0.0.0.0:9997](../images/setup/splunk-receiver/splunk-receiver-listening-9997.png)

*Ubuntu socket output showed a listener on `0.0.0.0:9997`.*

![Windows Test-NetConnection output showing TCP 9997 success to 192.168.100.10](../images/setup/splunk-forwarder/splunk-port-9997-connectivity-success.png)

*Windows `Test-NetConnection` to `192.168.100.10` on TCP port 9997 succeeded.*

![Splunk forwarder active forward server output showing 192.168.100.10:9997](../images/setup/splunk-forwarder/splunk-active-forward-server.png)

*Splunk Universal Forwarder reported `192.168.100.10:9997` as an active forward server.*
