Get-NetIPInterface
New-NetIPAddress 
-InterfaceAlias Ethernet0 
-AddressFamily IPv4 
-IPAddress 10.180.117.8 
-PrefixLength 24 
-DefaultGateway 10.180.117.1
Set-DnsClientServerAddress
-InterfaceIndex 4
-ServerAddresses 10.180.117.7
