$objCPU = Get-WmiObject win32_processor

switch ($objCPU.architecture)
{
0 {"This is a x86 architecture"}
1 {"This is a MPIS architecture"}
2 {"This is an Alpha architecture"}
3 {"This is a PowerPC architecture"}
9 {"This is a x64 architecture"}
Default {"This is an alien architecture"}
}