import serial
import serial.tools.list_ports as list_ports
import numpy as np
import math as mt
import time
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (ResolutionType, VoltageUnits, BridgeUnits, AcquisitionType)
import Parameters as para
import nidaqmx as ni
from nidaqmx.stream_writers import CounterWriter
import multiprocessing as mp


def get_arduino_port(verbose=False):
    ports = list_ports.comports()
    if verbose:
        for p in ports:
            print(p.device) #print(p[0])
            #print(p.description) #print(p[1])
            #print(p[2])
            print(p.device_path)
        print(len(ports), 'ports found')

    ports = [(port, desc) for port, desc, _ in sorted(ports) if "Arduino" in desc]

    assert len(ports) != 0, "Aucun port n'a été reconnu comme étant connecté à un Arduino"

    if len(ports) > 1:
        print("Voici les Arduinos connectés aux ports:")
        for i, (port, desc) in enumerate(ports):
            print(f"{i+1} - {port}: {desc}")
        num = int(input("\nVeuillez sélectionner le numéro du port à connecter: "))

        return ports[num-1][0]

    return ports[0][0]


def v_to_temp(v, a, b, c, e, r):
    """
    Fonction qui convertit le voltage en température.

    :param v: voltage à convertir
    :param a,b,c,e,r:
    :return : température en float

    """
    arg = r * v / (e-v)
    denom = a + b * np.log(arg) + c * (np.log(arg))**3
    return 1 / denom


def set_voltage(port, voltage):
    """
    Fonction qui définit le voltage en sortie des analogue out du myDaq.

    :param port: port ao0 ou ao1
    :param voltage: valeur du voltage voulue

    """
    task = nidaqmx.Task()
    task.ao_channels.add_ao_voltage_chan(port,min_val=0,max_val=10.0) # Ajouter le canal analogique
    task.write(voltage)  # Écrire une tension sur le port
    task.close()


def mesure_v(port):
    """
      Fonction qui permet de faire une lecture de voltage à une certaine fréquence sur le ports sélectionné.

       :param port: port ao0 ou ao1 en string (voir paramètre pour plus d'information)
       :return : valeur de voltage en float

    """

    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan(
        physical_channel=port, min_val=0.0, max_val=2.0, units=VoltageUnits.VOLTS)  # initialise port
    task.timing.cfg_samp_clk_timing(sample_mode=AcquisitionType.CONTINUOUS, rate=100)  # Spécification lecture MydaQ
    task.start()  # Commence à m'écouter
    v = task.read(number_of_samples_per_channel = 1)[0] # lit le port
    task.stop()#Ne m'écoute plus
    task.close() #Retourne dodo
    return v


def mesure_resistance(r1, vs, channel_list):
    """
    Fonction qui permet de retourner la valeur de résistance d'une thermistance.

    :param port: port ao0 ou ao1 en string (voir paramètre pour plus d'information)
    :return : valeur de résistance des thermistances 1 et 2 en float

    """
    v0, v1 = mesure_v(channel_list[0]), mesure_v(channel_list[1])
    rt0 = r1*(1/((vs/v0)-1.0))
    rt1 = r1*(1/((vs/v1)-1.0))
    return rt0,rt1


def mesure_temperature(a,b,c, channel_list, freq):
    RT0, RT1 = mesure_resistance(115000.0,15.0, channel_list)
    T0 = 1/(a+(b*mt.log(RT0)) + (c*(mt.log(RT0))**3))
    T1 = 1/(a+(b*mt.log(RT1)) + (c*(mt.log(RT1))**3))
    print(f'Hot : {T0} °K,   Cold : {T1} °K')


def pwm(duty_cycle, freq, port):
    T = 1e9/freq
    task = ni.Task()
    task.ao_channels.add_ao_voltage_chan(port, min_val=0, max_val=10.0)  # Ajouter le canal analogique
    start = time.time_ns()
    while True:
        while (((time.time_ns() -start) % T)/T) > duty_cycle:
            pass
        task.write(5)  # Écrire une tension sur le port
        while (((time.time_ns() -start) % T)/T) < duty_cycle:
            pass
        task.write(0)


class PowerControler:
    def __init__(self, port, max_p, freq=None, p=None):
        self.port = port  # Port de l'élément chauffant
        self.power = p
        self.max_p = max_p
        self.task = None
        self.args = {"port": port, "duty_cycle": None, "freq": freq}
        self.running_args = dict()

    def start_pwm(self):
        if self.args != self.running_args:
            if self.task is not None: self.stop_pwm()
            self.running_args = self.args.copy()
            self.task = mp.Process(target=pwm, kwargs=self.running_args)
            self.task.start()

    def set_arg(self, **kwargs):
        self.args.update(kwargs)

    def stop_pwm(self):
        self.task.kill()
        self.task = None
        set_voltage(self.port, 0)

    def set_power(self, p):
        self.power = min(p, self.max_p)
        self.args["duty_cycle"] = self.p_to_duty_cycle(self.power)

    def p_to_duty_cycle(self, p):
        return p / self.max_p


if __name__ == "__main__":
    a = PowerControler("myDAQ1/ao0", 30, freq=5)
    a.set_power(30)
    a.start_pwm()
    print(a.args)
    time.sleep(10)

    a.set_power(15)
    a.start_pwm()
    print(a.args)
    time.sleep(10)

    a.stop_pwm()
    # port = get_arduino_port()
    # arduino = serial.Serial(port, baudrate=9600, timeout=0.2)
    # arduino.close()
