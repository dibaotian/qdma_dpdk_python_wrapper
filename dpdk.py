#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import socket

#basedir = os.path.dirname(__file__)
#print ("basedir:" + basedir)

cmd_help = 'help\r'
cmd_port_init = 'port_init 0 32 16 1024 4096\r'
cmd_port_close = 'port_close 0\r'


app_path = '/home/xilinx/tencent_nfv/dpdk-stable-18.11.5/examples/qdma_testapp/build'
app_name = 'qdma_testapp'
prarm  = '-c 0x1f -n 4 -w 3b:00.0'
cmd = './qdma_testapp -c 0x1f -n 4 -w 3b:00.0'

switch = True
switch1 = True
switch2 = True

HOST = '127.0.0.1'
PORT = 9527

if __name__ == "__main__":
    #
    # dpdkp = subprocess.Popen(args=cmd,
    #                          stdin=subprocess.PIPE,
    #                          stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE,
    #                          shell=True,
    #                          bufsize=1)

    dpdkp = subprocess.Popen(args=cmd,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True,
                             bufsize=1)

    print ("#######################################")
    print ("start qdma_app with  pid %s" % dpdkp.pid)
    print ("#######################################")

    print("\n")


    try:
        while True:
            buff = dpdkp.stdout.readline()
            print(buff)
            if buff != '' and dpdkp.poll() is not None:
                break
    except Exception:
        print("read buffer error")
    finally:
        print("read buffer complete")


    # while dpdkp.poll() is None:
    #     line = dpdkp.stdout.readline()
    #     # line = line.strip()
    #     print (dpdkp.poll())
    #     print ('read line')
    #     if line:
    #         print (line)
    #         print(dpdkp.poll())
    #     else:
    #         break

    # while True:
    #     line = dpdkp.stdout.readline()
    #     if line == '' and dpdkp.poll() is not None:
    #         print('break read')
    #         break
    #     else:
    #         print(line)



    # if dpdkp.returncode == 0:
    #     print('return with success code')
    # else:
    #     print('return with failed code')

    print ("#######################################")
    print ("###########start the server#############")
    print ("#######################################")

    print("\n")



    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:

        serv.bind((HOST, PORT))

        serv.listen()

        conn, addr = serv.accept()
        with conn:
            print('Connected by', addr)
            while True:
                try:
                    cmd = conn.recv(1024)
                    print (cmd)

                    # todo parameter check

                    if not cmd:
                        print ('break')
                        break

                    print ('execute cmd')
                    dpdkp.stdin.write(b'help\r')


                   # conn.sendall(out)

                except IOError as e:
                    print('exception')
                    if dpdkp.returncode == 0:
                        print ('dpdk run success')
                    else:
                        print ('dpdk process run fail')
                    line = dpdkp.stdout.readline()
                    print (line)

                if dpdkp.poll() != 0:
                    err = dpdkp.stderr.read().decode(current_encoding)
                    print (err)



    # try:
    #     while True:
    #
    #         if switch:
    #             dpdkp.stdin.write(cmd_help)
    #             out = dpdkp.stdout.readline()
    #             switch = False
    #
    #         if switch1:
    #             dpdkp.stdin.write(cmd_port_init)
    #             out = dpdkp.stdout.readline()
    #             switch1 = False
    #
    #         if switch2:
    #             dpdkp.stdin.write(cmd_port_close)
    #             out = dpdkp.stdout.readline()
    #             switch2 = False





# ################################################################################################
 #dpdkp.stdin.write(b"help\n")
    #dpdkp.stdin.close()
    #while True:
    #    line = dpdkp.stdout.readline()
    #    line = line.strip()
    #    if line:
    #        print line
    #    else:
    #        break

    # stdout, stderr = dpdkp.communicate('help\r')

    # # To interpret as text, decode
    # if stderr is not None:
    #     err = stderr.decode('utf-8')
    #     print(err)
    # else:
    #     out = stdout.decode('utf-8')
    #     print (out)

#dpdkp.communicate(cmd_help)

#dpdkp.communicate(cmd_port_init)

#dpdkp.communicate(cmd_port_close)



#ret = dpdkp.wait()
#print (ret)


#dpdkp.poll()
#print(dpdkp.stdout.read())
#dpdkp.wait()

#print(dpdkp.returncode)

# dpdkp.stdout.close()
            # print(out)


            # line = line.strip()
            # if line:
            #     print (line)
            # else:
            #     dpdkp.stdin.write(b"help\n")
            #     dpdkp.stdin.close()
            #     # stdout, stderr = dpdkp.communicate('help\r')
            #     # print (stdout)
            #     # print (stderr)
            #     #line dpdkp.stdout.readline()
            #     #print (line)
            #     #if dpdkp.stderr is not None:
            #     #    print dpdkp.stderr.readline()
            #     # while True:
            #     #     line = dpdkp.stdout.readline()
            #     #     line = line.strip()
            #     #     if line:
            #     #         print (line)
            #     #     else:
            #     #         break

            #print (input_cmd)
            #print (type(input_cmd))
            #dpdkp.communicate(str(input_cmd))
