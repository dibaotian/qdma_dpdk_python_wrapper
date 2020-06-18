#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import pexpect

#basedir = os.path.dirname(__file__)
#print ("basedir:" + basedir)

cmd_help = 'help\r'
cmd_port_init = 'port_init 0 32 16 1024 4096\r'
cmd_port_close = 'port_close 0\n'


app_path = '/home/xilinx/tencent_nfv/dpdk-stable-18.11.5/examples/qdma_testapp/build'
app_name = 'qdma_testapp'
prarm  = '-c 0x1f -n 4 -w 09:00.0'
cmd = './qdma_testapp -c 0x1f -n 4 -w 3b:00.0'


def send_cmd(self):
    while True:
        self.process.expect("xilinx-app>")
        self.process.logfile_read = sys.stdout
        # print(dpdkp.after)
        # dpdkp.sendline('help\r')
        # dpdkp.expect("xilinx-app>")
        # print(dpdkp.after)
        # self.process.logfile_read = sys.stdout

        str = raw_input("")

        if str:
            if str == " ":
                self.process.sendline('\r\n')
            elif str in ['exit', 'Exit', 'quit', 'Quit']:
                self.kill_process()
            else:
                self.process.sendline(str)
        else:
            self.process.sendline('\r\n')


class Qdmaplugin():
    def __init__(self, cmd):
        """
        Start the qdma app
        :param cmd:
        cmd represents qdma comand string
        """
        self.cmd = cmd

        print ("##################################################################")
        print ("###########start the Xilinx QDMA DPDK plugin service##############")
        print ("##################################################################")

        # todo parameter check

        # self.process = pexpect.spawn(self.cmd, timeout=None, logfile=sys.stdout)
        self.process = pexpect.spawn(self.cmd, timeout=None)

    def flush_output(self):
        """
        Clear the contents of readbufer
        :return:
        """
        self.process.expect("xilinx-app>")

    def port_init(self, port_id, num_queues, st_queues, ring_depth, pkt_buffer_size):
        """
        Assigns queues to the port, sets up required resources for the queues and prepares queues for data processing
        :param port_id:
        :param num_queues:
        :param st_queues:
        :param ring_depth:
        :param pkt_buffer_size:
        :return: string of init result

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0.
        num-queues represents the total number of queues to be assigned to the port
        num-st-queues represents the total number of queues to be configured in streaming mode.
                      This implies that the (num-queues - num-st-queues) number of queues has to be configured
                      in memory mapped mode.
        ring-depth represents the number of entries in C2H and H2C descriptor rings of each queue of the port
        pkt-buff-size represents the size of the data that a single C2H or H2C descriptor can support
        example  port_init 0 1 1 1024 2048
        """

        port_cmd = 'port_init %s %s %s %s %s' % (port_id, num_queues, st_queues, ring_depth, pkt_buffer_size)

        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")

        result = self.process.before
        return result
        # print self.process.after

    def port_close(self, port_id):
        """
        Free up all the allocated resources and removes the queues associated with the port.
        :param port_id:
        :return:string of close result

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        """

        port_cmd = 'port_close %s' % port_id
        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def port_reset(self, port_id, num_queues, st_queues, ring_depth, pkt_buff_size):
        """
        Reset specified port
        :param port_id:
        :param num_queues:
        :param st_queues:
        :param ring_depth:
        :param pkt_buff_size:
        :return: string of reset result

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        num-queues represents the total number of queues to be assigned to the port
        num-st-queues represents the total number of queues to be configured in streaming mode.
                      This implies that the (num-queues - num-st-queues) number of queues has to be configured
                      in memory mapped mode.
        ring-depth represents the number of entries in C2H and H2C descriptor rings of each queue of the port
        pkt-buff-size represents the size of the data that a single C2H or H2C descriptor can support
        """

        port_cmd = 'port_reset %s %s %s %s %s' % (port_id, num_queues, st_queues, ring_depth, pkt_buff_size)
        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def port_remove(self, port_id):
        """
        Free up all the resources allocated for the port and removes the port from application use
        :param port_id:
        :return:

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        """

        port_cmd = 'port_remove %s' % port_id
        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def reg_read(self, port_id, bar_num, address):
        """
        Read specified register
        :param port_id:
        :param bar_num:
        :param address:
        :return: register value

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0

        bar-num represents the PCIe BAR where the register is located

        address represents offset of the register in the PCIe BAR bar-num
        """

        reg_cmd = 'reg_read %s %s %s' % (port_id, bar_num, address)
        self.process.sendline(reg_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def reg_write(self, port_id, bar_num, address, value):
        """
        Write a 32-bit value to the specified register
        :param port_id:
        :param bar_num:
        :param address:
        :param value:
        :return: reg value/succeed/fail

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0.
        bar-num represents the PCIe BAR where the register is located
        address represents offset of the register in the PCIe BAR bar-num
        value represents the value to be written at the register offset address
        """

        reg_cmd = 'reg_write %s %s %s %s' % (port_id, bar_num, address, value)
        self.process.sendline(reg_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def reg_dump(self, port_id):
        """
        Dump registers values of the given port
        :param port_id:
        :return: reg values

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        """

        # currently this method will cause host crash

        reg_cmd = 'reg_dump %s' % (port_id)
        self.process.sendline(reg_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result

    def queue_dump(self, port_id, queue_id):
        """
        Dump the queue-context of a queue-number
        :param port_id:
        :param queue_id:
        :return: queue-context

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0.
        queue-id represents the queue number relative to the port, whose context information needs to be logged
        """

        dump_cmd = 'queue_dump %s %s' % (port_id, queue_id)
        self.process.sendline(dump_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result

    def desc_dump(self, port_id, queue_id):
        """
        Dump the descriptors of the C2H and H2C rings of the specified queue number of the given port.
        :param port_id:
        :param queue_id:
        :return: desctiptor

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0.
        queue-id represents the queue number relative to the port, whose context information needs to be logged
        """

        dump_cmd = 'desc_dump %s %s' % (port_id, queue_id)
        self.process.sendline(dump_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result

    def dma_to_device(self, port_id, num_queues, input_filename, dst_addr, size, iterations):
        """
        DMA the data from host to card
        :param port_id:
        :param num_queues:
        :param input_filename:
        :param dst_addr:
        :param size:
        :param iterations:
        :return:

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver
                The first PCIe function that is bound has port id as 0
        num-queues represents the total number of queues to use for transmitting the data
        input-filename represents the path to a valid binary data file, contents of which needs to be DMA’ed
        dst-addr represents the destination address (offset) in the card to where DMA should be done in memory mapped mode
                 This field is ignored for streaming mode queues.
        size represents the amount of data in bytes that needs to be transmitted to the card from the given input file
             Data will be segmented across queues such that the total data transferred to the card is size amount
        iterations represents the number of loops to repeat the same DMA transfer
        """

        dma_to_dev_cmd = 'dma_to_device %s %s %s %s %s %s' % (
        port_id, num_queues, input_filename, dst_addr, size, iterations)
        self.process.sendline(dma_to_dev_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result

    def dma_from_device(self, port_id, num_queues, output_filename, src_addr, size, iterations):
        """
        DMA the data from card to host
        :param port_id:
        :param num_queues:
        :param output_filename:
        :param src_addr:
        :param size:
        :param iterations:
        :return:

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver
                The first PCIe function that is bound has port id as 0
        num-queues represents the total number of queues to use for transmitting the data
        output-filename represents the path to output file to dump the received data
        src-addr represents the source address (offset) in the card from where DMA should be done in memory mapped mode.
                 This field is ignored for streaming mode queues.
        size represents the amount of data in bytes that needs to be received from the card.
             Data will be segmented across queues such that the total data transferred from the card is size amount
        iterations represents the number of loops to repeat the same DMA transfer
        """

        dma_from_dev_cmd = 'dma_to_device %s %s %s %s %s %s' % (
        port_id, num_queues, output_filename, src_addr, size, iterations)
        self.process.sendline(dma_from_dev_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result

    def process_return(self):
        self.process.kill(1)
        print "Exit qdma process"

    def kill_process(self):
        self.process.sendintr()
        print "Kill qdma process"


if __name__ == "__main__":

    dpdkp = Qdmaplugin(cmd)
    # dpdkp.run()
    # ret = dpdkp.send_cmd()

    dpdkp.flush_output()

    ret = dpdkp.port_init(0, 1, 1, 1024, 2048)
    # print ret

    ret = dpdkp.dma_to_device(0, 1,'data/datafile0_4K.bin', 0, 4096, 1)
    print ret

    ret = dpdkp.dma_from_device(0, 1, 'data/port0_qcount0_size4k.bin', 0, 4096, 1)
    print ret




    # ret = dpdkp.reg_read(0, 0, 0)
    # print ret

    # ret = dpdkp.reg_write(0, 0, 0, 0x1)
    # print ret

    #  It will cause system crash
    # ret = dpdkp.reg_dump(0)
    # print ret

    # ret = dpdkp.queue_dump(0, 0)
    # print ret

    # ret = dpdkp.desc_dump(0, 0)
    # print ret

    #  return failure
    # ret = dpdkp.port_reset(0, 1, 1, 1024, 2048)
    # print ret

    #  It will cause system crash
    # ret = dpdkp.port_remove(0)
    # print ret

    ret = dpdkp.port_close(0)
    print ret





    # dpdkp.port_close(0)

    # dpdkp.port_remove(0)

    # dpdkp.port_init(port_id=0, num_queues=1, st_queues=1, ring_depth=1024, pkt_buffer_size=2048)



    # dpdkp = pexpect.spawn(cmd,  logfile=sys.stdout)
    # #print str(dpdkp)
    # while True:
    #     dpdkp.expect("xilinx-app>")
    #     dpdkp.logfile_read = sys.stdout
    #     # print(dpdkp.after)
    #     # dpdkp.sendline('help\r')
    #     # dpdkp.expect("xilinx-app>")
    #     # print(dpdkp.after)
    #     dpdkp.logfile_read = sys.stdout
    #
    #     str = raw_input("");
    #     if str:
    #         dpdkp.sendline(str)






    # dpdkp = subprocess.Popen(args=cmd,
    #                          stdin=subprocess.PIPE,
    #                          stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE,
    #                          shell=True)
    #
    # print ("#######################################")
    # print ("start qdma_app pid is %s" % dpdkp.pid)
    # print ("#######################################")
    #
    # print("\n")
    #
    # while True:
    #     qdma_cmd = raw_input('')
    #     dpdkp.stdin.write(qdma_cmd + "\n")  # Include '\n'
    #     dpdkp.stdin.flush()


    # for stdout_line in iter(dpdkp.stdout.readline, ""):
    #     print stdout_line
    # dpdkp.stdout.close()
    # return_code = dpdkp.wait()
    # if return_code:
    #     raise subprocess.CalledProcessError(return_code, cmd)

    # while True:
    #     nextline = dpdkp.stdout.readline()
    #     print(nextline.strip())
    #     sys.stdout.flush()
    #     if nextline == "" and scan.poll() != None:
    #         break

    # while True:
    #     response = dpdkp.stdout.readline()
    #     if response != '':
    #         print "Process response:", response
    #     else:
    #         sys.stdout.flush()
    #         break
    #
    #     s = raw_input('Enter message:')
    #     dpdkp.stdin.write(s + "\n")  # Include '\n'
    #     dpdkp.stdin.flush()


    # dpdkp.stdin.write(b"help\n")
    # dpdkp.stdin.close()
    # while True:
    #    line = dpdkp.stdout.readline()
    #    line = line.strip()
    #    if line:
    #        print (line)
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



    # try:
    #     while dpdkp.poll() is None:
    #         line = dpdkp.stdout.readline()
    #         line = line.strip()
    #         if line:
    #             print (line)
    #         else:
    #             #dpdkp.stdin.write(b"help\n")
    #             #dpdkp.stdin.close()
    #             stdout, stderr = dpdkp.communicate('help\r')
    #             print (stdout)
    #             print (stderr)
    #             #line dpdkp.stdout.readline()
    #             #print (line)
    #             #if dpdkp.stderr is not None:
    #             #    print dpdkp.stderr.readline()
    #             # while True:
    #             #     line = dpdkp.stdout.readline()
    #             #     line = line.strip()
    #             #     if line:
    #             #         print (line)
    #             #     else:
    #             #         break
    #
    #         #print (input_cmd)
    #         #print (type(input_cmd))
    #         #dpdkp.communicate(str(input_cmd))
    #
    #     if dpdkp.pool() != 0:
    #         err = dpdkp.stderr.read().decode(current_encoding)
    #         print (err)
    #
    #     if dpdkp.returncode == 0:
    #        print ('dpdk run success')
    #     else:
    #        print ('dpdk process run fail')
    # except:
    #    print('exception')


#dpdkp.communicate(cmd_help)

#dpdkp.communicate(cmd_port_init)

#dpdkp.communicate(cmd_port_close)



#ret = dpdkp.wait()
#print (ret)


#dpdkp.poll()
#print(dpdkp.stdout.read())
#dpdkp.wait()

#print(dpdkp.returncode)
