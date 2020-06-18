import os
import sys

import subprocess
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
        self.cmd = cmd

        print ("#######################################")
        print ("###########start the server#############")
        print ("#######################################")

        # self.process = pexpect.spawn(self.cmd, timeout=None, logfile=sys.stdout)
        self.process = pexpect.spawn(self.cmd, timeout=None)

    def flush_output(self):
        self.process.expect("xilinx-app>")

    def port_init(self, port_id, num_queues, st_queues, ring_depth, pkt_buffer_size):
        """port initailization
        port_init < port - id > < num - queues > < st - queues > < ring - depth > < pkt - buff - size >

        This command assigns queues to the port, sets up required resources for the queues,
        and prepares queues for data processing

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
                The first PCIe function that is bound has port id as 0.

        num-queues represents the total number of queues to be assigned to the port

        num-st-queues represents the total number of queues to be configured in streaming mode.
                      This implies that the (num-queues - num-st-queues) number of queues has to be configured
                      in memory mapped mode.

        ring-depth represents the number of entries in C2H and H2C descriptor rings of each queue of the port

        pkt-buff-size represents the size of the data that a single C2H or H2C descriptor can support

        example  port_init 0 1 1 1024 2048"""

        port_cmd = 'port_init %s %s %s %s %s' % (port_id, num_queues, st_queues, ring_depth, pkt_buffer_size)

        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")

        result = self.process.before
        return result
        # print self.process.after

    def port_close(self, port_id):
        """port close
        port_close <port-id>
        This command frees up all the allocated resources and removes the queues associated with the port
        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
        The first PCIe function that is bound has port id as 0"""

        port_cmd = 'port_close %s' % port_id
        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def port_reset(self, port_id, num_queues, st_queues, ring_depth, pkt_buff_size):
        """port reset
        port_reset <port-id> <num-queues> <st-queues> <ring-depth > <pkt-buff-size>"""

        port_cmd = 'port_reset %s %s %s %s %s' % (port_id, num_queues, st_queues, ring_depth, pkt_buff_size)
        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def port_remove(self, port_id):
        """port remove
        port_remove <port-id>"""

        port_cmd = 'port_remove %s' % port_id
        self.process.sendline(port_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def reg_read(self, port_id, bar_num, address):
        """Reads Specified Register
        reg_read <port-id> <bar-num> <address>
        This command is used to read the specified register

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
        The first PCIe function that is bound has port id as 0

        bar-num represents the PCIe BAR where the register is located

        address represents offset of the register in the PCIe BAR bar-num"""

        reg_cmd = 'reg_read %s %s %s' % (port_id, bar_num, address)
        self.process.sendline(reg_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def reg_write(self, port_id, bar_num, address, value):
        """Writes Specified Register
        reg_write <port-id> <bar-num> <address> <value>
        This command is used to write a 32-bit value to the specified register

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
        The first PCIe function that is bound has port id as 0.

        bar-num represents the PCIe BAR where the register is located

        address represents offset of the register in the PCIe BAR bar-num

        value represents the value to be written at the register offset address"""

        reg_cmd = 'reg_write %s %s %s %s' % (port_id, bar_num, address, value)
        self.process.sendline(reg_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result
        # self.process.logfile_read = sys.stdout

    def reg_dump(self, port_id):
        """To dump all the valid registers
        reg_dump <port-id>
        This command dumps important QDMA registers values of the given port on console

        port-id represents a logical numbering for PCIe functions in the order they are bind to igb_uio driver.
        The first PCIe function that is bound has port id as 0."""

        # currently this method will cause host crash

        reg_cmd = 'reg_dump %s' % (port_id)
        self.process.sendline(reg_cmd)
        self.process.expect("xilinx-app>")
        result = self.process.before
        return result

    def queue_dump (self, port_id, queue_id):
        


    def process_return (self):
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
    print ret

    ret = dpdkp.reg_read(0, 0, 0)
    print ret

    ret = dpdkp.reg_write(0, 0, 0, 0x1)
    print ret

    ret = dpdkp.reg_dump(0)
    print ret

    ret = dpdkp.port_reset(0, 1, 1, 1024, 2048)
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
