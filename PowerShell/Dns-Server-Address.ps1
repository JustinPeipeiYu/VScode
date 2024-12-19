# get the interface index 
Get-NetIPInterface

# set the dns server address
Set-DnsClientServerAddress -InterfaceIndex 100 -ServerAddresses 10.0.0.1