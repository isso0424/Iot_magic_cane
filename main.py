import serial
import switch_bot
import threading


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
        self.control_thread = threading.Thread(target=self._control())
        self.thread_alive = False

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
            self.thread_alive = False
        self.data_lis = []
        for i in range(2):
            self.data_lis.append(
                float(
                    self.ser.readline().decode("ASCII")
                )
            )

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

        while self.thread_alive:
            if self.data_lis[0] < -10 and self.data_lis[1] > 10:
                print("off")
                switch_bot.operate(10, "FC:5B:2F:10:D7:82", "off")
                self._reset()
            elif self.data_lis[0] > 10 and self.data_lis[1] < -10:
                print("on")
                switch_bot.operate(10, "FC:5B:2F:10:D7:82", "on")
                self._reset()
            elif self.data_lis[0] < -10 and self.data_lis[1] < 10:
                print("off")
                switch_bot.operate(10, "FC:5B:2F:10:D7:82", "off")
                self._reset()
            elif self.data_lis[0] > 10 and self.data_lis[1] > -10:
                print("on")
                switch_bot.operate(10, "FC:5B:2F:10:D7:82", "on")
                self._reset()
            else:
                self._refresh_data()

    def start(self):
        if self.thread_alive:
            RuntimeError("This class can run only one thread per one instance.")
        self.thread_alive = True
        self.control_thread.start()

    def kill(self):
        if not self.thread_alive:
            RuntimeError("This instance dont have running thread.")
        self.thread_alive = False
        self.control_thread.join()

    def wait_finish(self):
        if not self.thread_alive:
            RuntimeError("This instance dont have running thread.")
        self.control_thread.join()


if __name__ == "__main__":
    con = RemoteSwitch(port=9600, path="/dev/ttyUSB0", limit_count=3)
    con.start()
