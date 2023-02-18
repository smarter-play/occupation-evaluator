
$scriptBlock = { curl 'http://localhost:5000/api/occupation?basket=589505315&t=2016-08-10T18:00:00' }

1..10 | ForEach-Object {
    Start-Job -ScriptBlock $scriptBlock
}

Get-Job | Wait-Job | Receive-Job
