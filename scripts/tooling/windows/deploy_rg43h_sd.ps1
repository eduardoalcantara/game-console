# deploy_rg43h_sd.ps1
# game-console — formata SD RG43H (FAT32 EEROMS) e copia staging EmuELEC
# Uso: .\deploy_rg43h_sd.ps1 -DriveLetter H -StagingPath "...\resources\rg43h\staging" -Yes
# Volumes >32GB: requer fat32format (winget install Ridgecrop.fat32format)

param(
    [Parameter(Mandatory = $false)]
    [string] $DriveLetter = "H",

    [Parameter(Mandatory = $false)]
    [string] $StagingPath = "",

    [Parameter(Mandatory = $false)]
    [switch] $SkipFormat,

    [Parameter(Mandatory = $false)]
    [switch] $Yes
)

$ErrorActionPreference = "Stop"

function Clear-ScreenGameConsole {
    Clear-Host
}

function Write-Header {
    Write-Host "game-console"
    Write-Host "Script: deploy_rg43h_sd"
    Write-Host "Funcao: Formatar FAT32 EEROMS e copiar staging RG43H"
    Write-Host "----------------------------------------"
}

function Find-RepoRoot {
    $startPaths = @(
        $PSScriptRoot,
        (Get-Location).Path
    )
    foreach ($start in $startPaths) {
        if (-not $start) { continue }
        $p = $start
        while ($p) {
            if ((Split-Path -Leaf $p) -eq "game-console") {
                return $p
            }
            $parent = Split-Path -Parent $p
            if (-not $parent -or $parent -eq $p) { break }
            $p = $parent
        }
    }
    return $null
}

function Prompt-YesNo {
    param([string]$Question, [int]$Default = 0)
    while ($true) {
        Write-Host $Question
        Write-Host "  0 = nao"
        Write-Host "  1 = sim"
        Write-Host "  Enter = default ($(if ($Default -eq 1) { 'sim' } else { 'nao' }))"
        $raw = Read-Host ">"
        if ($raw -eq "") { return $Default }
        if ($raw -eq "0") { return 0 }
        if ($raw -eq "1") { return 1 }
        Write-Host "Entrada invalida."
    }
}

function Format-Rg43hVolume {
    param(
        [string]$Letter,
        [int]$ClusterSectors = 128
    )
    $drive = "${Letter}:"
    Write-Host "A formatar ${drive} (FAT32, EEROMS)..."
    $usedFallback = $false
    try {
        Format-Volume -DriveLetter $Letter -FileSystem FAT32 -NewFileSystemLabel "EEROMS" -Confirm:$false -Force | Out-Null
    } catch {
        Write-Host "Format-Volume falhou ($($_.Exception.Message)); a usar fat32format (volumes >32GB)."
        $fat32 = Get-Command fat32format -ErrorAction SilentlyContinue
        if (-not $fat32) {
            Write-Host "ERRO: fat32format nao encontrado. Instale: winget install Ridgecrop.fat32format"
            throw
        }
        cmd /c "echo y| `"$($fat32.Source)`" -c$ClusterSectors $drive"
        if ($LASTEXITCODE -ne 0) {
            throw "fat32format exit code $LASTEXITCODE"
        }
        $usedFallback = $true
        Start-Sleep -Seconds 2
        cmd /c "label $drive EEROMS" | Out-Null
    }
    Start-Sleep -Seconds 3
    $vol = Get-Volume -DriveLetter $Letter -ErrorAction SilentlyContinue
    if ($vol) {
        Write-Host "Formatado: $($vol.FileSystem) / $($vol.FileSystemLabel)"
        if ($vol.FileSystem -ne "FAT32") {
            throw "Volume nao ficou FAT32 (atual: $($vol.FileSystem))"
        }
    }
    if ($usedFallback) {
        Write-Host "Nota: formatado com fat32format -c$ClusterSectors (64 KB clusters)."
    }
}

Clear-ScreenGameConsole
Write-Header

$RepoRoot = Find-RepoRoot
if (-not $RepoRoot) {
    Write-Host "ERRO: pasta game-console nao encontrada."
    exit 1
}
Write-Host "REPO_ROOT=$RepoRoot"

if (-not $StagingPath) {
    $StagingPath = Join-Path $RepoRoot "resources\rg43h\staging"
}
$TargetRoot = "${DriveLetter}:\"
$Volume = Get-Volume -DriveLetter $DriveLetter -ErrorAction SilentlyContinue

Write-Host "Staging: $StagingPath"
Write-Host "Destino: $TargetRoot"
Write-Host ""

if (-not (Test-Path $StagingPath)) {
    Write-Host "ERRO: staging nao encontrado. Execute curate_rg43h_roms.py --execute --yes primeiro."
    exit 1
}

$fat32Issues = Get-ChildItem $StagingPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 4294967295 }
if ($fat32Issues) {
    Write-Host "ERRO: ficheiros > 4GB incompativeis com FAT32:"
    $fat32Issues | ForEach-Object { Write-Host "  $($_.FullName)" }
    exit 1
}

$stagingFiles = (Get-ChildItem $StagingPath -Recurse -File -ErrorAction SilentlyContinue).Count
$stagingSize = (Get-ChildItem $StagingPath -Recurse -File -ErrorAction SilentlyContinue |
    Measure-Object Length -Sum).Sum
Write-Host "Staging: $stagingFiles ficheiros, $([math]::Round($stagingSize/1GB, 2)) GB"

if ($Volume) {
    Write-Host "Volume atual: $($Volume.FileSystem) | $($Volume.FileSystemLabel) | $([math]::Round($Volume.Size/1GB, 1)) GB"
} else {
    Write-Host "AVISO: volume ${DriveLetter}: nao encontrado."
    exit 1
}

if ($Volume.Size -lt 100GB) {
    Write-Host "AVISO: volume parece < 100GB. Confirmar que e o cartao 128GB correto."
}

if (-not $SkipFormat) {
    if (-not $Yes) {
        if ((Prompt-YesNo "APAGAR e formatar ${DriveLetter}: como FAT32 EEROMS?" 0) -ne 1) {
            Write-Host "Cancelado."
            exit 0
        }
    }
    Format-Rg43hVolume -Letter $DriveLetter
}

Write-Host "A copiar staging -> ${DriveLetter}:\ ..."
robocopy $StagingPath $TargetRoot /E /R:2 /W:5 /NFL /NDL /NJH /NJS /nc /ns /np
$rc = $LASTEXITCODE
if ($rc -ge 8) {
    Write-Host "ERRO robocopy exit code: $rc"
    exit $rc
}

$firstDl = Join-Path $TargetRoot ".firstDownload"
if (-not (Test-Path $firstDl)) {
    New-Item -ItemType File -Path $firstDl -Force | Out-Null
}

Write-Host ""
Write-Host "Validacao:"
@("bios", "snes", "megadrive", "neogeo") | ForEach-Object {
    $p = Join-Path $TargetRoot $_
    if (Test-Path $p) {
        $c = (Get-ChildItem $p -Recurse -File -ErrorAction SilentlyContinue).Count
        Write-Host "  $_/: $c ficheiros"
    } else {
        Write-Host "  $_/: AUSENTE"
    }
}

$snesRom = Get-ChildItem (Join-Path $TargetRoot "snes") -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "Metal Warriors|Rock n" }
if ($snesRom) {
    Write-Host "  Favoritos SNES OK: $($snesRom.Name -join ', ')"
}

$destFiles = (Get-ChildItem $TargetRoot -Recurse -File -ErrorAction SilentlyContinue).Count
Write-Host "  Total SD: $destFiles ficheiros"

Write-Host ""
Write-Host "Acao concluida: deploy_rg43h_sd"
Write-Host "Diretorio raiz detectado: $RepoRoot"
exit 0
