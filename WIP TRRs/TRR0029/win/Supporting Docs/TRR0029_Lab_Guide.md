# TRR0029 Lab Verification Guide

## Purpose

Three claims in TRR0029 required lab validation before the TRR could be
finalized. All three were factual assertions about telemetry behavior that
directly affect DDM accuracy and procedure differentiation. A fourth test
(EID 29 scope) was added during execution since the infrastructure was already
deployed. Lab testing was completed on 2026-03-04.

| # | Claim to Verify | TRR Impact if Wrong |
|---|-----------------|---------------------|
| 1 | Sysmon 7 (ImageLoad) fires when the CLR loads a disk-backed .NET assembly into `w3wp.exe` | Procedure B loses its Sysmon 7 telemetry coverage — a gap that must be documented |
| 2 | A reflectively loaded assembly can independently register into the IIS pipeline via `HttpApplication.RegisterModule()` | Procedure C's DDM may need a "Register Module" operation, or the narrative must clarify that interception is performed by a loader, not the loaded assembly |
| 3 | ETW `Microsoft-Windows-DotNETRuntime` EID 154 (AssemblyLoad_V1) fires for reflective `Assembly.Load(byte[])` loads | If false, Procedure C has ZERO telemetry at the load operation — a complete observability gap that must be documented |
| 4 | EID 29 (IIS Configuration Auditing) fires for direct `web.config` edits | If true, EID 29 covers all module registration paths. If false, EID 29 is API-path only — direct config edits bypass auditing entirely. |

## Environment

- Windows 10/11 Pro (or Server equivalent) with IIS 10.0
- IIS with ASP.NET 4.x enabled
- Sysmon (v15.x or later recommended)
- `csc.exe` (ships with .NET Framework) for compiling test assemblies

## Safety and Reversibility

All test code is benign — no outbound connections, no privilege escalation, no
system modification beyond IIS configuration entries and test files. Everything
is fully reversible:

- Test assemblies are placed in a dedicated test directory
- `web.config` changes are scoped to the test application
- Sysmon configuration changes are reverted in the cleanup phase
- IIS application and app pool are removed in cleanup

A system restore point created before testing provides an additional safety
net, though it should not be needed.

---

## Phase 0: Environment Verification

### Step 0.1 — Verify IIS

```powershell
Get-Service W3SVC
```

If not running, install IIS with ASP.NET support:

```powershell
$features = @(
    "IIS-WebServerRole",
    "IIS-WebServer",
    "IIS-CommonHttpFeatures",
    "IIS-DefaultDocument",
    "IIS-HttpErrors",
    "IIS-StaticContent",
    "IIS-HealthAndDiagnostics",
    "IIS-HttpLogging",
    "IIS-Security",
    "IIS-RequestFiltering",
    "IIS-Performance",
    "IIS-HttpCompressionStatic",
    "IIS-WebServerManagementTools",
    "IIS-ManagementConsole",
    "IIS-ApplicationDevelopment",
    "IIS-ASPNET45",
    "IIS-NetFxExtensibility45",
    "IIS-ISAPIExtensions",
    "IIS-ISAPIFilter"
)
Enable-WindowsOptionalFeature -Online -FeatureName $features -All
```

### Step 0.2 — Verify Sysmon

```powershell
Get-Service Sysmon64
```

If not installed, install Sysmon with a config that enables at minimum:

- EID 7 (ImageLoad) enabled with an include filter on `Image` = `w3wp.exe`
- EID 11 (FileCreate) with include filters for `TRR0029_Lab`, `inetpub`,
  `web.config`, and `applicationHost.config`
- EID 1 (ProcessCreate) with include filters on `w3wp.exe`

If an existing Sysmon config is deployed, verify that Image loading is
enabled — many configs disable it by default. A TRR0029-specific config is
recommended to reduce noise and isolate test telemetry.

Verify with:

```powershell
sysmon64 -c
```

Confirm that `Image loading: enabled` appears in the output and that the
ImageLoad rule includes `w3wp.exe`.

### Step 0.3 — Create Test Directory Structure

```powershell
New-Item -Path "C:\TRR0029_Lab" -ItemType Directory -Force
New-Item -Path "C:\TRR0029_Lab\assemblies" -ItemType Directory -Force
New-Item -Path "C:\TRR0029_Lab\logs" -ItemType Directory -Force
New-Item -Path "C:\TRR0029_Lab\test_app" -ItemType Directory -Force
New-Item -Path "C:\TRR0029_Lab\test_app\bin" -ItemType Directory -Force
```

### Step 0.4 — Create IIS Test Application

Create a dedicated application under Default Web Site so test configuration
changes are isolated:

```powershell
Import-Module WebAdministration
New-WebApplication -Name "trr0029lab" -Site "Default Web Site" `
    -PhysicalPath "C:\TRR0029_Lab\test_app" -ApplicationPool "DefaultAppPool"
```

Verify:

```powershell
Invoke-WebRequest -Uri "http://localhost/trr0029lab/" -UseBasicParsing
```

Expected: 403 (directory listing disabled) or default page. Either confirms the
application is responding.

---

## Phase 1: Test 1 — Sysmon 7 on CLR Disk-Backed Assembly Load

### Objective

Confirm that when the CLR loads a .NET assembly from the `/bin` directory into
`w3wp.exe`, Sysmon 7 (ImageLoad) fires with the assembly path.

### Step 1.1 — Build a Benign Managed Module

Create a minimal `IHttpModule` that does nothing harmful — it writes a
response header to confirm it loaded.

**File:** `C:\TRR0029_Lab\BenignModule.cs`

```csharp
using System;
using System.Web;

public class BenignModule : IHttpModule
{
    public void Init(HttpApplication context)
    {
        context.BeginRequest += OnBeginRequest;
    }

    private void OnBeginRequest(object sender, EventArgs e)
    {
        HttpApplication app = (HttpApplication)sender;
        app.Context.Response.Headers.Add("X-TRR0029-Test", "BenignModule-Loaded");
    }

    public void Dispose() { }
}
```

Compile it:

```powershell
# Use the .NET Framework compiler (ships with Windows)
$csc = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
& $csc /target:library /reference:"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Web.dll" `
    /out:"C:\TRR0029_Lab\assemblies\BenignModule.dll" `
    "C:\TRR0029_Lab\BenignModule.cs"
```

Verify compilation succeeded:

```powershell
Test-Path "C:\TRR0029_Lab\assemblies\BenignModule.dll"
```

### Step 1.2 — Deploy via web.config (Procedure B Path)

Copy the assembly to the application's `/bin` directory:

```powershell
Copy-Item "C:\TRR0029_Lab\assemblies\BenignModule.dll" `
    -Destination "C:\TRR0029_Lab\test_app\bin\BenignModule.dll"
```

Create a `web.config` that registers the module:

```powershell
@'
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <modules>
            <add name="BenignModule" type="BenignModule" />
        </modules>
    </system.webServer>
</configuration>
'@ | Out-File -FilePath "C:\TRR0029_Lab\test_app\web.config" -Encoding UTF8
```

### Step 1.3 — Create Default Page

The test application needs a default page to return a 200 response — without
one, IIS returns 403 (directory listing disabled) and PowerShell's
`Invoke-WebRequest` throws, preventing header inspection.

```powershell
@'
<%@ Page Language="C#" %>
<html><body>
<pre>TRR0029 Lab - OK
Time: <%= DateTime.Now %>
</pre>
</body></html>
'@ | Out-File -FilePath "C:\TRR0029_Lab\test_app\default.aspx" -Encoding UTF8
```

### Step 1.4 — Clear Sysmon Log and Trigger

Clear the Sysmon operational log to isolate test telemetry:

```powershell
wevtutil cl "Microsoft-Windows-Sysmon/Operational"
```

Send a request to trigger the CLR load:

```powershell
$response = Invoke-WebRequest -Uri "http://localhost/trr0029lab/default.aspx" -UseBasicParsing
$response.Headers["X-TRR0029-Test"]
```

Expected: The header `X-TRR0029-Test: BenignModule-Loaded` confirms the module
loaded and executed.

### Step 1.5 — Check Sysmon 7

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" |
    Where-Object { $_.Id -eq 7 } |
    Where-Object { $_.Message -match "BenignModule" -or $_.Message -match "w3wp" } |
    Format-List TimeCreated, Message
```

**Expected result (if TRR claim is correct):**

- Sysmon 7 fires with:
  - Image: `C:\Windows\...\w3wp.exe`
  - ImageLoaded: `C:\TRR0029_Lab\test_app\bin\BenignModule.dll`
  - Signed: `false` (unsigned test assembly)

**If Sysmon 7 does NOT fire:**

- The CLR may not use `NtMapViewOfSection` for `/bin` assemblies
- Procedure B's Sysmon 7 telemetry claim in the TRR must be corrected
- Check if Sysmon config is filtering it out before concluding

### Step 1.6 — Export Evidence

```powershell
wevtutil qe "Microsoft-Windows-Sysmon/Operational" /q:"*[System[(EventID=7)]]" `
    /f:text > "C:\TRR0029_Lab\logs\test1_sysmon7_disk_load.txt"

wevtutil qe "Microsoft-Windows-Sysmon/Operational" /q:"*[System[(EventID=11)]]" `
    /f:text > "C:\TRR0029_Lab\logs\test1_sysmon11_file_creates.txt"
```

Also capture EID 11 (FileCreate) for both the assembly write and the
`web.config` write — these validate Procedures A/B prerequisite telemetry.

---

## Phase 2: Test 2 — Reflective Assembly Load and Pipeline Registration

### Objective

Determine how a reflectively loaded assembly hooks into the IIS pipeline.
Three sub-tests explore the possible mechanisms.

### Step 2.1 — Build a Reflective Loader Page

This ASPX page loads a .NET assembly from a byte array using
`Assembly.Load(byte[])` and attempts to call it. This is the Procedure C
entry point.

**File:** `C:\TRR0029_Lab\test_app\reflective_loader.aspx`

```csharp
<%@ Page Language="C#" %>
<%@ Import Namespace="System.Reflection" %>
<%@ Import Namespace="System.IO" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e)
{
    string action = Request.QueryString["action"];
    if (string.IsNullOrEmpty(action)) {
        Response.Write("TRR0029 Reflective Loader - use ?action=load or ?action=register\n");
        return;
    }

    // Read the assembly bytes from disk (simulating attacker delivering bytes)
    string dllPath = Server.MapPath("~/bin/BenignModule.dll");
    byte[] assemblyBytes = File.ReadAllBytes(dllPath);

    if (action == "load")
    {
        // Test 2A: Load reflectively and invoke directly (loader pattern)
        try {
            Assembly asm = Assembly.Load(assemblyBytes);
            Response.Write("Assembly loaded reflectively: " + asm.FullName + "\n");
            Type moduleType = asm.GetType("BenignModule");
            Response.Write("Found type: " + moduleType.FullName + "\n");
            Response.Write("Implements IHttpModule: " +
                typeof(System.Web.IHttpModule).IsAssignableFrom(moduleType) + "\n");
            Response.Write("\nDirect invocation successful. No pipeline registration.\n");
        } catch (Exception ex) {
            Response.Write("ERROR: " + ex.Message + "\n" + ex.StackTrace);
        }
    }
    else if (action == "register")
    {
        // Test 2B: Attempt HttpApplication.RegisterModule()
        try {
            Assembly asm = Assembly.Load(assemblyBytes);
            Type moduleType = asm.GetType("BenignModule");
            HttpApplication.RegisterModule(moduleType);
            Response.Write("RegisterModule() succeeded for: " + moduleType.FullName + "\n");
            Response.Write("Module should intercept subsequent requests.\n");
        } catch (Exception ex) {
            Response.Write("RegisterModule() FAILED: " + ex.Message + "\n" + ex.StackTrace);
        }
    }
}
</script>
```

### Step 2.2 — Test 2A: Reflective Load Only (Loader Pattern)

Clear Sysmon log:

```powershell
wevtutil cl "Microsoft-Windows-Sysmon/Operational"
```

Trigger the reflective load:

```powershell
(Invoke-WebRequest -Uri "http://localhost/trr0029lab/reflective_loader.aspx?action=load" `
    -UseBasicParsing).Content
```

**Check Sysmon 7 — this is the critical Procedure C telemetry question:**

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" |
    Where-Object { $_.Id -eq 7 } |
    Where-Object { $_.Message -match "BenignModule" } |
    Format-List TimeCreated, Message
```

**Expected result (if TRR claim is correct):**

- Sysmon 7 does NOT fire for the reflective load (byte array path bypasses
  `NtMapViewOfSection`)
- This confirms the telemetry gap documented in Procedure C

**If Sysmon 7 DOES fire:**

- The CLR may still use `NtMapViewOfSection` for byte array loads in some
  circumstances
- Procedure C's telemetry claim must be re-evaluated
- Check the ImageLoaded path — if it shows a temp file, the CLR may be
  writing a shadow copy

**Important comparison:** Run this test AFTER Test 1 completes. If Test 1
shows Sysmon 7 firing for the disk-backed load, and this test shows it NOT
firing for the byte array load, there is confirmation of the differential
telemetry behavior that distinguishes Procedures B and C.

Export evidence:

```powershell
wevtutil qe "Microsoft-Windows-Sysmon/Operational" /q:"*[System[(EventID=7)]]" `
    /f:text > "C:\TRR0029_Lab\logs\test2a_sysmon7_reflective_load.txt"
```

### Step 2.3 — Test 2B: RegisterModule() Attempt

This test determines whether `HttpApplication.RegisterModule()` can be called
at request time to wire a reflectively loaded assembly into the pipeline.

Clear Sysmon log:

```powershell
wevtutil cl "Microsoft-Windows-Sysmon/Operational"
```

Trigger the registration attempt:

```powershell
(Invoke-WebRequest -Uri "http://localhost/trr0029lab/reflective_loader.aspx?action=register" `
    -UseBasicParsing).Content
```

**Possible outcomes:**

**Outcome A — RegisterModule() succeeds:**

The loaded module is now wired into the pipeline. Verify by sending a
subsequent request and checking for the `X-TRR0029-Test` header:

```powershell
$response = Invoke-WebRequest -Uri "http://localhost/trr0029lab/default.aspx" -UseBasicParsing
$response.Headers["X-TRR0029-Test"]
```

If the header appears, the reflectively loaded assembly is intercepting
requests independently. This means:

- "Register Module" is a distinct essential operation in Procedure C's DDM
- It occurs between "Load Assembly Reflectively" and "Intercept HTTP Request"
- Observable via: potentially the CLR method invocation (ETW), but likely
  no direct telemetry — flag as a gap

**Outcome B — RegisterModule() fails with an exception:**

`RegisterModule()` is documented as requiring call during application startup
(`PreApplicationStartMethod`). If it throws at request time, then:

- Real-world Procedure C implementations must use the loader/proxy pattern
- The loaded assembly does NOT independently register into the pipeline
- "Intercept HTTP Request" in the DDM is performed by the parent/loader
  component, not the reflective assembly
- The TRR narrative needs to clarify this distinction
- The DDM may need to show the interception as belonging to the loader,
  with the reflective assembly as a sub-operation

**Outcome C — RegisterModule() succeeds but has no effect on subsequent
requests:**

Registration may succeed silently but only take effect after an app domain
restart. If the header doesn't appear on subsequent requests:

- The module was registered but not yet active
- An `iisreset` or app pool recycle would be needed to activate it
- This is a hybrid between persistent and in-memory — the registration
  exists but only in the current AppDomain's future lifecycle

### Step 2.4 — Test 2C: Persistence Check

If Test 2B succeeded (Outcome A), verify whether the registration survives
an app pool recycle:

```powershell
# Recycle the app pool
Restart-WebAppPool -Name "DefaultAppPool"

# Wait for recycle to complete
Start-Sleep -Seconds 3

# Check if the module still intercepts
$response = Invoke-WebRequest -Uri "http://localhost/trr0029lab/default.aspx" -UseBasicParsing
$response.Headers["X-TRR0029-Test"]
```

**Expected:** Header is gone after recycle. This confirms the TRR's statement
that Procedure C "is not persistent — it is lost when the `w3wp.exe` process
terminates or recycles."

---

## Phase 3: ETW EID 154 (AssemblyLoad_V1) Verification

### Objective

Confirm that ETW `Microsoft-Windows-DotNETRuntime` EID 154 fires when an
assembly is loaded reflectively via `Assembly.Load(byte[])`, and verify
whether it also fires for disk-backed CLR loads. This validates the TRR's
claim that EID 154 is the *only* telemetry source for Procedure C's load
operation.

### Background

The TRR states that EID 154 requires "an active ETW consumer session
subscribed to the runtime provider with `LoaderKeyword (0x8)`." This means
the event is not captured by default — a trace session must be started before
the load occurs. The CLR runtime provider GUID is
`e13c0d23-ccbc-4e12-931b-d9cc2eee27e4`.

### Step 3.1 — Start an ETW Trace Session

Open an **elevated** PowerShell window. Start a trace session that captures
the DotNETRuntime loader events:

```powershell
# Create the trace output directory
New-Item -Path "C:\TRR0029_Lab\etw" -ItemType Directory -Force

# Start a real-time ETW session with LoaderKeyword (0x8)
logman create trace TRR0029_DotNET `
    -p "Microsoft-Windows-DotNETRuntime" 0x8 0x5 `
    -o "C:\TRR0029_Lab\etw\dotnet_loader.etl" `
    -f bincirc -max 64 -ets
```

Verify the session is running:

```powershell
logman query TRR0029_DotNET -ets
```

Expected: Status shows `Running`.

**What the flags mean:**
- `0x8` = `LoaderKeyword` — captures assembly load/unload events
- `0x5` = Verbose level — ensures EID 154 (AssemblyLoad_V1) is captured
- `-f bincirc -max 64` = circular binary format, 64MB max (prevents disk fill)

### Step 3.2 — Test EID 154 on Disk-Backed Load (Baseline)

If Phase 1 was already run before starting this trace session, the disk-backed
load must be triggered again to capture it in the ETW trace. Recycle the app
pool to force a fresh CLR load:

```powershell
Restart-WebAppPool -Name "DefaultAppPool"
Start-Sleep -Seconds 3

# Trigger the CLR to load BenignModule.dll from /bin
Invoke-WebRequest -Uri "http://localhost/trr0029lab/default.aspx" -UseBasicParsing | Out-Null
```

### Step 3.3 — Test EID 154 on Reflective Load

Trigger the reflective load (same as Test 2A):

```powershell
(Invoke-WebRequest -Uri "http://localhost/trr0029lab/reflective_loader.aspx?action=load" `
    -UseBasicParsing).Content
```

### Step 3.4 — Stop the Trace and Extract Events

```powershell
# Stop the trace session
logman stop TRR0029_DotNET -ets
```

Parse the ETL file for AssemblyLoad events. Use `tracerpt` to convert to XML
or use PowerShell's `Get-WinEvent`:

```powershell
# Method 1: tracerpt to XML (works on all Windows versions)
tracerpt "C:\TRR0029_Lab\etw\dotnet_loader.etl" `
    -o "C:\TRR0029_Lab\logs\test3_etw_events.xml" -of XML -summary summary.txt

# Method 2: If you have PowerShell 5.1+, parse the ETL directly
Get-WinEvent -Path "C:\TRR0029_Lab\etw\dotnet_loader.etl" -Oldest |
    Where-Object { $_.Id -eq 154 } |
    Format-List TimeCreated, Message |
    Out-File "C:\TRR0029_Lab\logs\test3_eid154_events.txt"
```

If Method 2 doesn't work (ETW parsing can be version-dependent), use Method 1
and search the XML output:

```powershell
Select-String -Path "C:\TRR0029_Lab\logs\test3_etw_events.xml" `
    -Pattern "BenignModule" -Context 5
```

### Step 3.5 — Analyze Results

Look for two distinct EID 154 events:

**Disk-backed load (from Step 3.2):**
- Should show the assembly identity in the `ClrInstanceID` field
- The `FullyQualifiedAssemblyName` field may or may not contain a file path

**Reflective load (from Step 3.3):**
- Should show the assembly loaded WITHOUT a file path
- The Microsoft Security Blog notes that reflectively loaded assemblies
  show only the assembly name, not a path — the `ModuleILPath` field is
  either empty or contains just the assembly name
- This is the key forensic differentiator

**Possible outcomes:**

**Outcome A — EID 154 fires for both loads:**

This is the expected result and confirms the TRR's claim. Record:
- Whether the disk-backed load shows a full file path
- Whether the reflective load shows only the assembly name (no path)
- This path-vs-no-path distinction is the forensic indicator for in-memory
  loads documented by Microsoft

**Outcome B — EID 154 fires only for the disk-backed load:**

This would contradict the TRR's claim that EID 154 covers reflective loads.
Possible explanations:
- The `LoaderKeyword` may not cover `Assembly.Load(byte[])` — check if a
  different keyword mask is needed
- The event may have a different EID for byte-array loads

**Outcome C — EID 154 fires for neither:**

Trace session configuration issue. Verify:
- The session was running during the loads (`logman query`)
- The keyword mask includes `0x8` (LoaderKeyword)
- The ETL file is not empty

### Step 3.6 — Optional: ETW Suppression Test

If EID 154 fires successfully in Step 3.5, an optional follow-up test can
verify the TRR's claim that ETW events can be suppressed by patching
`ntdll!EtwEventWrite`.

**WARNING:** This test modifies a running process's memory. It is safe in the
sense that it only affects the `w3wp.exe` worker process (which can be recycled
to restore normal behavior), but it is more invasive than the other tests.
Skip this if not comfortable with it.

This test would require injecting a call to patch `EtwEventWrite` within the
`w3wp.exe` process before the reflective load. This is beyond the scope of a
basic lab plan — note it as a known limitation and reference the MDSec and XPN
blog posts in the TRR's references for supporting evidence.

### Step 3.7 — Export Evidence

```powershell
# Copy the ETL file for archival
Copy-Item "C:\TRR0029_Lab\etw\dotnet_loader.etl" `
    -Destination "C:\TRR0029_Lab\logs\test3_dotnet_loader.etl"
```

---

## Phase 4: EID 29 Verification

This phase verifies the scope of IIS Configuration Auditing EID 29 — whether
it fires for all module registration paths or only for API-mediated changes.

### Step 4.1 — Enable IIS Configuration Operational Log

```powershell
wevtutil sl /e:true "Microsoft-IIS-Configuration/Operational"
```

### Step 4.2 — Add a Module via appcmd (API Path)

```powershell
# Clear the IIS config log
wevtutil cl "Microsoft-IIS-Configuration/Operational"

# Add a module via the API
& "$env:SystemRoot\System32\inetsrv\appcmd.exe" add module `
    /name:"TestEID29Module" /type:"BenignModule" `
    /app.name:"Default Web Site/trr0029lab"
```

Check for EID 29:

```powershell
Get-WinEvent -LogName "Microsoft-IIS-Configuration/Operational" |
    Where-Object { $_.Id -eq 29 } |
    Format-List TimeCreated, Message
```

### Step 4.3 — Edit web.config Directly (Bypass Path)

```powershell
# Clear the IIS config log
wevtutil cl "Microsoft-IIS-Configuration/Operational"

# Edit web.config directly (not via API)
# The existing web.config from Test 1 already has the module entry.
# Add a second module by editing the file directly:
$replacement = "  <add name=""TestDirectEdit"" type=""BenignModule"" />`n        </modules>"
$config = Get-Content "C:\TRR0029_Lab\test_app\web.config" -Raw
$config = $config -replace '</modules>', $replacement
$config | Out-File "C:\TRR0029_Lab\test_app\web.config" -Encoding UTF8
```

Check for EID 29:

```powershell
Get-WinEvent -LogName "Microsoft-IIS-Configuration/Operational" -ErrorAction SilentlyContinue |
    Where-Object { $_.Id -eq 29 } |
    Format-List TimeCreated, Message
```

**Expected:** EID 29 fires for Step 4.2 (appcmd) but NOT for Step 4.3 (direct
edit). This confirms the TRR's Telemetry Constraints section.

### Step 4.4 — Export Evidence

```powershell
# Export whatever is in the IIS config log (may be empty after the direct edit test)
wevtutil qe "Microsoft-IIS-Configuration/Operational" `
    /f:text > "C:\TRR0029_Lab\logs\test4_eid29_direct_edit_silent.txt"
```

---

## Phase 5: Bonus Evidence Captures

Before cleanup, capture supplementary evidence that strengthens the overall
evidence package.

```powershell
# Sysmon config — proves EID 7 was enabled with w3wp.exe filter during testing
sysmon64 -c > "C:\TRR0029_Lab\logs\sysmon_config_during_test.txt"

# web.config as deployed — proves module registration configuration
Copy-Item "C:\TRR0029_Lab\test_app\web.config" `
    -Destination "C:\TRR0029_Lab\logs\web_config_as_deployed.xml"

# Sysmon EID 1 — w3wp.exe process lifecycle
wevtutil qe "Microsoft-Windows-Sysmon/Operational" /q:"*[System[(EventID=1)]]" `
    /f:text > "C:\TRR0029_Lab\logs\sysmon1_process_create.txt"
```

### Archive

```powershell
Compress-Archive -Path "C:\TRR0029_Lab\logs\*" `
    -DestinationPath "C:\TRR0029_Lab\TRR0029_lab_evidence.zip"
```

Copy the zip to a persistent location before proceeding to cleanup.

---

## Phase 6: Cleanup

### Step 6.1 — Remove Test Application

```powershell
Import-Module WebAdministration
Remove-WebApplication -Name "trr0029lab" -Site "Default Web Site"
```

### Step 6.2 — Stop ETW Trace (if Phase 3 was run)

```powershell
# Check if the session is still running and stop it
logman stop TRR0029_DotNET -ets 2>$null
```

(This may error if the session was already stopped — that's fine.)

### Step 6.3 — Remove Test Files

```powershell
Remove-Item -Path "C:\TRR0029_Lab" -Recurse -Force
```

### Step 6.4 — Remove appcmd Module (if Phase 4 was run)

```powershell
& "$env:SystemRoot\System32\inetsrv\appcmd.exe" delete module `
    "TestEID29Module" /app.name:"Default Web Site/trr0029lab"
```

(This may error if the application was already removed — that's fine.)

### Step 6.5 — Disable IIS Config Log (if enabled in Phase 4)

```powershell
wevtutil sl /e:false "Microsoft-IIS-Configuration/Operational"
```

### Step 6.6 — Verify Clean State

```powershell
# Confirm test app is removed
Get-WebApplication -Site "Default Web Site" | Where-Object { $_.Path -eq "/trr0029lab" }

# Confirm test directory is gone
Test-Path "C:\TRR0029_Lab"

# Confirm ETW session is gone
logman query TRR0029_DotNET -ets 2>$null
```

All should return empty/false/error.

---

## Lab Results

Lab executed: 2026-03-04, Windows 11 Pro, IIS 10.0, Sysmon v15.15.

### Test 1: Sysmon 7 on CLR Disk Load

| Question | Result |
|----------|--------|
| Did Sysmon 7 fire for BenignModule.dll loaded from `/bin`? | **NO** |
| ImageLoaded path in Sysmon 7 event | N/A — event did not fire |
| Loading process (Image field) | N/A |

Sysmon 7 fired for native DLLs loaded into `w3wp.exe` during the same request
(wldp.dll, System.EnterpriseServices.Wrapper.dll) but not for the managed
assembly. The module was confirmed loaded and executing via the
`X-TRR0029-Test` response header.

**TRR impact:** Procedure B's Sysmon 7 (ImageLoad) claim was incorrect and has
been removed. The CLR's managed assembly loader does not trigger
`PsSetLoadImageNotifyRoutine`.

### Test 2A: Sysmon 7 on Reflective Load

| Question | Result |
|----------|--------|
| Did Sysmon 7 fire for `Assembly.Load(byte[])`? | **NO** |
| If YES, what was the ImageLoaded path? | N/A |

Consistent with Test 1. Only native DLLs appeared in Sysmon 7 events (AMSI,
Defender, crypto libs). Confirms that Sysmon 7 does not cover any CLR-managed
assembly load path.

**TRR impact:** Confirms Procedure C's Sysmon 7 absence. Combined with Test 1,
Sysmon 7 is now documented as Procedure A (native DLL) only.

### Test 2B: HttpApplication.RegisterModule()

| Question | Result |
|----------|--------|
| Did RegisterModule() succeed? | **EXCEPTION** |
| If exception, what was the error message? | `Cannot register a module after the application has been initialized.` |
| Did the module intercept subsequent requests (header present)? | N/A |

The CLR enforces that `RegisterModule()` can only be called during application
startup (`PreApplicationStartMethod`), not at request time.

**TRR impact:** Procedure C's narrative revised to document the loader/proxy
pattern. The loaded assembly does not independently register into the pipeline.

### Test 2C: Persistence After Recycle

Skipped — Test 2B failed, so there was no registered module to test persistence
against. The non-persistence claim remains supported by the architectural
analysis: no configuration file is modified, so no registration survives
process termination.

### Test 3: ETW EID 154 (AssemblyLoad_V1)

| Question | Result |
|----------|--------|
| Did EID 154 fire for disk-backed CLR load? | **YES** |
| If YES, did it show a full file path? | No — `FullyQualifiedAssemblyName=0`, `ClrInstanceID=BenignModule, Version=0.0.0.0...` |
| Did EID 154 fire for reflective `Assembly.Load(byte[])`? | **YES** |
| If YES, did it show a file path or just the assembly name? | Same format — `FullyQualifiedAssemblyName=0`, assembly name only |

Two BenignModule EID 154 events captured during the trace session (timestamps
will vary by environment):

| Trigger | Description |
|---------|-------------|
| Disk-backed load | App pool recycle → `default.aspx` request → CLR loads BenignModule.dll from `/bin` |
| Reflective load | `reflective_loader.aspx?action=load` → `Assembly.Load(byte[])` |

At the EID 154 level, disk-backed and reflective loads are indistinguishable —
both show assembly name only, no file path. The Microsoft Security Blog notes
that EID 155 (AssemblyLoadFromRundown) may show the `ModuleILPath` field for
disk-backed loads, but that is a different event not tested here.

**TRR impact:** ETW EID 154 confirmed as the telemetry source for managed
assembly loads across both Procedures B and C.

### Test 4: EID 29 (IIS Configuration Auditing)

| Question | Result |
|----------|--------|
| Did EID 29 fire for `appcmd add module`? | **YES** |
| Did EID 29 fire for direct `web.config` edit? | **NO** |

The `appcmd` path produced four EID 29 events — granular per-attribute commits
for the module addition (`@name`, `@type`, and the `add` element itself). The
direct `web.config` file edit produced zero EID 29 events despite successfully
adding a module entry (confirmed via `Get-Content`).

**TRR impact:** Confirms the TRR's Telemetry Constraints section. EID 29 fires
only for API-mediated configuration changes (via `appcmd`, IIS Manager, or the
`Microsoft.Web.Administration` API). An attacker who writes or modifies
`web.config` directly — the most common real-world delivery path — bypasses
IIS configuration auditing entirely.

---

## Outcome Summary

The lab matched **row 5** of the decision matrix: Sysmon 7 absent for both
disk-backed and reflective managed loads, RegisterModule fails, ETW fires for
both.

| Finding | TRR Change |
|---------|------------|
| Sysmon 7 does not fire for CLR-managed assembly loads | Removed Sysmon 7 from Procedure B. Sysmon 7 now documented as Procedure A (native DLL) only. |
| ETW EID 154 fires for both disk-backed and reflective loads | ETW EID 154 added as the load telemetry for Procedure B. Already documented for Procedure C. |
| RegisterModule() fails at request time | Procedure C narrative revised to document loader/proxy pattern. |
| EID 29 fires only for API-mediated config changes | Telemetry Constraints section confirmed accurate. Direct `web.config` edits bypass IIS configuration auditing. |
| Telemetry Constraints section | Rewritten to accurately describe Sysmon 7 scope (native only) and ETW EID 154 scope (all managed loads). |

## Evidence Inventory

| File | Proves |
|------|--------|
| `test1_sysmon7_disk_load.txt` | Sysmon 7 absent for managed DLL; native DLLs present prove filter was active |
| `test1_sysmon11_file_creates.txt` | FileCreate telemetry for assembly write and web.config write |
| `test2a_sysmon7_reflective_load.txt` | Sysmon 7 absent for reflective load; AMSI/Defender native DLLs prove filter was active |
| `test3_dotnet_loader.etl` | Raw ETW trace (archival) |
| `test3_eid154_events.txt` | Parsed EID 154 events for both disk-backed and reflective load paths |
| `test4_eid29_direct_edit_silent.txt` | Empty file — EID 29 silent on direct web.config edit |
| `sysmon_config_during_test.txt` | Sysmon config proving EID 7 was enabled with w3wp.exe include filter |
| `web_config_as_deployed.xml` | Module registration configuration as deployed during testing |
| `sysmon1_process_create.txt` | w3wp.exe process lifecycle events |
