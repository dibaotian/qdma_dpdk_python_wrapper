# qdma_dpdk_python_wrapper

## 1 Prerequisites

CentOS 7.4 1708 3.10.0-862.el7.x86_64

GCC 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)

Xilinx QDMA IP (Vivado 2018.3)

Xilinx QDMA DPDK driver (2019.1)

DPDK dpdk-stable-18.11.5

Alveo card U50

Python 2.7
 

##2 Getting Started
1 Set up the Hardware, Program the QDMA MCS to card (you may need JTAG, please power cycle server after program)

using the #> lspci -vd 10ee: check  you will find the qdma device as following if the QDMA is programed succeed

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
	


2 build the software, please refrence folloing link
https://xilinx.github.io/dma_ip_drivers/2019.2/DPDK/html/build.html





##3 Known issues

reg dump will cause host crash

##4  Related document
https://xilinx.github.io/dma_ip_drivers/2019.1/DPDK/html/index.html
https://www.xilinx.com/support/documentation/ip_documentation/qdma/v3_0/pg302-qdma.pdf
https://www.xilinx.com/support/answers/71453.html
