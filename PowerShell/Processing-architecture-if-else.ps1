$objCPU = Get-WmiObject win32_processor

If ($objCPU.architecture -eq 0)
{"This is a x86 architecture"}
Elseif ($objCPU.architecture -eq 1)
{"This is a MIPS architecture"}
Elseif ($objCPU.architecture -eq 2)
{"This is an Alpha architecture"}
Elseif ($objCPU.architecture -eq 3)
{"This is a PowerPC architecture"}
Elseif ($objCPU.architecture -eq 9)
{"This is a x64 arhitecture"}
Else
{"This is an alien architecture"}