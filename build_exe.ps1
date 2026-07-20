param(
    [switch]$Clean,
    [switch]$NoWindow = $true,
    [string]$OutputDir = "$PSScriptRoot\dist",
    [string]$Name = "PoE2 Mirror Crafter"
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

Write-Host "=== PoE2 Mirror Crafter Build Script ===" -ForegroundColor Cyan

# 1. Check/install PyInstaller
Write-Host "`n[1/4] Checking PyInstaller..." -ForegroundColor Yellow
$pi = python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null
if (-not $pi) {
    Write-Host "  Installing PyInstaller..." -ForegroundColor Gray
    python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) { throw "Failed to install PyInstaller" }
    Write-Host "  PyInstaller installed." -ForegroundColor Green
} else {
    Write-Host "  PyInstaller $pi found." -ForegroundColor Green
}

# 2. Install pygame if needed
Write-Host "`n[2/4] Checking dependencies..." -ForegroundColor Yellow
$pygame_check = python -c "import pygame; print(pygame.version.ver)" 2>$null
if (-not $pygame_check) {
    Write-Host "  Installing pygame..." -ForegroundColor Gray
    python -m pip install pygame>=2.0
    if ($LASTEXITCODE -ne 0) { throw "Failed to install pygame" }
    Write-Host "  pygame installed." -ForegroundColor Green
} else {
    Write-Host "  pygame $pygame_check found." -ForegroundColor Green
}

# 3. Clean previous builds
Write-Host "`n[3/4] Cleaning previous builds..." -ForegroundColor Yellow
$cleanDirs = @("build", "dist", "__pycache__")
foreach ($dir in $cleanDirs) {
    if (Test-Path -LiteralPath $dir) {
        Remove-Item -Recurse -Force -LiteralPath $dir
        Write-Host "  Removed $dir/" -ForegroundColor Gray
    }
}
Get-ChildItem -Filter "*.spec" -File | Remove-Item -Force
Write-Host "  Clean." -ForegroundColor Green

# 4. Build
Write-Host "`n[4/4] Building executable..." -ForegroundColor Yellow

$addData = "assets\fonts\gothic.ttf;assets\fonts"

$pyiArgs = @(
    "--name", $Name,
    "--onefile",
    "--add-data", $addData,
    "--distpath", $OutputDir,
    "--workpath", "build",
    "--specpath", "."
)
if ($NoWindow) { $pyiArgs += "--windowed" }
$pyiArgs += "main.py"

Write-Host "  Running: python -m PyInstaller $($pyiArgs -join ' ')" -ForegroundColor Gray
python -m PyInstaller @pyiArgs

if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }

# 5. Copy exe to project root
$exeName = "$Name.exe"
$builtExe = Join-Path $OutputDir $exeName
if (Test-Path -LiteralPath $builtExe) {
    Copy-Item -LiteralPath $builtExe -Destination $PSScriptRoot -Force
    $size = [math]::Round((Get-Item -LiteralPath $builtExe).Length / 1MB, 1)
    Write-Host "`nBuild successful!" -ForegroundColor Green
    Write-Host "  Output: $builtExe ($size MB)" -ForegroundColor White
    Write-Host "  Also copied to: $PSScriptRoot\$exeName" -ForegroundColor White
} else {
    throw "Expected .exe not found at $builtExe"
}

# 6. Clean up .spec file
Get-ChildItem -Filter "*.spec" -File | Remove-Item -Force -ErrorAction SilentlyContinue
