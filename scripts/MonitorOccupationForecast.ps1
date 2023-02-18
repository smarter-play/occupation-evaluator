
.\.venv\Scripts\activate

$fromDate = (Get-Date).AddMinutes(-30)
$toDate = Get-Date

#py .\src\sample_data_generator.py

py .\src\occupation_forecast_visualizer.py `
    -b 589505315 `
    --present "2016-08-15 17:30:00" `
    -np 90 `
    -nf 14 `
    -t '2016-08-17 14:30:00'
