# ============================================================
# Velora AI Backend Audit Tool
# Version : 1.0.0
# Author  : Velora AI
# Purpose : Audit Backend Structure
# ============================================================

Clear-Host

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "        VELORA AI BACKEND AUDIT v1.0"
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$Root = Split-Path $PSScriptRoot -Parent
$App = Join-Path $Root "app"

# ------------------------------------------------------------
# Required Folders
# ------------------------------------------------------------

$RequiredFolders = @(
    "api",
    "core",
    "database",
    "dependencies",
    "middleware",
    "models",
    "schemas",
    "services",
    "uploads",
    "utils"
)

Write-Host "Checking Folders..." -ForegroundColor Yellow
Write-Host ""

foreach ($folder in $RequiredFolders){

    $path = Join-Path $App $folder

    if(Test-Path $path){
        Write-Host ("[ OK ]  " + $folder) -ForegroundColor Green
    }
    else{
        Write-Host ("[MISS]  " + $folder) -ForegroundColor Red
    }

}

Write-Host ""

# ------------------------------------------------------------
# Required Root Files
# ------------------------------------------------------------

Write-Host "Checking Root Files..." -ForegroundColor Yellow
Write-Host ""

$RootFiles=@(
".env",
"requirements.txt"
)

foreach($file in $RootFiles){

    if(Test-Path (Join-Path $Root $file)){
        Write-Host ("[ OK ]  " + $file) -ForegroundColor Green
    }
    else{
        Write-Host ("[MISS]  " + $file) -ForegroundColor Red
    }

}

Write-Host ""

# ------------------------------------------------------------
# Empty Python Files
# ------------------------------------------------------------

Write-Host "Checking Empty Python Files..." -ForegroundColor Yellow
Write-Host ""

$EmptyFiles=Get-ChildItem $App -Recurse -Filter *.py | Where-Object {$_.Length -eq 0}

if($EmptyFiles.Count -eq 0){

    Write-Host "No Empty Python Files Found." -ForegroundColor Green

}
else{

    foreach($file in $EmptyFiles){

        Write-Host ("EMPTY -> " + $file.FullName.Replace($Root,"")) -ForegroundColor DarkYellow

    }

}

Write-Host ""

# ------------------------------------------------------------
# __init__.py Check
# ------------------------------------------------------------

Write-Host "Checking __init__.py Files..." -ForegroundColor Yellow
Write-Host ""

$Folders=Get-ChildItem $App -Directory

foreach($folder in $Folders){

    $init=Join-Path $folder.FullName "__init__.py"

    if(Test-Path $init){

        Write-Host ("[ OK ]  " + $folder.Name) -ForegroundColor Green

    }
    else{

        Write-Host ("[MISS]  " + $folder.Name + "\__init__.py") -ForegroundColor Red

    }

}

Write-Host ""

# ------------------------------------------------------------
# Project Summary
# ------------------------------------------------------------

$PythonFiles=(Get-ChildItem $App -Recurse -Filter *.py).Count
$FolderCount=(Get-ChildItem $App -Directory).Count

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "               PROJECT SUMMARY"
Write-Host "=============================================" -ForegroundColor Cyan

Write-Host ""
Write-Host ("Backend Folder : " + $App)
Write-Host ("Folders        : " + $FolderCount)
Write-Host ("Python Files   : " + $PythonFiles)
Write-Host ("Empty Files    : " + $EmptyFiles.Count)

Write-Host ""
Write-Host "Audit Completed Successfully." -ForegroundColor Green
Write-Host ""