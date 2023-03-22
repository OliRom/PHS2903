import time
import serial
import serial.tools.list_ports as list_ports
import random
import nidaqmx as ni
from nidaqmx import stream_writers


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


if __name__ == "__main__":
    # port = get_arduino_port()
    # arduino = serial.Serial(port, baudrate=9600, timeout=0.2)
    #
    # while True:
    #     send_message(arduino, str(random.randint(0, 10)))
    #     time.sleep(1)

    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("mydaq1/ai0")
        a = task.read()
        print(a)

    task = ni.Task()
    # task.ao_channels.add_ao_voltage_chan(task.out_stream)
    # task.close()

    a = stream_writers.CounterWriter("mudaq1/ao0")
    a.write_one_sample_pulse_frequency(10, 0.2)
    task.close()

    time.sleep(20)
