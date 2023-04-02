import time
import serial
import serial.tools.list_ports as list_ports
import random

import nidaqmx as ni
from nidaqmx.stream_writers import CounterWriter
from nidaqmx.constants import AcquisitionType

def pwm_output(freq, duty_cycle, sample_freq, physical_channel):
    task = ni.Task()
    task.ao_channels.add_ao_voltage_chan(physical_channel=physical_channel,
                                         min_val=0.0, max_val=10.0)
    task.timing.cfg_samp_clk_timing(rate=sample_freq, 
                                    sample_mode=AcquisitionType.CONTINUOUS)
    writer = CounterWriter
    writer.write_one_sample_pulse_frequency(frequency=freq, duty_cycle=duty_cycle, auto_start=True)
    return task  
# La fonction retourne la tache, donc on peut appeler task.stop() et task.close() 
# à l'extérieur de la fonction



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

    


    
