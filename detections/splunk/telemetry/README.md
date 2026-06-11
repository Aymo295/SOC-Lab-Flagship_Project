# Telemetry Health and Ingestion Monitoring

## Purpose

Monitor Splunk ingestion health, source silence, and event-volume baselines.

## Live adaptation required

- Verify hostnames and sourcetypes.
- Adjust ingestion-delay thresholds.
- Configure the silence-detection window.

## Searches

- `ingestion-delay.spl` - calculates `_indextime - _time` for each sourcetype to detect ingestion lag.
- `source-silence.spl` - calculates the time since each source last reported so a silence threshold can be applied during validation.
- `sysmon-event-volume.spl` - monitors Sysmon event ingestion for event-volume baselining.
- `security-event-volume.spl` - monitors Windows Security event ingestion for event-volume baselining.
