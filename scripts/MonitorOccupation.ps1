
.\.venv\Scripts\activate

$fromDate = (Get-Date).AddMinutes(-30)
$toDate = Get-Date

py .\src\occupation_visualizer.py `
    -b 2045615519 `
    -f $(Get-Date $fromDate.ToUniversalTime() -UFormat '+%Y-%m-%dT%H:%M:%S.000') `
    -t $(Get-Date $toDate.ToUniversalTime() -UFormat '+%Y-%m-%dT%H:%M:%S.000')
