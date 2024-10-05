#
# Windows PowerShell script for Active Directory Domain Service Deployment
#
Install-WindowsFeature AD-Domain-Services
Install-WindowsFeature DNS
Install-WindowsFeature RSAT-AD-Tools
#
# Windows PowerShell script for Domain Controller Deployment
#
Import-Module ADDSDeployment
Install-ADDSForest 
-CreateDnsDelegation:$false 
-DatabasePath "C:\Windows\NTDS"
-DomainMode "WinThreshold" 
-DomainName "2375labs.local" 
-DomainNetbiosName "2375LABS" 
-ForestMode "WinThreshold" 
-InstallDns:$true 
-LogPath "C:\Windows\NTDS" 
-NoRebootOnCompletion:$false 
-SysvolPath "C:\Windows\SYSVOL" 
-Force:$true