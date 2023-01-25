import struct

SLAVE_CMD = 11

class Log4Device:
    PROTOCOL_HEADER_STRUCT = struct.Struct("<BBB")
    SET_STREAM_CMD_STRUCT = struct.Struct("<BBBBBB")
    SLAVE_DATA_USB_STRUCT = struct.Struct("<QHii")
    SLAVE_DATA_POE_STRUCT = struct.Struct("<QHiiii")
    KEEP_ALIVE = struct.Struct("<BBBBB")

    def __init__(self):
        self.current = 0.0
        self.voltage = 0.0
        self.power = 0.0
        self.timestamp = 0
        self.device = "Log4 USB"

    def __str__(self):
        return "%s,%f,%f,%f" % (
            self.timestamp, self.current, self.voltage, self.power)

    def setStreaming(self, serialdevice, streaming):
        serialdevice.write(Log4Device.SET_STREAM_CMD_STRUCT.pack(
            0x3A, 0x01, 0x11, 0x01, 0x01 if streaming else 0x00, 0x0A))

    def keepAlive(selfself, serialdevice):
        serialdevice.write(Log4Device.KEEP_ALIVE.pack(
            0x3A, 0x01, 0x02, 0x00, 0x0A))

    def measure(self, serialdevice):
        byte_read = serialdevice.read()
        if byte_read == b":":
            serialdata = serialdevice.read(3)
            (address, command_code, data_len) = \
                Log4Device.PROTOCOL_HEADER_STRUCT.unpack(serialdata)
            data = serialdevice.read(data_len)
            end_byte = serialdevice.read()
            if end_byte != b'\n':
                return

            if command_code == SLAVE_CMD:
                timestamp = 0
                timestamp_us = 0

                if data_len == 18:
                    timestamp, timestamp_us, self.current, self.voltage = \
                        Log4Device.SLAVE_DATA_USB_STRUCT.unpack(data)
                self.power = self.current * self.voltage
                self.timestamp = (timestamp / 1.0e3) + (timestamp_us / 1.0e6)
