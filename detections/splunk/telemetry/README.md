"""
Detection: Telemetry Health & Ingestion Monitoring
Purpose: Monitor Splunk ingestion health, source silence, and time drift
Detection Method: Meta-search and ingestion monitoring
Expected Log Sources: Internal Splunk index, Sysmon, Windows Events

LIVE ADAPTATION REQUIRED:
- Verify host names and sourcetypes match your environment
- Adjust threshold for ingestion delay based on acceptable SLA
- Set time window for silence detection (e.g., 10 minutes)
"""

This folder contains separate telemetry health searches:

- `ingestion-delay.spl` - ingestion delay analysis
- `source-silence.spl` - source silence detection
- `sysmon-event-volume.spl` - Sysmon event count baseline
- `security-event-volume.spl` - Windows Security event volume baseline
