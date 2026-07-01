import serial
import re
import threading
import queue
import config


class Balance:

    def __init__(self):

        self.data_queue = queue.Queue()

        self.ser = serial.Serial(
            port=config.SERIAL_PORT,
            baudrate=config.BAUD_RATE,
            bytesize=config.DATA_BITS,
            parity=config.PARITY,
            stopbits=config.STOP_BITS,
            timeout=config.TIMEOUT
        )

        self.thread = threading.Thread(
            target=self.listen,
            daemon=True
        )

        self.thread.start()

    def listen(self):
        """
        Runs forever in the background.
        Waits for the balance to transmit data.
        """

        while True:

            raw = self.ser.readline()

            if not raw:
                continue

            try:
                raw = raw.decode().strip()

            except UnicodeDecodeError:
                continue

            match = re.search(r"[-+]?\d+\.\d+", raw)

            if match:

                weight = float(match.group())

                self.data_queue.put(weight)