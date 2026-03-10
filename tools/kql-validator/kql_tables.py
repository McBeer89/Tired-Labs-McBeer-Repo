"""Known KQL table names and their properties.

Provides sets of recognized table names for Sentinel and Defender,
along with a mapping of which time field each table uses.
"""

SENTINEL_TABLES = {
    "SecurityEvent",
    "SysmonEvent",
    "Event",
    "W3CIISLog",
    "SigninLogs",
    "AuditLogs",
    "AADNonInteractiveUserSignInLogs",
    "CommonSecurityLog",
    "Syslog",
    "Usage",
    "Heartbeat",
    "Perf",
    "IdentityLogonEvents",
    "IdentityDirectoryEvents",
    "IdentityQueryEvents",
}

DEFENDER_TABLES = {
    "DeviceProcessEvents",
    "DeviceFileEvents",
    "DeviceRegistryEvents",
    "DeviceImageLoadEvents",
    "DeviceNetworkEvents",
    "DeviceLogonEvents",
    "DeviceEvents",
    "IdentityLogonEvents",
    "IdentityDirectoryEvents",
    "IdentityQueryEvents",
    "AlertInfo",
    "AlertEvidence",
}

ALL_KNOWN_TABLES = SENTINEL_TABLES | DEFENDER_TABLES

# Tables that appear in both Sentinel and Defender (Identity tables)
# use different time fields depending on the workspace context.
# For these, we accept either TimeGenerated or Timestamp.
DUAL_TABLES = SENTINEL_TABLES & DEFENDER_TABLES

# Mapping: table name -> expected time field name.
# Tables in DUAL_TABLES accept either field, so they are omitted here.
SENTINEL_TIME_FIELD = "TimeGenerated"
DEFENDER_TIME_FIELD = "Timestamp"

# Sentinel-only tables use TimeGenerated
SENTINEL_ONLY_TABLES = SENTINEL_TABLES - DUAL_TABLES
# Defender-only tables use Timestamp
DEFENDER_ONLY_TABLES = DEFENDER_TABLES - DUAL_TABLES


def expected_time_field(table_name: str) -> str | None:
    """Return the expected time field for a table, or None if unknown/dual."""
    if table_name in SENTINEL_ONLY_TABLES:
        return SENTINEL_TIME_FIELD
    if table_name in DEFENDER_ONLY_TABLES:
        return DEFENDER_TIME_FIELD
    # Dual tables or unknown tables: no single expected field
    return None
