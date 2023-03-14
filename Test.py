import time
import serial
import serial.tools.list_ports as list_ports
import random


def get_arduino_port():
    ports = list_ports.comports()
    selected = None
    for port, desc, _ in sorted(ports):
        print(f"{port}: {desc}")

        if "Arduino" in desc:
            if selected is None:
                selected = port
            elif type(selected) is str:
                selected = list((selected, port))
            else:
                selected.append(port)

    return selected


def send_message(connection, message):
    print(message)
    connection.write(bytes(message, "utf-8"))
    time.sleep(0.1)
    recived = connection.read(100)
    print("Recived:", recived)


port = get_arduino_port()
arduino = serial.Serial(port, baudrate=9600, timeout=0.2)

while True:
    send_message(arduino, str(random.randint(0, 10)))
    time.sleep(1)
