$FilesFromOriginal = Get-ChildItem -Path C:\Users\UserFolder\Desktop\good -Recurse -File
$FilesFromOriginal | Measure-Object

$FilesRecovered = Get-ChildItem -Path C:\Users\UserFolder\Desktop\recovered -Recurse -File
$FilesRecovered | Measure-Object

$goodDir = "C:\Users\UserFolder\Desktop\good"
$recoveredDir = "C:\Users\UserFolder\Desktop\recovered"

$goodFiles = Get-ChildItem -Path $goodDir -Recurse -File | ForEach-Object {
    [PSCustomObject]@{
        RelativePath = $_.FullName.Substring($goodDir.Length + 1)
        Hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    }
}

$recoveredFiles = Get-ChildItem -Path $recoveredDir -Recurse -File | ForEach-Object {
    [PSCustomObject]@{
        RelativePath = $_.FullName.Substring($recoveredDir.Length + 1)
        Hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    }
}

$goodHashes = $goodFiles.Hash
$uniqueRecovered = $recoveredFiles | Where-Object { $_.Hash -notin $goodHashes }
$uniqueRecovered | Select-Object RelativePath, Hash


$destFolder = "C:\Users\UserFolder\Desktop\UniqueRecovered"
if (-not (Test-Path $destFolder)) {
    New-Item -ItemType Directory -Path $destFolder | Out-Null
}

$recoveredBase = "C:\Users\UserFolder\Desktop\recovered"

foreach ($file in $uniqueRecovered) {
    $sourcePath = Join-Path $recoveredBase $file.RelativePath
    $destPath = Join-Path $destFolder $file.RelativePath

    # Ensure subdirectories exist
    $destDir = Split-Path $destPath
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    Copy-Item -Path $sourcePath -Destination $destPath
}
