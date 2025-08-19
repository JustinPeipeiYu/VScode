# Target host
$host = "google.com"

Write-Host "Tracing route and pinging each hop to $host..." -ForegroundColor Cyan

# Run tracert
$tracertOutput = tracert $host

# Extract IP addresses from tracert output
$hops = $tracertOutput | Select-String "^\s*\d+" | ForEach-Object {
    ($_ -split '\s+')[2]  # Extract the IP address
} | Where-Object { $_ -match '\d+\.\d+\.\d+\.\d+' }

# Initialize table array
$resultTable = @()
$hopNumber = 1

foreach ($hop in $hops) {
    try {
        # Ping the hop once
        $ping = Test-Connection -ComputerName $hop -Count 1 -ErrorAction Stop
        $hostname = ([System.Net.Dns]::GetHostEntry($hop)).HostName
        $rtt = $ping.ResponseTime
    } catch {
        $hostname = "N/A"
        $rtt = "No reply"
    }

    # Add entry to table
    $resultTable += [PSCustomObject]@{
        "Hop #" = $hopNumber
        "IP Address" = $hop
        "Hostname" = $hostname
        "RTT (ms)" = $rtt
    }

    $hopNumber++
}

# Display the table
$resultTable | Format-Table -AutoSize
