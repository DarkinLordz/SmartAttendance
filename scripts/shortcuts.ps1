[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$Destination = [Environment]::GetFolderPath("Desktop"),
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-FullPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path -Path (Get-Location) -ChildPath $Path))
}

$resolvedProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$resolvedDestination = Get-FullPath -Path $Destination

if (-not (Test-Path -LiteralPath $resolvedDestination)) {
    New-Item -ItemType Directory -Path $resolvedDestination -Force | Out-Null
}

$shortcutItems = @(
    @{
        Name = "Faces"
        TargetPath = Join-Path $resolvedProjectRoot "data\faces"
        WorkingDirectory = Join-Path $resolvedProjectRoot "data"
        Description = "Open the SmartAttendance faces folder"
    }
    @{
        Name = "GUI"
        TargetPath = Join-Path $resolvedProjectRoot "src\gui.pyw"
        WorkingDirectory = Join-Path $resolvedProjectRoot "src"
        Description = "Open the SmartAttendance GUI script"
    }
    @{
        Name = "Recognize"
        TargetPath = Join-Path $resolvedProjectRoot "src\recognize.py"
        WorkingDirectory = Join-Path $resolvedProjectRoot "src"
        Description = "Open the SmartAttendance recognize script"
    }
    @{
        Name = "Attendance"
        TargetPath = Join-Path $resolvedProjectRoot "data\attendance.csv"
        WorkingDirectory = Join-Path $resolvedProjectRoot "data"
        Description = "Open the SmartAttendance attendance CSV"
    }
    @{
        Name = "Students"
        TargetPath = Join-Path $resolvedProjectRoot "data\students.csv"
        WorkingDirectory = Join-Path $resolvedProjectRoot "data"
        Description = "Open the SmartAttendance students CSV"
    }
)

$missingTargets = $shortcutItems | Where-Object { -not (Test-Path -LiteralPath $_.TargetPath) }
if ($missingTargets) {
    $missingList = $missingTargets.TargetPath -join [Environment]::NewLine
    throw "Cannot create shortcuts because the following targets were not found:`n$missingList"
}

$shell = New-Object -ComObject WScript.Shell
$createdShortcuts = @()

foreach ($item in $shortcutItems) {
    $shortcutPath = Join-Path $resolvedDestination ("{0}.lnk" -f $item.Name)

    if ($PSCmdlet.ShouldProcess($shortcutPath, "Create shortcut")) {
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = $item.TargetPath
        $shortcut.WorkingDirectory = $item.WorkingDirectory
        $shortcut.Description = $item.Description
        $shortcut.Save()
        $createdShortcuts += $shortcutPath
    }
}

if ($createdShortcuts.Count -gt 0) {
    Write-Host "Created shortcuts:"
    foreach ($shortcutPath in $createdShortcuts) {
        Write-Host " - $shortcutPath"
    }
} else {
    Write-Host "No shortcuts were created."
}
