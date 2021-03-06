import serial
import time
import switch_bot


def _switch(addr, command):
    switch_bot.operate(10, addr, command)


class RemoteSwitch:
    """
    Switch Bot を動かすクラスです
    非同期で処理します
    """
    def __init__(self, port, path, limit_count=-1):
        """
        Args:
            port(int): シリアル通信で使用するPort
            path(str): シリアル通信するデバイスのpath
        """
        self.ser = serial.Serial(path, port)
        self.data_lis = []
        self.limit_count = limit_count
        self.alive = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.close()

    def _refresh_data(self):
        """
        データを新しいものに更新する
        """
        del self.data_lis[0]
        self.data_lis.append(
            float(
                self.ser.readline().decode("ASCII")
            )
        )

    def _reset(self):
        """
        Switch Botを操作した後にデータをリセットする
        """
        self.limit_count -= 1
        if self.limit_count == 0:
            self.alive = False
        self.data_lis = []
        for i in range(2):
            self.data_lis.append(
                float(
                    self.ser.readline().decode("ASCII")
                )
            )
            time.sleep(0.1)

    def _control(self):
        """
        Switch Botを動かすメインの関数
        thread_aliveがTrueである限り処理をし続ける
        """
        for i in range(2):
            self.data_lis.append(
                float(
                    self.ser.readline().decode("ASCII")
                )
            )
            time.sleep(0.1)

        while self.alive:
            if (self.data_lis[0] < -15 and self.data_lis[1] > 15) or (self.data_lis[0] < -15 and self.data_lis[1] < 15):
                print("off")
                _switch("CF:13:80:93:9E:03", "off")
                time.sleep(2)
                self._reset()

            elif (self.data_lis[0] > 15 and self.data_lis[1] < -15) or self.data_lis[0] > 15 and self.data_lis[1] > -15:
                print("on")
                _switch("CF:13:80:93:9E:03", "on")
                time.sleep(2)
                self._reset()

            else:
                self._refresh_data()

    def start(self):
        self._control()


if __name__ == "__main__":
    con = RemoteSwitch(port=9600, path="/dev/ttyUSB0", limit_count=-1)
    con.start()
