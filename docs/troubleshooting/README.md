# Troubleshooting Evidence

This section documents troubleshooting case studies from the SOC lab telemetry pipeline. Each page separates symptoms, investigation steps, root cause, resolution, validation evidence, and remaining validation limits.

| Case study | Status | Main lesson | Evidence |
|---|---|---|---|
| [Missing Windows event index](missing-index.md) | Validation evidence incomplete | Forwarder connectivity does not prove successful indexing. | Splunk warning showing events dropped because `index=wineventlog` was missing or unavailable. |
| [Splunk forwarder service recovery](splunk-forwarder-service.md) | Partially validated | Forwarder service state, configuration checks, and active receiver status validate different layers. | Service failure, stopped state, configuration check, restart recovery, running service, and active forward server screenshots. |
| [Sysmon channel permissions](sysmon-channel-permissions.md) | Validation evidence incomplete | Local Sysmon activity does not guarantee Splunk can subscribe to the Sysmon event channel. | Splunk Universal Forwarder access/subscription error for `Microsoft-Windows-Sysmon/Operational`. |
| [Time synchronization troubleshooting](time-synchronization.md) | Partially validated | Time sync setup may require iterative authorization, configuration, restart, and tracking checks. | Chrony authorization failure, allow rules, restart failure, and later healthy tracking output. |
| [Heartbeat monitor configuration](heartbeat-monitoring.md) | Partially validated | `btool` helps confirm effective monitor configuration and precedence, but searchable events still require separate validation. | Heartbeat monitor stanza, `btool` precedence output, restart recovery, and loaded stanza evidence. |
| [Splunk Web connectivity](splunk-web-connectivity.md) | Documented | HTTP response and redirect output can validate Splunk Web reachability from a system. | `curl` output showing Splunk Web HTML and redirect to `/en-US/`. |
| [Receiver and TCP 9997 validation](receiver-and-forwarder-connectivity.md) | Documented | Receiver listening, network reachability, and active forwarder destination state are separate validation layers. | Ubuntu listener, Windows TCP connectivity, and active forward server screenshots. |
