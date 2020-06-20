#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@Author  :   Minxie

@License :   (C) Copyright 2013-2020

@Contact :   Minx@xilinx.com

@Software:   Xilinx QDMA DPDK plugin

@File    :   qdma_dpdk_plugin.py

@Time    :   2020-06-15

@Desc    :
'''

import sys
import qdma_dpdk_python_wrapper
import socket
import subprocess

CPU_MASK = '0x1f'
MEM_CHAN = 4

QUEUE_BASE = 0

BAR0 = 0
BAR1 = 1
CMPT_DESC_LEN = 32
PREFETCH_ENABLE = 1
PREFETCH_DISABLE = 0
MAX_QUEUES = 64

PORT0 = 0
ALL_Q_NUM_8 = 8
ST_Q_NUM_8 = 8
RING_DEEP_1K = 1024
PKT_BUFF_SIZE_4K = 4096
ITERATION1 = 1


# param_org = " -c 0x1f -n 4 -w 3b:00.0 queue_base=0 config_bar=0 cmpt_desc_len=32 desc_prefetch=0 --config=\"(64)\""

param_org = " -c %s -n %s -w %s queue_base=%s config_bar=%s cmpt_desc_len=%s desc_prefetch=%s"

HOST = '127.0.0.1'
PORT = 9527

if __name__ == "__main__":

    # qdma_app folder path
    exe_path = './'

    # app name
    exe_name = 'qdma_testapp'

    # parameter
    drv_list = ['vfio-pci', 'igb_uio']
    bdf = subprocess.Popen(args='lspci -vd 10ee:', stdout=subprocess.PIPE, shell=True)
    out, err = bdf.communicate()
    if 'Xilinx Corporation Device' in out:
        if any(drv in out for drv in drv_list):
            PF0_bdf = out[0:8]
            param = param_org % (CPU_MASK, MEM_CHAN, PF0_bdf, QUEUE_BASE, BAR0, CMPT_DESC_LEN, PREFETCH_DISABLE)
        else:
            print "QDMA device does not bind the DPDK, please use dodk_bind.py to bind the vfio or igb-uio"
            exit(-1)
    else:
        print "Can not find xilinx QDMA device, Please Check your system"
        exit(-1)

    # combine
    cmd = exe_path + exe_name + param

    # todo parameters check
    if len(sys.argv) > 3:
        print len(sys.argv)
        print 'Usage: Plugin function need max two parameters, 1 input command string,  2 debug(True/False)'
        exit(1)
    else:
        if len(sys.argv) == 2:
            cmd = sys.argv[1]
            debug = False
        elif len(sys.argv) == 3:
            cmd = sys.argv[1]
            debug = sys.argv[2]
        else:
            debug = False

    # start the qdma app process
    dpdkp = qdma_dpdk_python_wrapper.Qdmaplugin(cmd, debug)

    # check if the process is running
    if dpdkp.is_qdma_app_run():
        print " "
        print "QDMA APP is running"
        print " "

    else:
        print " "
        print "QDMA APP is not running  Quit with error"
        print " "
        dpdkp.flush_output()
        exit(-1)

    dpdkp.set_echo(False)

    print dpdkp.get_methods()

    # create
    ret = dpdkp.port_init(PORT0, ALL_Q_NUM_8, ST_Q_NUM_8, RING_DEEP_1K, PKT_BUFF_SIZE_4K)
    print ret

    # send data
    ret = dpdkp.dma_to_device(PORT0, 1, 'data/datafile0_4K.bin', 0, 4096, ITERATION1)
    print ret

    # receive data
    ret = dpdkp.dma_from_device(PORT0, 1, 'data/port0_qcount0_size4k.bin', 0, 4096, ITERATION1)
    print ret

    # read register
    ret = dpdkp.reg_read(PORT0, 0, 0)
    print ret

    # write register
    ret = dpdkp.reg_write(PORT0, 0, 0, 0x5a5a)
    print ret

    # It will cause system crash
    # ret = dpdkp.reg_dump(PORT0)
    # print ret

    # # dump the queue status
    ret = dpdkp.queue_dump(PORT0, 0)
    print ret

    # dump the port descriptor
    ret = dpdkp.desc_dump(PORT0, 0)
    print ret

    # reset the port
    ret = dpdkp.port_reset(PORT0, ALL_Q_NUM_8, ST_Q_NUM_8, RING_DEEP_1K, PKT_BUFF_SIZE_4K)
    print ret

    # close the port
    ret = dpdkp.port_close(PORT0)
    print ret

    # remove the port
    ret = dpdkp.port_remove(PORT0)
    print ret

    # todo get the api call form North management plane
    # start a Daemon for service

    exit(0)

    # # get the app cmd
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
    #     serv.bind((HOST, PORT))
    #     serv.listen()
    #     conn, addr = serv.accept()
    #
    #     with conn:
    #         print('Connected by', addr)
    #         while True:
    #             try:
    #                 cmd = conn.recv(1024)
    #                 print (cmd)
    #                 # todo parameter check
    #                 if not cmd:
    #                     print ('break')
    #                     break
    #                 print ('execute cmd')
    #                 switch.get(choice, default)()
    #
    #             except IOError as e:
    #                 print('exception')
    #                 if dpdkp.returncode == 0:
    #                     print ('dpdk run success')
    #                 else:
    #                     print ('dpdk process run fail')
    #                 line = dpdkp.stdout.readline()
    #                 print (line)

