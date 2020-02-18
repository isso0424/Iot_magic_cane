import bluetooth
from bluetooth.ble import DiscoveryService, GATTRequester
import time


class Driver(object):
    handle = 0x16
    commands = {
        'press': '\x57\x01\x00',
        'on': '\x57\x01\x01',
        'off': '\x57\x01\x02',
    }

    def __init__(self, device, timeout_secs=None):
        self.device = device
        self.timeout_secs = timeout_secs if timeout_secs else 5
        self.req = None

    def _connect(self):
        self.req = GATTRequester(self.device, False)
        self.req.connect(True, 'random')
        connect_start_time = time.time()
        while not self.req.is_connected():
            if time.time() - connect_start_time >= self.timeout_secs:
                raise RuntimeError('Connection to {} timed out after {} seconds'
                                   .format(self.device, self.timeout_secs))

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.req.disconnect()

    def run_command(self, command):
        return self.req.write_by_handle(self.handle, self.commands[command])


def operate(timeout, addr, command):
    with Driver(device=addr, timeout_secs=timeout) as driver:
        print('Connected!')
        command_list = {
            'press': '\x57\x01\x00',
            'on': '\x57\x01\x01',
            'off': '\x57\x01\x02',
        }
        if command in command_list.keys():
            driver.run_command(command)
        else:
            ValueError("Command is press, on or off.")
        print("completed")


def all_on(timeout, addr_list):
    if not isinstance(addr_list, list):
        TypeError("addr_list is list of addresses")
    for addr in addr_list:
        operate(timeout=timeout, addr=addr, command='on')
        print("{} is switched on!".format(addr))
    print("finish!!!")


def all_off(timeout, addr_list):
    if not (isinstance(addr_list, list) or isinstance(addr_list[0], str)):
        TypeError("addr_list is list of string addresses")
    for addr in addr_list:
        operate(timeout=timeout, addr=addr, command='off')
        print("{} is switched off!".format(addr))
    print("finished!!!")


if __name__ == "__main__":
    operate(10, "FC:5B:2F:10:D7:82", "on")
