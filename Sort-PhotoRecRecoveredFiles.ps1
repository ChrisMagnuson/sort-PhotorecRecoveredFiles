$SourcePath = "I:\recoveredfilesfromphotorec\unsorted"
$DestinationPath = "I:\recoveredfilesfromphotorec\sorted"

$FilesToBeSorted = Get-ChildItem -Recurse -Path $SourcePath -File
foreach ($File in $FilesToBeSorted) {
    $Extension = $File.Extension.Substring(1)
    $Destination = "$DestinationPath\$Extension"
    New-Item -ItemType Directory -Path $Destination -ErrorAction SilentlyContinue | Out-Null
    $File | Move-Item -Destination "$Destination/$($File.Directory.Name)-$($File.Name)"
}