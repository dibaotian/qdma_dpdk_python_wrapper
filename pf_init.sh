#!/bin/sh

DRV=VFIO
#DRV = UIO

if [ "$(whoami)" != "root" ]; then
    echo "WARN : root priviledge required"
    exit -1
fi


# create the hugepage mount point
if [ ! -d "/mnt/huge" ]; then
   mkdir /mnt/huge
fi

mount -t hugetlbfs nodev /mnt/huge


if [ $DRV == "UIO" ]; then

    modprobe uio

    echo "load igb_uio"
    if [ "$(lsmod | grep igb_uio | awk 'NR==1 {print $1}')" != "igb_uio" ]; then
        insmod x86_64-native-linuxapp-gcc/kmod/igb_uio.ko
    fi

    echo "bind PF0 with igb_uio"
    PF0_bdf=$(lspci -d 10ee: | awk 'NR==1 {print $1}')
    usertools/dpdk-devbind.py -b igb_uio $PF0_bdf
    echo "bind PF0 driver complete"
    echo " "

else
   echo "load vfio pci"
   modprobe vfio-pci
   

   echo "bind PF0 with vfio"
   PF0_bdf=$(lspci -d 10ee: | awk 'NR==1 {print $1}')
   usertools/dpdk-devbind.py -b vfio-pci $PF0_bdf
   echo "bind PF0 driver complete"
   echo " "

fi



