#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author  :   Minxie

@License :   (C) Copyright 2013-2020

@Contact :   Minx@xilinx.com

@Software:   Xilinx QDMA DPDK plugin base class

@File    :   qdma_dpdk_python_wrapper.py

@Time    :   2020-06-15

@Desc    :
'''

import os
import sys
import time
import pexpect

# basedir = os.path.dirname(__file__)
# print ("basedir:" + basedir)


class Qdmaplugin():
    def __init__(self, cmd, debug=False):
        """
        Start the qdma app
        :param cmd:
        :param debug
        cmd represents qdma command string
        debug option, True/False , make the subprocess output print to screen
        """

        # todo parameter check
        print ("  ")
        self.cmd = cmd
        self.debug = debug
        print "execute command %s,   debug mode is %s" % (self.cmd, self.debug)
        print ("  ")

        print ("#####################################################################")
        print ("###########Starting the Xilinx QDMA DPDK plugin service##############")
        print ("#####################################################################")
        print ("  ")

        try:
            if self.debug:
                print "###plugin execute in debug mode###"
                self.process = pexpect.spawn(self.cmd, timeout=None, logfile=sys.stdout)
                print self.process
                self.process.expect("xilinx-app>", timeout=60)
            else:
                print "###plugin execute in normal mode###"
                self.process = pexpect.spawn(self.cmd, timeout=None)
        except Exception, e:
            print "###qdma app start failure###"
            print e
            self.exit_with_usage()

    def flush_output(self):
        """
        Clear the contents of readbufer
        :return:
        """
        try:
            self.process.expect("xilinx-app>", timeout=60)
            result = self.process.before
        except pexpect.EOF:
            result = "flush_output EOF"
        except pexpect.TIMEOUT:
            result = "flush_output TIMEOUT"
        finally:
            return result

    def set_echo(self, switch):
        """
        Set the subprogram response method.
        :param switch:
        :return:
        switch True -enable / False-disable
        """
        self.process.setecho(switch)

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

        try:
            port_cmd = 'port_init %s %s %s %s %s' % (port_id, num_queues, st_queues, ring_depth, pkt_buffer_size)

            self.process.sendline(port_cmd)
            self.process.expect("xilinx-app>", timeout=60)

            result = self.process.before
        except pexpect.EOF:
            result = "port_init EOF"
        except pexpect.TIMEOUT:
            result = "port_init TIMEOUT"
        finally:
            return result

    def port_close(self, port_id):
        """
        Free up all the allocated resources and removes the queues associated with the port.
        :param port_id:
        :return:string of close result

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        """

        try:
            port_cmd = 'port_close %s' % port_id
            self.process.sendline(port_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "port_close EOF"
        except pexpect.TIMEOUT:
            result = "port_close TIMEOUT"
        finally:
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

        try:
            port_cmd = 'port_reset %s %s %s %s %s' % (port_id, num_queues, st_queues, ring_depth, pkt_buff_size)
            self.process.sendline(port_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
            return result
        except pexpect.EOF:
            result = "port_reset EOF"
        except pexpect.TIMEOUT:
            result = "port_reset TIMEOUT"
        finally:
            return result

    def port_remove(self, port_id):
        """
        Free up all the resources allocated for the port and removes the port from application use
        :param port_id:
        :return:

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        """

        try:
            port_cmd = 'port_remove %s' % port_id
            self.process.sendline(port_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "port_remove EOF"
        except pexpect.TIMEOUT:
            result = "port_remove TIMEOUT"
        finally:
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

        try:
            reg_cmd = 'reg_read %s %s %s' % (port_id, bar_num, address)
            self.process.sendline(reg_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "reg_read EOF"
        except pexpect.TIMEOUT:
            result = "reg_read TIMEOUT"
        finally:
            return result

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

        try:
            reg_cmd = 'reg_write %s %s %s %s' % (port_id, bar_num, address, value)
            self.process.sendline(reg_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "reg_write EOF"
        except pexpect.TIMEOUT:
            result = "reg_write TIMEOUT"
        finally:
            return result

    def reg_dump(self, port_id):
        """
        Dump registers values of the given port
        :param port_id:
        :return: reg values

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0
        """

        # currently this method will cause host crash
        try:
            reg_cmd = 'reg_dump %s' % (port_id)
            self.process.sendline(reg_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "reg_dump EOF"
        except pexpect.TIMEOUT:
            result = "reg_dump TIMEOUT"
        finally:
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
        try:
            dump_cmd = 'queue_dump %s %s' % (port_id, queue_id)
            self.process.sendline(dump_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "queue_dump EOF"
        except pexpect.TIMEOUT:
            result = "queue_dump TIMEOUT"
        finally:
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
        try:
            dump_cmd = 'desc_dump %s %s' % (port_id, queue_id)
            self.process.sendline(dump_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "desc_dump EOF"
        except pexpect.TIMEOUT:
            result = "desc_dump TIMEOUT"
        finally:
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

        try:
            dma_to_dev_cmd = 'dma_to_device %s %s %s %s %s %s' % (
                port_id, num_queues, input_filename, dst_addr, size, iterations)
            self.process.sendline(dma_to_dev_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "dma_to_device EOF"
        except pexpect.TIMEOUT:
            result = "dma_to_device TIMEOUT"
        finally:
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

        try:
            dma_from_dev_cmd = 'dma_from_device %s %s %s %s %s %s' % (
                port_id, num_queues, output_filename, src_addr, size, iterations)
            self.process.sendline(dma_from_dev_cmd)
            self.process.expect("xilinx-app>")
            result = self.process.before
        except pexpect.EOF:
            result = "dma_from_device EOF"
        except pexpect.TIMEOUT:
            result = "dma_from_device TIMEOUT"
        finally:
            return result

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

    def is_qdma_app_run(self):
        """
        check if the adma application is running
        :return: True-running, false-dead
        """
        return self.process.isalive()

    def process_close(self):
        """
        Close the QDMA app
        :return: execution result
        """
        return self.process.close()

    def process_return(self):
        self.process.kill(1)
        print "Exit qdma process"

    def process_kill(self):
        self.process.sendintr()
        print "Kill qdma process"

    def exit_with_usage(self):
        """
        If an error occurs in the middle of the program, print the prompt message and exit
        :return: exit
        """
        print globals()['__doc__']
        os._exit(1)

    def get_methods(self):
        return(list(filter(lambda m: not m.startswith("__") and not m.endswith("__")
                                     and callable(getattr(self, m)), dir(self))))