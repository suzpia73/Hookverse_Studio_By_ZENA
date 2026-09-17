Get-ChildItem -Path "C:\Users\june2\.gemini\antigravity-ide\brain" -Filter "*cut03_perfect_phone*" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "FOUND: $($_.FullName)"
}
