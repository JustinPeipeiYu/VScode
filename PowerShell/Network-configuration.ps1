#get interface specifications
Get-NetIPInterface

#add and remove IP address
New-NetIPAddress 
-InterfaceAlias Ethernet0 
-AddressFamily IPv4 
-IPAddress 10.180.117.8 
-PrefixLength 24 
-DefaultGateway 10.180.117.1
Remove-NetIPAddress
-InterfaceIndex 4

Rename-NetAdapter
-Name Ethernet1
-NewName Storage

#add and remove DNS server address
Set-DnsClientServerAddress
-InterfaceIndex 4
-ServerAddresses 10.180.117.7
Set-DnsClientServerAddress
-InterfaceIndex 4
-ResetServerAddresses

#add and remove default gateway
Remove-NetRoute -InterfaceIndex 4 -DestinationPrefix "0.0.0.0/0" -NextHop 10.180.117.1
New-NetRoute -InterfaceIndex 4 -DestinationPrefix "0.0.0.0/0" -NextHop 10.180.117.1
