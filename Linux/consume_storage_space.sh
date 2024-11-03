#show available disk usage
fdisk -l | grep -i sd

#check if LVM is installed
lvscan

#install yum (when above command fails)
yum install lvm2

#create physical volume
pvcreate /dev/sdb


