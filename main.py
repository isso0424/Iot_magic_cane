import serial
import time
import switch_bot


class Connection:
    def __init__(self, port):
        self.ser = serial.Serial("/dev/ttyUSB0", port)
        self.data_lis = []

    def _refresh_data(self):
        del self.data_lis[0]
        self.data_lis.append(
            float(
                self.ser.readline().decode("ASCII")
            )
        )

    def _reset(self):
        self.data_lis = []
        for i in range(2):
            self.data_lis.append(
                float(
                    self.ser.readline().decode("ASCII")
                )
            )

    def main(self):
        for i in range(2):
            self.data_lis.append(
                float(
                    self.ser.readline().decode("ASCII")
                )
            )
        while True:
            if self.data_lis[0] < -10 and self.data_lis[1] > 10:
                print("左1")
                self._reset()
            elif self.data_lis[0] > 10 and self.data_lis[1] < -10:
                print("右1")
                self._reset()
            elif self.data_lis[0] < -10 and self.data_lis[1] < 10:
                print("右2")
                self._reset()
            elif self.data_lis[0] > 10 and self.data_lis[1] > -10:
                print("左2")
                self._reset()
            else:
                self._refresh_data()
            """
            # 右
            if data > 10:
                switch_bot.main(10, "FC:5B:2F:10:D7:82", "off")
                exit()
            # 左
            elif data < -10:
                switch_bot.main(10, "FC:5B:2F:10:D7:82", "on")
                exit()
            """


if __name__ == "__main__":
    con = Connection(9600)
    con.main()
