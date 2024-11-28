#
# Windows PowerShell script for Active Directory Domain Service Deployment
#
Install-WindowsFeature AD-Domain-Services
Add-WindowsCapability -Name rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0 -Online

#Install and remove active directory domain services, DNS
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Remove-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-WindowsFeature DNS -IncludeManagementTools
Remove-WindowsFeature DNS -IncludeManagementTools

#display server roles including RSAT management tools
Get-WindowsFeature | Where-Object installed -like install

Install-WindowsFeature RSAT-AD-Tools


#
# Windows PowerShell script for Domain Controller Deployment
#
Import-Module ADDSDeployment
Install-ADDSForest 
-CreateDnsDelegation:$false 
-DatabasePath "C:\Windows\NTDS"
-DomainMode "WinThreshold" 
-DomainName "INFO2255-jyu4340.local" 
-DomainNetbiosName "INFO2255-jyu4340" 
-ForestMode "WinThreshold" 
-InstallDns:$true 
-LogPath "C:\Windows\NTDS" 
-NoRebootOnCompletion:$false 
-SysvolPath "C:\Windows\SYSVOL" 
-Force:$true

#remove Domain Controller 
Uninstall-ADDSDomainController -ForceRemoval -DemoteOperationMasterRole

#check functional levels (domain must not be lower than forest)
Get-ADDomain | fl Name,Mode
Get-ADForest | fl Name,Mode

#verify active directory domain controller was installed
Get-ADDomain
