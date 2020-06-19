#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import qdma_dpdk_python_wrapper
import socket

# qdma_app folder path
exe_path = './'
# app name
exe_name = 'qdma_testapp'
# parameter
param = ' -c 0x1f -n 4 -w 3b:00.0'
# combine
cmd = exe_path + exe_name + param

HOST = '127.0.0.1'
PORT = 9527

if __name__ == "__main__":

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
    ret = dpdkp.port_init(0, 1, 1, 1024, 2048)
    print ret

    # send data
    ret = dpdkp.dma_from_device(0, 1, 'data/port0_qcount0_size4k.bin', 0, 4096, 1)
    print ret

    # read register
    ret = dpdkp.reg_read(0, 0, 0)
    print ret

    # write register
    ret = dpdkp.reg_write(0, 0, 0, 0x1)
    print ret

    #  It will cause system crash
    # ret = dpdkp.reg_dump(0)
    # print ret

    # dump the queue status
    ret = dpdkp.queue_dump(0, 0)
    print ret

    # dump the port descriptor
    ret = dpdkp.desc_dump(0, 0)
    print ret

    # reset the port
    ret = dpdkp.port_reset(0, 1, 1, 1024, 2048)
    print ret

    # close the port
    ret = dpdkp.port_close(0)
    print ret

    # remove the port
    ret = dpdkp.port_remove(0)
    print ret

    # todo get the api call form North management plane

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

