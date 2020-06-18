# qdma_dpdk_python_wrapper


1 The Plugin is based on the xilinx QDMA (2019.1)
  https://github.com/Xilinx/dma_ip_drivers
2 The Plugin is based on the python2.7
3 The Plugin is based on the DPDK dpdk-stable-18.11.5
4 Support Alveo card U50

5 Related document
  https://xilinx.github.io/dma_ip_drivers/2019.1/DPDK/html/index.html
  https://www.xilinx.com/support/documentation/ip_documentation/qdma/v3_0/pg302-qdma.pdf
  https://www.xilinx.com/support/answers/71453.html

### Prerequisites
 CentOS 7.4 1708 3.10.0-862.el7.x86_64
 GCC 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
 Xilinx QDMA IP (Vivado 2018.3)
 Xilinx QDMA DPDK driver (2019.1)
 DPDK  dpdk-stable-18.11.5
 Alveo card U50
 Python 2.7
 



###Known issues
reg dump will cause host crash