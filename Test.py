import time
import serial
import serial.tools.list_ports as list_ports
import random

import nidaqmx as ni
from nidaqmx import stream_readers
import nidaqmx.stream_writers as ns
from nidaqmx.constants import AcquisitionType, Edge
import multiprocessing as mp


"""def pwm_output(freq, d_c, sample_freq, channel):
    task = ni.Task("Tache 1")
    task.ao_channels.add_ao_voltage_chan(physical_channel= channel,min_val=0.0, max_val=10.0)
    print(1)
    task.timing.cfg_samp_clk_timing(rate=sample_freq, sample_mode = AcquisitionType.CONTINUOUS)
    print(2)
    task.stop()
    writer = ns.AnalogSingleChannelWriter(task_out_stream = )
    #task.out_stream.output_buf_size = 1000
    print(3)
    writer.write_one_sample_pulse_frequency(frequency=freq, duty_cycle=d_c)
    print(4)
    

my_task = pwm_output(100, 0.5, 1000, "myDAQ1/ao0")
my_task.stop()
my_task.close()
time.sleep(10.0)"""

def pwm(duty_cycle, freq, port):
    T = 1e9/freq
    task = ni.Task()
    task.ao_channels.add_ao_voltage_chan(port, min_val=0, max_val=10.0)  # Ajouter le canal analogique
    start = time.time_ns()
    while True:
        while (((time.time_ns() -start) % T)/T) > duty_cycle:
            pass
        task.write(2.5)  # Écrire une tension sur le port
        while (((time.time_ns() -start) % T)/T) < duty_cycle:
            pass
        task.write(0.0)
#pwm(0.8, 10, "myDAQ1/ao0")

# La fonction retourne la tache, donc on peut appeler task.stop() et task.close() 
# à l'extérieur de la fonction



"""def get_arduino_port():
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
    print("Recived:", recived)"""


if __name__ == "__main__":
    # port = get_arduino_port()
    # arduino = serial.Serial(port, baudrate=9600, timeout=0.2)
    #
    # while True:
    #     send_message(arduino, str(random.randint(0, 10)))
    #     time.sleep(1)
    args = {"duty_cycle" : 0.8, "freq" :100, "port" :"myDAQ1/ao0"}
    pwm_task = mp.Process(target = pwm, kwargs = args)
    pwm_task.start()
    print(1)
    time.sleep(10.0)
    pwm_task.kill()
    print(2)
    args["duty_cycle"]


    
