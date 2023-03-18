import numpy as np
import time ; from tkinter import *
import nidaqmx ; from nidaqmx import stream_readers;
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (BridgeConfiguration, VoltageUnits, 
                               BridgeUnits, AcquisitionType)
import matplotlib.pyplot as plt
###############################################################################################################################################

"""Nom des différents ports physiques (id) [ces informations peuvent être changées dans NI MAX]: 
myDAQ1/ai0 ; myDAQ1/ai1 ; myDAQ1/ao0 ; myDAQ1/ao1
myDAQ1/audioOutputLeft ; myDAQ1/audioOutputRight

L-->  https://www.ni.com/docs/fr-FR/bundle/ni-daqmx/page/mxdevconsid/mydaqphyschanns.html

 Limites d'entrée (valeurs maximales et minimales)
L--> https://www.ni.com/docs/fr-FR/bundle/ni-daqmx/page/measfunds/limitsettings.html 

Demander au prof si on peut configurer un gain avec nidaqmx pour les entrées analogiques

Chercher de l'info pour de la lecture en simultané de plusieurs ports analogiques"""

###############################################################################################################################################


#Conditions d'échantillonnage
def analog_setup(freq = float, id_ai0 = str, id_ai1 = str, bool_ai0 = bool, bool_ai1 = bool, T_max = float):

    task = nidaqmx.Task()
    cas1 = None ; cas2 = None ; cas3 = None
    if (bool_ai0 == True) and (bool_ai1 == True):
        task.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai0, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI0
        task.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai1, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI1
        cas1 = True
    elif (bool_ai0 == True) and (bool_ai1 == False):
        task.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai0, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI0
        cas2 = True
    elif (bool_ai0 == False) and (bool_ai1 == True):
        task.ai_channels.add_ai_voltage_chan(
            physical_channel=id_ai1, min_val=0.0,max_val=2.0,units=VoltageUnits.VOLTS) #init. AI1
        cas3 = True
        
    task.timing.cfg_samp_clk_timing(freq, sample_mode = AcquisitionType.CONTINUOUS)    #Cette ligne doit être après l'init. des AI
    
    #reader = AnalogMultiChannelReader(task.in_stream) [read alternatif]
    #data = np.ndarray([2,])  [read alternatif]
    task.start()

    T = 0
    while T < 1000:                                 # Modifier 1000 pour T_max
        data = task.read(number_of_samples_per_channel = 1)

        #a) reader.read_one_sample(data)  [read alternatif]
        #b) Afficher data sur GUI

        #convertir les tensions list en float
        if cas1 == True:
            V0 = data[0][0]
            V1 = data[1][0]
            print(V0,"v   ",V1,"v")
        elif cas2 == True:
            V0 = data[0]
            print(V0,"V")
        elif cas3 == True:
            V1 = data[0]
            print(V1,"V")
        #Insérer équation de température en fonction de voltage provenant de l'étallonnage
        T = T + 1

    task.stop()
    task.close()


analog_setup(30.0, "myDAQ1/ai0", "myDAQ1/ai1", True, True, 40.0)




