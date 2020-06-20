# qdma_dpdk_python_wrapper

## 1 Prerequisites

CentOS 7.4 1708 3.10.0-862.el7.x86_64

GCC 4.8.5 20150623 (Red Hat 4.8.5-36)

Xilinx QDMA IP (Vivado 2018.3)

Xilinx QDMA DPDK driver (2019.1)

DPDK dpdk-stable-18.11.5

Alveo card U50

Python 2.7

## 2 Introduction 

qdma_dpdk_python_wrapper.py   Qdmaplugin Base Class

qdma_dpdk_plugin.py           Plugin framework

pf_inis.sh                    Prepare dpdk env 

data/                         test data file

## 3 Getting Started

##### 1) Set up the Hardware

Program the QDMA  shell bit/MCS to card (You may need JTAG, please power cycle server after program)

Using the $> lspci -vd 10ee: cmd check,  you will find the following device if the QDMA shell is programed succeed

    xx:xx.0 Memory controller: Xilinx Corporation Device 913f

	Subsystem: Xilinx Corporation Device 0007
	
	Flags: bus master, fast devsel, latency 0, NUMA node 0
	
	Memory at 382ffe040000 (64-bit, prefetchable) [size=128K]
	
	Memory at 382ffa000000 (64-bit, prefetchable) [size=32M]
	
	Capabilities: [40] Power Management version 3
	
	Capabilities: [60] MSI-X: Enable- Count=8 Masked-
	
	Capabilities: [70] Express Endpoint, MSI 00
	
	Capabilities: [100] Advanced Error Reporting
	
	Capabilities: [140] Single Root I/O Virtualization (SR-IOV)
	
	Capabilities: [180] Alternative Routing-ID Interpretation (ARI)

##### 2) Build the software, please refer to the link below
https://xilinx.github.io/dma_ip_drivers/2019.2/DPDK/html/build.html

##### 3) Setup the DPDK environment

Put the pf_init.sh in the <dpdk_root> and run, the script support load the load vfio-pci/igbuio in the PF0

##### 4) Run the application

 $>python qdma_dpdk_plugin.py <cmd, parameter>
 
 cmd example ./qdma_testapp -c 0x1f -n 4 -w 3b:00.0 queue_base=0 config_bar=0 cmpt_desc_len=32 desc_prefetch=0


## 3 Known issues

reg_dump cause host crash

dma_from_device fail

## 4  Related document

https://xilinx.github.io/dma_ip_drivers/2019.1/DPDK/html/index.html
https://www.xilinx.com/support/documentation/ip_documentation/qdma/v3_0/pg302-qdma.pdf
https://www.xilinx.com/support/answers/71453.html
