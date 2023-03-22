import numpy as np ; import math as mt
import time ;
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (ResolutionType, VoltageUnits, 
                               BridgeUnits, AcquisitionType)
import Parameters as para

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



def GET_V(port,freq):
    '''Fonction qui permet de faire une lecture de voltage à une certaine fréquence sur le ports sélectionné '''

    task = nidaqmx.Task() # Coucou, wake-up
    task.ai_channels.add_ai_voltage_chan(
        physical_channel=port, min_val=0.0, max_val=2.0, units=VoltageUnits.VOLTS)  # initialise port
    task.timing.cfg_samp_clk_timing(freq, sample_mode=AcquisitionType.CONTINUOUS)  # Spécification lecture MydaQ
    task.start()  # Commence à m'écouter
    v = task.read(number_of_samples_per_channel = 1)[0] # lit le port
    task.stop()#Ne m'écoute plus
    task.close() #Retourne dodo
    return v

def GET_R(r1, vs, channel_list, freq):
    '''Fonction qui permet de retourner la valeur de résistance d'une thermistance'''
    v0, v1 =  GET_V(channel_list[0], freq), GET_V(channel_list[1], freq)
    rt0 = r1*(1/((vs/v0)-1.0))
    rt1 = r1*(1/((vs/v1)-1.0))
    return rt0,rt1


def GET_T(a,b,c, channel_list, freq):

    RT0,RT1 = GET_R(115000.0,15.0, channel_list, freq)
    T0 = 1/(a+(b*mt.log(RT0)) + (c*(mt.log(RT0))**3))
    T1 = 1/(a+(b*mt.log(RT1)) + (c*(mt.log(RT1))**3))
    print(f'Hot : {T0} °K,   Cold : {T1} °K')

# Test
GET_T(*para.coef_init_guess[:3], ["myDAQ1/ai0", "myDAQ1/ai1"], 10.0)
