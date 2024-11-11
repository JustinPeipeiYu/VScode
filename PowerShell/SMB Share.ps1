New-SmbShare -Name "Data" -Path "J:\Data" -EncryptData $True
Remove-SmbShare -Name "Data"
